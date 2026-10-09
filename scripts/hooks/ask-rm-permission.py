import json
import posixpath
import shlex
import sys


def command_strings(value, key=""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from command_strings(child, child_key.lower())
    elif isinstance(value, list):
        for child in value:
            yield from command_strings(child, key)
    elif isinstance(value, str) and key in {
        "command",
        "cmd",
        "script",
        "shellcommand",
    }:
        yield value


def contains_rm(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        words = list(lexer)
    except ValueError:
        return True

    for word in words:
        executable = posixpath.basename(word.lstrip("\\"))
        if executable in {"rm", "rmdir", "unlink"}:
            return True
    return False


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    sys.exit(0)

tool_name = str(payload.get("tool_name", "")).lower()
if tool_name in {"rm", "rmdir", "unlink"} or any(
    contains_rm(command) for command in command_strings(payload.get("tool_input", {}))
):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        "This tool call may run rm, rmdir, or unlink. "
                        "Approve it only if the deletion is intended."
                    ),
                }
            }
        )
    )
