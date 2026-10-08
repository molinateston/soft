"""Hermes adapter for the shared, advisory-only JEV client."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

try:
    from . import credentials
except ImportError:  # Loaded as a standalone file (offline tests).
    _SPEC = importlib.util.spec_from_file_location("jev_auto_credentials", Path(__file__).with_name("credentials.py"))
    credentials = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(credentials)


CLI_PATH = Path.home() / ".local/share/jev-auto/src/cli.mjs"
MAX_INPUT_BYTES = 24_000
PROCESS_TIMEOUT_SECONDS = 12

# Mirrored from src/contracts.mjs; a cross-runtime test checks the registered schema.
_CONTEXT = {"anyOf": [{"type": "string"}, {"type": "object"}, {"type": "array"}]}
_QUESTION_TYPES = [
    {
        "type": "object",
        "properties": {
            "type": {"const": "noul"},
            "instructions": _CONTEXT,
            "criteria": {
                "type": "object",
                "minProperties": 1,
                "additionalProperties": False,
                "properties": {"true": _CONTEXT, "false": _CONTEXT},
            },
        },
        "required": ["type", "instructions"],
        "additionalProperties": False,
    },
    {
        "type": "object",
        "properties": {
            "type": {"const": "choice"},
            "instructions": _CONTEXT,
            "criteria": {
                "type": "object",
                "minProperties": 2,
                "maxProperties": 255,
                "propertyNames": {"minLength": 1},
                "additionalProperties": {"anyOf": [*_CONTEXT["anyOf"], {"type": "null"}]},
            },
        },
        "required": ["type", "instructions", "criteria"],
        "additionalProperties": False,
    },
    {
        "type": "object",
        "properties": {
            "type": {"const": "score"},
            "instructions": _CONTEXT,
            "criteria": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": _CONTEXT,
            },
        },
        "required": ["type", "instructions", "criteria"],
        "additionalProperties": False,
    },
]

SCHEMA = {
    "name": "jev_decide",
    "description": (
        "Evaluate 1–16 batched closed semantic questions through JEV. "
        "Use minimal non-sensitive evidence, up to 24 KB. Advisory only: "
        "this tool cannot authorize actions. Each answer comes with "
        "faixas[id]: alta (>= 0.8) follow it; media (0.6-0.8) check another "
        "way; baixa (< 0.6 or an abstain option) decide yourself. If "
        "unavailable, continue the existing workflow without retrying automatically."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "state": {
                **_CONTEXT,
                "description": "Only the minimal non-sensitive facts needed for the decisions.",
            },
            "questions": {
                "type": "object",
                "minProperties": 1,
                "maxProperties": 16,
                "propertyNames": {"minLength": 1, "maxLength": 64},
                "additionalProperties": {"oneOf": _QUESTION_TYPES},
            },
        },
        "required": ["state", "questions"],
        "additionalProperties": False,
    },
}


def _unavailable(reason):
    return {
        "available": False,
        "reason": reason,
        "answers": {},
        "advisory_only": True,
    }


def decide(args):
    """Keep credentials inside the shared client and never expose subprocess errors."""
    if not isinstance(args, dict) or set(args) != {"state", "questions"}:
        return _unavailable("invalid_arguments")
    try:
        payload = json.dumps(args, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        if len(payload.encode("utf-8")) > MAX_INPUT_BYTES:
            return _unavailable("invalid_arguments")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        return _unavailable("invalid_arguments")

    node = shutil.which("node")
    if node is None or not CLI_PATH.is_file():
        return _unavailable("runtime_unavailable")
    try:
        result = subprocess.run(
            [node, str(CLI_PATH), "--decide"],
            input=payload,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=PROCESS_TIMEOUT_SECONDS,
            check=False,
            env=credentials.child_environment(),
        )
    except subprocess.TimeoutExpired:
        return _unavailable("runtime_timeout")
    except (OSError, UnicodeError):
        return _unavailable("runtime_unavailable")
    if result.returncode != 0:
        return _unavailable("runtime_unavailable")
    try:
        response = json.loads(result.stdout)
        if not isinstance(response, dict) or type(response.get("available")) is not bool:
            return _unavailable("runtime_output_invalid")
        # Reject non-standard JSON numbers before returning to Hermes.
        json.dumps(response, allow_nan=False)
    except (TypeError, ValueError, RecursionError):
        return _unavailable("runtime_output_invalid")
    if response.get("reason") == "upstream_auth":
        credentials.forget()
    return response


def handle(args, **kwargs):
    return json.dumps(decide(args), ensure_ascii=False, allow_nan=False)


def register(ctx):
    ctx.register_tool(
        name="jev_decide",
        toolset="jev",
        schema=SCHEMA,
        handler=handle,
        description=SCHEMA["description"],
    )
    # The explicit tool stays available when automatic advice is disabled.
    if ctx.get_config("automation_enabled", True) is not False:
        from .automation import Automation
        Automation().register(ctx)
