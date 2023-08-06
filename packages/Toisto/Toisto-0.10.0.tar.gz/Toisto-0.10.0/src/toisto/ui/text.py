"""Output for the user."""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

from ..metadata import CHANGELOG_URL, NAME, VERSION
from ..model.language.label import Label
from ..model.quiz.quiz import Quiz
from .dictionary import DICTIONARY_URL, linkify_and_enumerate
from .diff import colored_diff

theme = Theme(dict(secondary="grey69", quiz="medium_purple1", inserted="bright_green", deleted="bright_red"))

console = Console(theme=theme)

LINK_KEY = "⌘ (the command key)" if sys.platform == "darwin" else "Ctrl (the control key)"

WELCOME = f"""👋 Welcome to [underline]{NAME} [white not bold]v{VERSION}[/white not bold][/underline]!

Practice as many words and phrases as you like, for as long as you like.

[secondary]{NAME} quizzes you on words and phrases repeatedly. Each time you answer
a quiz correctly, {NAME} will wait longer before repeating it. If you
answer incorrectly, you get one additional attempt to give the correct
answer. If the second attempt is not correct either, {NAME} will reset
the quiz interval.

How does it work?
● To answer a quiz: type the answer, followed by Enter.
● To repeat the spoken text: type Enter without answer.
● To skip to the answer immediately: type ?, followed by Enter.
● To read more about an [link={DICTIONARY_URL}/underlined]underlined[/link] word: keep {LINK_KEY} pressed
  while clicking the word. Not all terminals may support this.
● To quit: type Ctrl-C or Ctrl-D.
[/secondary]"""

NEWS = (
    f"🎉 {NAME} [white not bold]{{0}}[/white not bold] is [link={CHANGELOG_URL}]available[/link]. "
    f"Upgrade with [code]pipx upgrade {NAME}[/code]."
    ""
)

DONE = f"""👍 Good job. You're done for now. Please come back later or try a different topic.
[secondary]Type `{NAME.lower()} -h` for more information.[/secondary]
"""

TRY_AGAIN = "⚠️  Incorrect. Please try again."

CORRECT = "✅ Correct.\n"


def feedback_correct(guess: Label, quiz: Quiz) -> str:
    """Return the feedback about a correct result."""
    return CORRECT + meaning(quiz) + other_answers(guess, quiz)


def feedback_incorrect(guess: Label, quiz: Quiz) -> str:
    """Return the feedback about an incorrect result."""
    evaluation = "" if guess == "?" else "❌ Incorrect. "
    if guess == "?":
        label = "The correct answer is" if len(quiz.answers) == 1 else "The correct answers are"
        return f"{label} {linkify_and_enumerate(*quiz.answers)}.\n" + meaning(quiz)
    return (
        f'{evaluation}The correct answer is "{colored_diff(guess, quiz.answer)}".\n'
        + meaning(quiz)
        + other_answers(quiz.answer, quiz)
    )


def meaning(quiz: Quiz) -> str:
    """Return the quiz's meaning, if any."""
    return f"[secondary]Meaning {linkify_and_enumerate(*quiz.meanings)}.[/secondary]\n" if quiz.meanings else ""


def other_answers(guess: Label, quiz: Quiz) -> str:
    """Return the quiz's other answers, if any."""
    if answers := quiz.other_answers(guess):
        label = "Another correct answer is" if len(answers) == 1 else "Other correct answers are"
        return f"""[secondary]{label} {linkify_and_enumerate(*answers)}.[/secondary]\n"""
    return ""


def instruction(quiz: Quiz) -> str:
    """Return the instruction for the quiz."""
    return f"[quiz]{quiz.instruction()}:[/quiz]"


def show_welcome(latest_version: str | None) -> None:
    """Show the welcome message."""
    console.print(WELCOME)
    if latest_version and latest_version.strip("v") > VERSION:
        console.print(Panel(NEWS.format(latest_version), expand=False))
        console.print()
