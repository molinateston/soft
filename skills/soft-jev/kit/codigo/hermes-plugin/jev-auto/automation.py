"""Native Hermes lifecycle integration; never changes authorization or providers.

Only current text and short catalog descriptors cross the shared client's privacy
gate. Histories, file contents, tool arguments/results and persona prompts do not.
Post-tool hooks collect metadata locally; they never call the decision API.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import threading
import unicodedata
import time

try:
    from . import credentials
except ImportError:  # Loaded as a standalone file (offline tests).
    _SPEC = importlib.util.spec_from_file_location("jev_auto_credentials", Path(__file__).with_name("credentials.py"))
    credentials = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(credentials)


AUTOMATION_CLI = Path.home() / ".local/share/jev-auto/src/automation-cli.mjs"
MAX_EVENT_BYTES = 128_000
MAX_TEXT_CHARS = 16_000
MAX_TURNS = 128
TURN_TTL_SECONDS = 1800
SAFE_PERSONALITIES = ("helpful", "concise", "technical", "creative", "teacher")
_ID = re.compile(r"^[A-Za-z0-9_.:/-]{1,100}$")
# Natural-language role requests. `@x`, `/x` and `$x` only count when x is an
# installed persona or skill: paths and mentions are not role choices.
_ROLE_PHRASE = re.compile(
    r"\b(?:act as|atue como|aja como|assuma o papel|fa[cç]a o papel|use (?:o|a) agente|usar (?:o|a) agente)\b", re.I
)


def _invokes(text, ids):
    """Same rule as hooks/catalog.mjs hasExplicitInvocation, over real ids only."""
    for name in ids:
        escaped = re.escape(name)
        if (re.search(r"(?:^|\s)[@/$](?:role-)?" + escaped + r"(?=$|[\s.,!?:])", text, re.I)
                or re.search(r"(?:ativa[r]?|ative|use|activate)\s+(?:a\s+|o\s+)?(?:persona\s+|agente\s+|skill\s+)?"
                             + escaped + r"(?=$|[\s.,!?:])", text, re.I)):
            return True
    return False


# Mesmos padrões de src/verification.mjs (casos compartilhados em test/verification-cases.json).
# Só o tipo sai daqui; o comando nunca vai ao core nem ao log.
_COMMAND_KINDS = (
    ("git", re.compile(r"\b(?:git\s+(?:push|log|show|status|rev-parse|ls-remote|fetch|diff)|gh\s+(?:pr|run|api|release|repo))\b", re.I)),
    ("test", re.compile(r"\b(?:(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:test|lint|typecheck|build|check|house:check|validate[\w:-]*|smoke)|node\s+--test|pytest|unittest|go\s+test|cargo\s+test|make\s+(?:test|check)|vitest|jest|tsc|eslint|runtime_hooks\.py)\b", re.I)),
    ("http", re.compile(r"\b(?:curl|wget|httpie|lynx)\b", re.I)),
    ("read", re.compile(r"(?:^|[;&|(]\s*)(?:cat|head|tail|less|sed\s+-n|grep|rg|ls|diff|stat|wc|jq|find)\b", re.I)),
)
_SHELL_TOOLS = {"bash", "shell", "exec_command", "run_terminal_command", "run_terminal_cmd", "terminal",
                "local_shell", "execute_command", "container.exec"}
_READ_TOOLS = {"read", "read_file", "view", "view_file", "grep", "glob", "search_files", "list_dir", "ls",
               "file_search", "notebookread"}
_HTTP_TOOLS = {"webfetch", "web_fetch", "web_extract", "fetch", "browser_navigate", "browser_snapshot",
               "browser_take_screenshot", "browser_screenshot", "browser_vision", "screenshot"}


def verification_kinds(tool_name, command=None):
    """Tipos de verificação (git, http, test, read) que uma ferramenta concluída representa."""
    if not isinstance(tool_name, str) or not tool_name:
        return []
    leaf = re.split(r"__|[.:/]", tool_name)[-1].lower()
    if leaf in _READ_TOOLS:
        return ["read"]
    if leaf in _HTTP_TOOLS:
        return ["http"]
    if leaf not in _SHELL_TOOLS and tool_name.lower() not in _SHELL_TOOLS:
        return []
    if isinstance(command, list):
        command = " ".join(part for part in command if isinstance(part, str))
    if not isinstance(command, str) or not command:
        return []
    bounded = command[:4096]
    return [kind for kind, pattern in _COMMAND_KINDS if pattern.search(bounded)]


_STOPWORDS = {
    "que", "para", "pra", "com", "uma", "uns", "umas", "dos", "das", "nos", "nas", "por", "isso", "esse", "essa",
    "este", "esta", "aqui", "ali", "mais", "muito", "como", "quando", "onde", "qual", "quais", "tem", "ter", "ser",
    "est", "sao", "foi", "vai", "faz", "fazer", "pode", "agora", "ainda", "tambem", "sobre", "entre", "seu", "sua",
    "meu", "minha", "nao", "sim", "the", "and", "for", "with", "this", "that", "from", "use", "when", "into", "your",
    "you", "are", "not", "all", "any", "skill", "squad", "agent", "agente", "source", "command", "migrated", "novo",
    "novos", "nova", "novas",
}


def _words(value):
    """Mesmo radical de hooks/catalog.mjs: sem acento, sem "s" final, 6 letras."""
    plain = unicodedata.normalize("NFD", value)
    plain = "".join(char for char in plain if not unicodedata.combining(char)).lower()
    stems = set()
    for word in re.findall(r"[a-z0-9]{3,}", plain):
        if word in _STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        stems.add(word[:6])
    return stems


def explicit_role(text, personas):
    return bool(_ROLE_PHRASE.search(text)) or _invokes(text, personas)


def run_event(payload):
    """An unavailable CLI cannot interrupt a Hermes turn or expose its stderr."""
    fallback = {"status": "fallback", "context": "", "reason": "runtime_unavailable"}
    try:
        encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        if len(encoded.encode("utf-8")) > MAX_EVENT_BYTES:
            return {**fallback, "reason": "event_too_large"}
        node = shutil.which("node")
        if not node or not AUTOMATION_CLI.is_file():
            return fallback
        completed = subprocess.run(
            [node, str(AUTOMATION_CLI)], input=encoded, capture_output=True,
            text=True, encoding="utf-8", timeout=12, check=False,
            env=credentials.child_environment(),
        )
        if completed.returncode != 0:
            return fallback
        output = json.loads(completed.stdout)
        if not isinstance(output, dict) or output.get("status") not in {
            "ok", "cached", "skipped", "fallback"
        }:
            return fallback
        json.dumps(output, allow_nan=False)
        if output.get("reason") == "upstream_auth":
            credentials.forget()
        return output
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError, subprocess.TimeoutExpired):
        return fallback


def _text(value):
    # Multimodal input: consider only ordinary text, never image URLs/attachments.
    if isinstance(value, list):
        value = "\n".join(
            block["text"] for block in value
            if isinstance(block, dict) and block.get("type") in {"text", "input_text"}
            and isinstance(block.get("text"), str)
        )
    return value if isinstance(value, str) and len(value) <= MAX_TEXT_CHARS else ""


def _too_large(value):
    if isinstance(value, list):
        value = "\n".join(
            block["text"] for block in value
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        )
    return isinstance(value, str) and len(value) > MAX_TEXT_CHARS


def _origin(platform):
    """Log only: which Hermes surface sent the request (whatsapp, cron, cli...)."""
    value = platform.lower() if isinstance(platform, str) else ""
    value = re.sub(r"[^a-z0-9_]", "_", value)[:17]
    return "hermes_" + value if value and value[0].isalpha() else "hermes"


def _code_note(result):
    """Note from the local "pronto sem prova" check; generated by the core from enums only."""
    check = result.get("code_check") if isinstance(result, dict) else None
    note = check.get("note") if isinstance(check, dict) else None
    return note if isinstance(note, str) and 0 < len(note) <= 600 else ""


def _profile():
    try:
        from hermes_constants import get_hermes_home
        home = str(get_hermes_home())
    except ImportError:
        home = str(Path.home() / ".hermes")
    return hashlib.sha256(home.encode()).hexdigest()[:20]


def _shortlist(rows, text, limit=12, only_relevant=False):
    words = _words(text)
    valid = {}
    invoked = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = row.get("id", row.get("name"))
        description = row.get("description", "")
        if isinstance(name, str) and _ID.fullmatch(name) and isinstance(description, str):
            # Descriptors only. Full skill/persona content is never sent for routing.
            valid[name] = {"id": name, "description": description[:180]}
            if _invokes(text, [name]):
                invoked.add(name)
    # Relevance: request words in the id count double (no alphabetical list when something matches).
    score = {name: 2 * len(words & _words(name)) + len(words & _words(row["description"]))
             for name, row in valid.items()}
    rows = list(valid.values())
    if only_relevant and any(score[row["id"]] for row in rows):
        rows = [row for row in rows if score[row["id"]] or row["id"] in invoked]
    # An explicitly invoked skill always stays in the list so it can be recognized.
    return sorted(rows, key=lambda row: (row["id"] not in invoked, -score[row["id"]], row["id"]))[:limit]


def catalog(text, platform, child=False):
    """Use installed, enabled skill metadata and native personality definitions."""
    skills, tools, personas, persona_prompts = [], [], [], {}
    explicit = False
    config = {}
    try:
        from hermes_cli.config import load_config_readonly
        config = load_config_readonly() or {}
    except Exception:
        pass
    try:
        from tools.skills_tool import skills_list
        skills = _shortlist(json.loads(skills_list()).get("skills", []), text, only_relevant=True)
    except Exception:
        pass
    try:
        from hermes_cli.personality import (
            active_personality_name, available_personalities, describe_personality,
            render_personality_prompt,
        )
        explicit = bool(active_personality_name(config) or config.get("agent", {}).get("system_prompt"))
        definitions = available_personalities(config)
        for name in SAFE_PERSONALITIES:
            if name not in definitions:
                continue
            prompt = render_personality_prompt(definitions[name])
            if not isinstance(prompt, str) or not prompt or len(prompt) > 2000:
                continue
            personas.append({"id": name, "description": describe_personality(definitions[name], width=180)})
            persona_prompts[name] = prompt
    except Exception:
        pass
    try:
        # pre_llm_call has no child agent's tool allowlist. Do not pretend the
        # broader platform catalog is available inside a restricted subagent.
        if not child:
            from model_tools import get_tool_definitions
            from tools.registry import registry
            enabled = config.get("platform_toolsets", {}).get(platform or "cli")
            if not enabled:
                enabled = config.get("toolsets", ["hermes-cli"])
            definitions = get_tool_definitions(
                enabled_toolsets=enabled, quiet_mode=True, skip_tool_search_assembly=True,
            )
            families = {}
            for definition in definitions:
                function = definition.get("function", {})
                name = function.get("name", "")
                family = registry.get_toolset_for_tool(name)
                if isinstance(family, str) and _ID.fullmatch(family) and family != "jev":
                    families.setdefault(family, []).append(name)
            tools = _shortlist([
                {"id": family, "description": "Available tools: " + ", ".join(sorted(names)[:5])}
                for family, names in families.items()
            ], text)
    except Exception:
        pass
    return {"skills": skills, "tools": tools, "personas": personas}, persona_prompts, explicit


class Automation:
    def __init__(self, runner=None, catalog_reader=None):
        self.runner = runner or run_event
        self.catalog_reader = catalog_reader or catalog
        self.lock = threading.RLock()
        self.turns = {}
        self.active = {}
        # Nota da checagem em código "pronto sem prova", entregue no próximo pedido da sessão.
        self.pending_notes = {}

    def register(self, ctx):
        for name, callback in (
            ("pre_llm_call", self.prepare), ("post_tool_call", self.collect),
            ("pre_verify", self.file_review), ("post_llm_call", self.observe),
            ("on_session_end", self.end), ("on_session_finalize", self.end),
            ("on_session_reset", self.end),
        ):
            ctx.register_hook(name, callback)
        ctx.register_middleware("tool_request", self.tool_request)

    def _prune(self):
        now = time.monotonic()
        for key, state in list(self.turns.items()):
            if now - state["created"] > TURN_TTL_SECONDS:
                self.turns.pop(key, None)
        while len(self.turns) > MAX_TURNS:
            self.turns.pop(next(iter(self.turns)))
        self.active = {key: turn for key, turn in self.active.items() if (*key, turn) in self.turns}

    def _state(self, session_id, turn_id=""):
        profile = _profile()
        with self.lock:
            self._prune()
            turn_id = turn_id or self.active.get((profile, session_id), "")
            return self.turns.get((profile, session_id, turn_id))

    def _event(self, state, event, **extra):
        payload = {
            "event": event, "harness": "hermes", "profile": state["profile"],
            "session_id": state["session_id"], "turn_id": state["turn_id"],
            "origin": state.get("origin", "hermes"), **extra,
        }
        try:
            # Parallel Hermes tool completions share one metadata state file.
            # Serialize this turn's events so a concurrent collect does not lose
            # evidence to the shared client's deliberately nonwaiting lock.
            with state["event_lock"]:
                result = self.runner(payload)
            return result if isinstance(result, dict) else {}
        except Exception:
            # Hermes logs uncaught hook exception messages; do not let a provider
            # error or test runner echo private input through that path.
            return {}

    def prepare(self, session_id="", turn_id="", user_message="", platform="", **kwargs):
        if not session_id or not turn_id:
            return None
        profile = _profile()
        key = (profile, session_id, turn_id)
        with self.lock:
            self._prune()
            if key in self.turns:
                context = self.turns[key].get("context", "")
                return {"context": context} if context else None
            pending = self.pending_notes.pop((profile, session_id), "")
            state = {
                "profile": profile, "session_id": session_id, "turn_id": turn_id,
                "origin": _origin(platform), "too_large": _too_large(user_message),
                "created": time.monotonic(), "request": _text(user_message),
                "context": "", "persona_prompts": {}, "catalog": {}, "explicit": False,
                "reviewed": False, "observed": False, "memory_seen": set(), "delegated": {},
                "event_lock": threading.RLock(),
            }
            self.turns[key] = state
            self.active[(profile, session_id)] = turn_id
        catalogs, prompts, configured_explicit = self.catalog_reader(
            state["request"], platform, bool(kwargs.get("parent_session_id")),
        )
        persona_ids = [row["id"] for row in catalogs.get("personas", []) if isinstance(row, dict)]
        skill_ids = [row["id"] for row in catalogs.get("skills", []) if isinstance(row, dict)]
        state.update(catalog=catalogs, persona_prompts=prompts,
                     explicit=configured_explicit or explicit_role(state["request"], persona_ids))
        if state["explicit"]:
            catalogs = {**catalogs, "personas": []}
        if _invokes(state["request"], skill_ids):
            catalogs = {**catalogs, "skills": []}
        if state["too_large"]:
            # Logged as skipped/too_large instead of vanishing; the text never goes on.
            result = self._event(state, "prepare", text="", skip_reason="too_large")
        else:
            result = self._event(state, "prepare", text=state["request"],
                                 explicit_choice=state["explicit"], **catalogs)
        context = result.get("context", "")
        if result.get("status") in {"ok", "cached"} and isinstance(context, str) and len(context) <= 2000:
            state["context"] = context
        if pending:
            # Somada à nota do JEV, nunca no lugar dela; não bloqueia nada.
            state["context"] = "\n".join(part for part in (state["context"], pending) if part)
        return {"context": state["context"]} if state["context"] else None

    def tool_request(self, tool_name="", args=None, session_id="", turn_id="", **kwargs):
        state = self._state(session_id, turn_id)
        if not state or not isinstance(args, dict):
            return None
        if tool_name == "memory":
            self._memory(state, args)
            return None  # Evaluation never changes memory operations or write gates.
        if tool_name != "delegate_task" or args.get("action", "spawn") != "spawn" or state["explicit"]:
            return None
        tasks = args.get("tasks")
        legacy = tasks is None and isinstance(args.get("goal"), str)
        if legacy:
            tasks = [args]
        if not isinstance(tasks, list) or len(tasks) > 16:
            return None
        updated, changed = [], False
        deadline = time.monotonic() + 10
        for task in tasks:
            if not isinstance(task, dict) or not isinstance(task.get("goal"), str):
                updated.append(task)
                continue
            goal = _text(task["goal"])
            context = task.get("context", "")
            personas = [row["id"] for row in state["catalog"].get("personas", []) if isinstance(row, dict)]
            if (not goal or not isinstance(context, str) or any(key in task for key in ("role", "persona"))
                    or explicit_role(goal + "\n" + context, personas)):
                updated.append(task)
                continue
            fingerprint = hashlib.sha256(goal.encode()).hexdigest()
            with self.lock:
                result = state["delegated"].get(fingerprint)
            if result is None:
                # Bound fan-out latency independently of the shared API budget.
                # A timed-out decision can take 12 s; remaining children then
                # keep their original context rather than serially timing out.
                if time.monotonic() >= deadline or len(state["delegated"]) >= 3:
                    updated.append(task)
                    continue
                result = self._event(state, "delegate", text=goal,
                                     personas=state["catalog"].get("personas", []), explicit_choice=False)
                with self.lock:
                    state["delegated"][fingerprint] = result
            selection = result.get("selection", {})
            persona = selection.get("persona") if isinstance(selection, dict) else None
            prompt = state["persona_prompts"].get(persona) if isinstance(persona, str) else None
            if result.get("status") not in {"ok", "cached"} or not prompt:
                updated.append(task)
                continue
            note = ("[JEV advisory delegation style: " + persona + "]\n" + prompt +
                    "\nPreserve the assigned objective, explicit instructions and all permissions.")
            updated.append({**task, "context": context + ("\n\n" if context else "") + note})
            changed = True
        if not changed:
            return None
        return {"args": updated[0] if legacy else {**args, "tasks": updated},
                "source": "jev-auto", "reason": "advisory_native_personality"}

    def _memory(self, state, args):
        operations = args.get("operations", [args])
        if not isinstance(operations, list):
            return
        for operation in operations[:4]:
            if not isinstance(operation, dict) or operation.get("action") not in {"add", "replace"}:
                continue
            candidate = _text(operation.get("content") or operation.get("new_text"))
            if not candidate:
                continue
            fingerprint = hashlib.sha256(candidate.encode()).hexdigest()
            with self.lock:
                if fingerprint in state["memory_seen"] or len(state["memory_seen"]) >= 4:
                    continue
                state["memory_seen"].add(fingerprint)
            self._event(state, "memory", text=candidate)

    def collect(self, tool_name="", session_id="", turn_id="", status="", args=None, **kwargs):
        state = self._state(session_id, turn_id)
        if not state or tool_name == "jev_decide" or not isinstance(tool_name, str) or not _ID.fullmatch(tool_name):
            return None
        normalized = "success" if status in {"ok", "success"} else (
            "failure" if status in {"error", "failed", "failure"} else "unknown"
        )
        evidence = {
            "tool_name": tool_name, "status": normalized,
            "wrote_files": normalized == "success" and tool_name in {"write_file", "patch", "apply_patch"},
        }
        # The command is classified here and dropped: only git/http/test/read reaches the core.
        command = args.get("command") if isinstance(args, dict) else None
        verify = verification_kinds(tool_name, command) if normalized != "failure" else []
        if verify:
            evidence["verify"] = verify
        self._event(state, "collect", evidence=evidence)
        return None

    def file_review(self, session_id="", attempt=0, changed_paths=None, final_response="", **kwargs):
        state = self._state(session_id)
        if not state or attempt != 0 or not changed_paths:
            return None
        with self.lock:
            if state["reviewed"]:
                return None
            state["reviewed"] = True
        result = self._event(state, "file_review", text=_text(final_response), request=state["request"],
                             evidence={"status": "unknown", "tool_name": "file_changes", "wrote_files": True})
        observations = result.get("observations", {})
        needs_review = isinstance(observations, dict) and any(
            type(observations.get(key)) in (int, float) and 0.8 <= observations[key] <= 1
            for key in ("review", "file_review")
        )
        if (result.get("status") in {"ok", "cached"} and isinstance(observations, dict)
                and needs_review):
            message = (
                "JEV advisory review: check that the final explanation matches the recorded file changes "
                "and verification evidence. Correct any unsupported completion claim. Do not repeat "
                "external actions or change permissions. This review is limited to one continuation."
            )
            note = _code_note(result)
            return {"action": "continue", "message": message + ("\n" + note if note else "")}
        return None

    def observe(self, session_id="", turn_id="", assistant_response="", **kwargs):
        state = self._state(session_id, turn_id)
        if not state:
            return None
        with self.lock:
            if state["observed"]:
                return None
            state["observed"] = True
        text = assistant_response if isinstance(assistant_response, str) else _text(assistant_response)
        if len(text) > MAX_TEXT_CHARS:
            result = self._event(state, "observe", text="", skip_reason="too_large")
        else:
            result = self._event(state, "observe", text=text, request=state["request"])
        note = _code_note(result)
        if note:
            with self.lock:
                self.pending_notes[(state["profile"], state["session_id"])] = note
                while len(self.pending_notes) > MAX_TURNS:
                    self.pending_notes.pop(next(iter(self.pending_notes)))
        return None  # May have streamed already. Never rewrite or block the final response.

    def end(self, session_id="", turn_id="", **kwargs):
        profile = _profile()
        with self.lock:
            for key in list(self.turns):
                if key[:2] == (profile, session_id) and (not turn_id or key[2] == turn_id):
                    self.turns.pop(key, None)
            current = self.active.get((profile, session_id))
            if not turn_id or current == turn_id:
                self.active.pop((profile, session_id), None)
        return None
