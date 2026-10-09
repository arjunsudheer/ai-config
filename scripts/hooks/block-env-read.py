import json
import posixpath
import re
import shlex
import sys


ENV_FILE = re.compile(
    r"(?<![A-Za-z0-9])\.env(?:[._-][^/\\\s\"'<>|;&]*)?"
    r"(?=$|[/\\\s\"'<>|;&])"
)
WRITE_TOOL_PARTS = ("write", "edit", "create", "patch", "replace", "save")
SHELL_TOOL_PARTS = ("bash", "terminal", "shell")
NON_READING_COMMANDS = {
    "chmod",
    "chown",
    "echo",
    "mkdir",
    "mv",
    "printf",
    "rm",
    "rmdir",
    "touch",
    "unlink",
}
COMMAND_WRAPPERS = {"busybox", "command", "env", "exec", "nice", "nohup", "sudo"}
SHELL_SEPARATORS = {";", "&&", "||", "&", "|", "(", ")"}


def strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, str):
        yield value


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


def shell_commands(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        words = list(lexer)
    except ValueError:
        return []

    commands = []
    at_command_start = True
    for word in words:
        if word in SHELL_SEPARATORS:
            at_command_start = True
        elif at_command_start and word in COMMAND_WRAPPERS:
            continue
        elif at_command_start and word.startswith("-"):
            continue
        elif at_command_start:
            commands.append(posixpath.basename(word.lstrip("\\")))
            at_command_start = False
    return commands


def only_non_reading_shell_commands(commands):
    return bool(commands) and all(
        names and all(name in NON_READING_COMMANDS for name in names)
        for names in (shell_commands(command) for command in commands)
    )


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    sys.exit(0)

tool_name = str(payload.get("tool_name", "")).lower()
tool_input = payload.get("tool_input", {})
input_strings = list(strings(tool_input))
references_env = any(ENV_FILE.search(value) for value in input_strings)
commands = list(command_strings(tool_input))
shell_tool = any(part in tool_name for part in SHELL_TOOL_PARTS)
is_write_tool = any(part in tool_name for part in WRITE_TOOL_PARTS)
is_non_reading_shell = (
    shell_tool
    and bool(commands)
    and only_non_reading_shell_commands(commands)
)

if references_env and not is_write_tool and not is_non_reading_shell:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Reading .env files is blocked by the global user hook."
                    ),
                }
            }
        )
    )
