import subprocess
import sys

from prompt_toolkit import HTML, PromptSession, print_formatted_text, prompt
from prompt_toolkit.completion import Completion, WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments_markdown_lexer.lexer import MarkdownLexer

from ai_git_commit.config import ICommitMessage


def git_user_commit_message() -> ICommitMessage:
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )

    type_options = [
        {"value": "feat", "label": "✨ Features", "hint": "A new feature"},
        {"value": "fix", "label": "🐞 Bug Fixes", "hint": "A bug fix"},
        {
            "value": "docs",
            "label": "📝 Documentation",
            "hint": "Documentation only changes",
        },
        {
            "value": "refactor",
            "label": "♻️ Code Refactoring",
            "hint": "A code change that neither fixes a bug nor adds a feature",
        },
        {
            "value": "perf",
            "label": "🚀 Performance",
            "hint": "A code change that improves performance",
        },
        {
            "value": "test",
            "label": "🧪 Tests",
            "hint": "Adding missing tests or correcting existing tests",
        },
        {
            "value": "build",
            "label": "🏗️ Build",
            "hint": "Changes that affect the build system or external dependencies",
        },
        {
            "value": "ci",
            "label": "🤖 CI",
            "hint": "Changes to our CI configuration files and scripts",
        },
        {
            "value": "style",
            "label": "💄 Styles",
            "hint": "A code change that improves code styles",
        },
    ]

    type_completer = WordCompleter([option["value"] for option in type_options])
    prompt_session = PromptSession(
        completer=type_completer, style=style, lexer=PygmentsLexer(MarkdownLexer)
    )

    def get_completions(document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        for option in type_options:
            if option["value"].startswith(word_before_cursor):
                yield Completion(
                    option["value"],
                    start_position=-len(word_before_cursor),
                    display=option["value"],
                    display_meta=option["hint"],
                )

    prompt_session.completer.get_completions = get_completions

    selected_type = prompt_session.prompt(
        HTML(
            "<b>Select the commit type <style fg='ansiwhite' bg='#00ff44'>[TAB]</style>:</b> "
        )
    )

    commit_type = next(
        (
            option["label"]
            for option in type_options
            if option["value"] == selected_type
        ),
        None,
    )

    commit_subject = prompt_session.prompt(
        HTML(f"<style fg='ansiwhite' bg='#00ff44'>{commit_type}:</style> ")
        if commit_type
        else "Write a brief title description for commit: "
    )

    commit_messages = []
    print_formatted_text(
        HTML("<ansiblue>Description [ENTER to exit or skip]</ansiblue>")
    )
    while True:
        msg = prompt_session.prompt(" - ")
        if not msg:
            break
        commit_messages.append(msg)

    if commit_type:
        commit_subject = f"{commit_type}: {commit_subject}"

    return ICommitMessage(id=0, subject=commit_subject, body=commit_messages)


def get_git_diff_output() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


def is_init_git_repository() -> bool:
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False


def exec_git_commit(commitMessage: ICommitMessage) -> None:
    with open("./.git/COMMIT_EDITMSG", "w") as f:
        f.write(f"{commitMessage['subject']}\n\n")
        for i in commitMessage["body"]:
            f.write(f" - {i}\n")

    subprocess.check_output(["git", "commit", "-F", "./.git/COMMIT_EDITMSG"])


def get_git_status_short_output() -> None:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=no"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    print_formatted_text(
        HTML(
            f"<style fg='ansiwhite' bg='#00ff44'><b>Checking Git Status</b></style>\n<style fg='#42f566'>{result.stdout}</style>"
        )
    )


def run_command_git_commit() -> None:
    if is_init_git_repository():
        get_git_status_short_output()
        commit_message = git_user_commit_message()

        checked = prompt(HTML("<b>Want to continue?</b> [y/n]: ")).lower()
        if checked.startswith("y") or checked == "":
            exec_git_commit(commit_message)
        else:
            print_formatted_text(
                HTML(
                    "<style fg='ansiwhite' bg='#ff0000'><b>Aborted:</b></style> canceled the commit ."
                )
            )
    else:
        print_formatted_text(
            HTML(
                "<style fg='ansiwhite' bg='#ff0000'><b>Error:</b></style> Current directory is not a git repository."
            )
        )

        sys.exit(1)
