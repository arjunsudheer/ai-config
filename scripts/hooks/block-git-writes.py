import json
import posixpath
import re
import shlex
import sys


COMMAND_KEYS = {
    "command",
    "commandline",
    "command_line",
    "cmd",
    "script",
    "shellcommand",
}
WRAPPERS = {"busybox", "command", "env", "exec", "nice", "nohup", "sudo"}
SHELLS = {"bash", "dash", "sh", "zsh"}
WRAPPER_OPTIONS_WITH_ARGUMENTS = {
    "-C",
    "-g",
    "-h",
    "-p",
    "-u",
    "--chdir",
    "--group",
    "--host",
    "--prompt",
    "--user",
}
SEPARATORS = {";", "&&", "||", "&", "|", "(", ")"}
OPTIONS_WITH_ARGUMENTS = {
    "-C",
    "-c",
    "--config-env",
    "--exec-path",
    "--git-dir",
    "--namespace",
    "--super-prefix",
    "--work-tree",
}
READ_ONLY_COMMANDS = {
    "blame",
    "cat-file",
    "check-attr",
    "check-ignore",
    "check-mailmap",
    "describe",
    "diff",
    "fsck",
    "grep",
    "help",
    "log",
    "ls-files",
    "ls-remote",
    "ls-tree",
    "merge-base",
    "name-rev",
    "rev-list",
    "rev-parse",
    "shortlog",
    "show",
    "show-ref",
    "status",
    "version",
    "verify-commit",
    "verify-tag",
    "whatchanged",
}
READ_ONLY_CONFIG_MODES = {
    "--get",
    "--get-all",
    "--get-regexp",
    "--get-urlmatch",
    "--list",
    "-l",
}
WRITE_OPTIONS = {
    "--edit",
    "--unset",
    "--unset-all",
    "--replace-all",
    "--add",
    "--remove-section",
    "--rename-section",
}


def command_strings(value, key=""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from command_strings(child, child_key.lower())
    elif isinstance(value, list):
        for child in value:
            yield from command_strings(child, key)
    elif isinstance(value, str) and key in COMMAND_KEYS:
        yield value


def split_commands(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        words = list(lexer)
    except ValueError:
        return []

    commands = []
    current = []
    for word in words:
        if word in SEPARATORS or word in {">", ">>", "<", "2>", "2>>"}:
            if current:
                commands.append(current)
                current = []
        else:
            current.append(word)
    if current:
        commands.append(current)
    return commands


def git_subcommand(words):
    index = 0
    while index < len(words):
        word = words[index]
        executable = posixpath.basename(word.lstrip("\\"))
        if executable in SHELLS and index + 2 < len(words) and words[index + 1] == "-c":
            nested = words[index + 2]
            if has_git_write(nested):
                return "blocked-shell-command", []
            return None, []
        if executable == "git":
            index += 1
            while index < len(words):
                option = words[index]
                if option in OPTIONS_WITH_ARGUMENTS:
                    index += 2
                    continue
                if option.startswith("--") and "=" in option:
                    index += 1
                    continue
                if option.startswith("-"):
                    index += 1
                    continue
                return option, words[index + 1 :]
            return None, []
        if executable == "env":
            index += 1
            while index < len(words):
                option = words[index]
                if option == "--":
                    index += 1
                    break
                if option in {"-u", "--unset", "-C", "--chdir"}:
                    index += 2
                    continue
                if option.startswith("--unset=") or option.startswith("--chdir="):
                    index += 1
                    continue
                if "=" in option and not option.startswith("-"):
                    index += 1
                    continue
                break
            continue
        if executable == "sudo":
            index += 1
            while index < len(words):
                option = words[index]
                if option == "--":
                    index += 1
                    break
                if option in WRAPPER_OPTIONS_WITH_ARGUMENTS:
                    index += 2
                    continue
                if option.startswith("--") and "=" in option:
                    index += 1
                    continue
                if option.startswith("-"):
                    index += 1
                    continue
                break
            continue
        if executable in WRAPPERS or word.startswith("-"):
            index += 1
            continue
        return None, []
    return None, []


def is_read_only(subcommand, arguments):
    if subcommand in READ_ONLY_COMMANDS:
        if subcommand == "fsck" and "--lost-found" in arguments:
            return False
        return True

    if subcommand in {"branch", "tag"}:
        if any(
            argument in {"-d", "-D", "--delete", "-m", "-M", "--move", "-f", "--force"}
            for argument in arguments
        ):
            return False
        return not any(not argument.startswith("-") for argument in arguments)

    if subcommand == "remote":
        return not arguments or all(
            argument in {"-v", "--verbose"} for argument in arguments
        ) or arguments[0] == "show"

    if subcommand == "stash":
        return not arguments or arguments[0] in {"list", "show"}

    if subcommand == "config":
        if any(argument in WRITE_OPTIONS for argument in arguments):
            return False
        return any(argument in READ_ONLY_CONFIG_MODES for argument in arguments)

    return False


def has_git_write(command):
    return any(
        subcommand is not None and not is_read_only(subcommand, arguments)
        for words in split_commands(command)
        for subcommand, arguments in [git_subcommand(words)]
    )


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    sys.exit(0)

tool_name = str(payload.get("tool_name", "")).lower()
tool_input = payload.get("tool_input", {})
commands = list(command_strings(tool_input))

git_tool_operation = re.search(r"(?:^|[^a-z])git[_\s-]+([a-z-]+)", tool_name)
tool_operation_blocked = (
    git_tool_operation is not None
    and not is_read_only(git_tool_operation.group(1), [])
)

if tool_operation_blocked or any(has_git_write(command) for command in commands):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Git write or repository-modifying commands are blocked "
                        "by the global user hook."
                    ),
                }
            }
        )
    )
