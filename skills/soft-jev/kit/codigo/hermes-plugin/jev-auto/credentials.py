"""TYPESAFE_API_KEY held in the gateway's memory.

TYPESAFE_API_KEY is always the primary path. When it is not already set in the
process environment, this module optionally falls back to your password manager,
if you use one that provides an `op read`-compatible command, reading it once
and holding it in memory. Without that cache, every hook would spawn a new
`node` process, which would run the password-manager read again: about 0.7 s
per consultation before the network round trip even starts. The gateway
process is long-lived, so the optional read happens once and the key is
passed to each child through its environment. The key is never written to
disk, logged or returned to Hermes.
"""

import os
import subprocess
import threading
import time


KEY_REFERENCE = "op://seu-cofre/sua-chave/credential"
RETRY_SECONDS = 300
_lock = threading.Lock()
_cache = {"key": None, "retry_at": 0.0}


def _valid(value):
    return (isinstance(value, str) and value.strip() and len(value) <= 8192
            and not any(character in value for character in "\r\n\0"))


def _read():
    """Optional shortcut: only used when TYPESAFE_API_KEY is not already set.
    Adjust KEY_REFERENCE to your own password manager's reference format, or
    remove this fallback entirely if you prefer to only ever use the
    environment variable.
    """
    try:
        completed = subprocess.run(
            ["op", "read", KEY_REFERENCE], capture_output=True, text=True,
            encoding="utf-8", timeout=5, check=False,
        )
    except (OSError, UnicodeError, subprocess.TimeoutExpired):
        return None
    value = completed.stdout.strip() if completed.returncode == 0 else ""
    return value if _valid(value) else None


def key():
    """The environment wins; otherwise, if available, the optional password-manager
    shortcut runs once, with a quiet retry after a failure.
    """
    # Adaptação OpenRouter: OPENROUTER_API_KEY é o caminho principal; TYPESAFE_API_KEY segue aceito.
    if _valid(os.environ.get("OPENROUTER_API_KEY")) or _valid(os.environ.get("TYPESAFE_API_KEY")):
        return None
    with _lock:
        if _cache["key"]:
            return _cache["key"]
        if time.monotonic() < _cache["retry_at"]:
            return None
        value = _read()
        _cache.update(key=value, retry_at=0.0 if value else time.monotonic() + RETRY_SECONDS)
        return value


def forget():
    """Called when the API rejects the key (`upstream_auth`), so it is read again."""
    with _lock:
        _cache.update(key=None, retry_at=0.0)


def child_environment(harness="hermes"):
    environment = {**os.environ, "JEV_HARNESS": harness}
    value = key()
    if value:
        environment["OPENROUTER_API_KEY"] = value
    return environment
