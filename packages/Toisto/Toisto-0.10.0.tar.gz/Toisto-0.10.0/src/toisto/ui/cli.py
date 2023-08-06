"""Command-line interface."""

import sys
from argparse import ArgumentParser, ArgumentTypeError, _SubParsersAction
from configparser import ConfigParser
from typing import get_args

from rich_argparse import RichHelpFormatter

from ..metadata import BUILT_IN_LANGUAGES, README_URL, SUMMARY, TOPICS, VERSION, latest_version
from ..model.language.cefr import CommonReferenceLevel
from ..model.language.iana_language_subtag_registry import ALL_LANGUAGES, IANA_LANGUAGE_SUBTAG_REGISTRY_URL


def add_language_arguments(parser: ArgumentParser, config: ConfigParser) -> None:
    """Add the language arguments to the parser."""
    languages = ", ".join(sorted(BUILT_IN_LANGUAGES))
    for argument in ("target", "source"):
        default = config.get("languages", argument, fallback=None)
        default_help = f"default: {default}; " if default else ""
        parser.add_argument(
            f"-{argument[0]}",
            f"--{argument}",
            default=default,
            dest=f"{argument}_language",
            help=f"{argument} language; {default_help}languages available in built-in topics: {languages}",
            metavar="{language}",
            required=not default,
            type=check_language,
        )


def check_language(language: str) -> str:
    """Check that the language is valid."""
    if language in ALL_LANGUAGES:
        return language
    message = f"invalid choice: '{language}' (see {IANA_LANGUAGE_SUBTAG_REGISTRY_URL} for valid choices)"
    raise ArgumentTypeError(message)


def add_topic_arguments(parser: ArgumentParser) -> None:
    """Add the topic arguments to the parser."""
    parser.add_argument(
        "-T",
        "--topic",
        action="append",
        default=[],
        choices=sorted([*TOPICS, "easter"]),
        metavar="{topic}",
        help="topic to use, can be repeated; default: all; available topics: %(choices)s",
    )
    parser.add_argument(
        "-f",
        "--topic-file",
        action="append",
        default=[],
        metavar="{topic file}",
        help="topic file to use, can be repeated",
    )


def add_level_arguments(parser: ArgumentParser, config: ConfigParser) -> None:
    """Add the language level arguments to the parser."""
    levels = get_args(CommonReferenceLevel)
    default = [level for level in levels if level in config.get("languages", "levels", fallback="")]
    default_help = ", ".join(default) if default else "all"
    parser.add_argument(
        "-l",
        "--level",
        action="append",
        default=default,
        dest="levels",
        metavar="{level}",
        choices=levels,
        help=f"language levels to use, can be repeated; default: {default_help}; available levels: %(choices)s",
    )


def add_practice_command(subparser: _SubParsersAction, config: ConfigParser) -> None:
    """Add a practice command."""
    command_help = (
        "practice a language, for example type `%(prog)s practice --target fi --source en` to "
        "practice Finnish from English"
    )
    add_command(subparser, "practice", "Practice a language.", command_help, config)


def add_progress_command(subparser: _SubParsersAction, config: ConfigParser) -> None:
    """Add a command to show progress."""
    command_help = (
        "show progress, for example `%(prog)s progress --target fi --source en` shows progress "
        "on practicing Finnish from English"
    )
    parser = add_command(subparser, "progress", "Show progress.", command_help, config)
    parser.add_argument(
        "-S",
        "--sort",
        metavar="{option}",
        choices=["retention", "attempts"],
        default="retention",
        help="how to sort progress information; default: by retention; available options: %(choices)s",
    )


def add_topics_command(subparser: _SubParsersAction, config: ConfigParser) -> None:
    """Add a command to show topics."""
    command_help = "show topics, for example `%(prog)s topics --topic nature` shows the contents of the nature topic"
    add_command(subparser, "topics", "Show topics.", command_help, config)


def add_command(
    subparser: _SubParsersAction,
    command: str,
    description: str,
    command_help: str,
    config: ConfigParser,
) -> ArgumentParser:
    """Add a command."""
    parser = subparser.add_parser(
        command,
        description=description,
        help=command_help,
        formatter_class=RichHelpFormatter,
    )
    add_language_arguments(parser, config)
    add_level_arguments(parser, config)
    add_topic_arguments(parser)
    return parser


def create_argument_parser(config: ConfigParser) -> ArgumentParser:
    """Create the argument parser."""
    epilog = f"See {README_URL} for more information."
    argument_parser = ArgumentParser(description=SUMMARY, epilog=epilog, formatter_class=RichHelpFormatter)
    latest = latest_version()
    version = f"v{VERSION}" + (f" ({latest} is available)" if latest and latest.strip("v") > VERSION else "")
    argument_parser.add_argument("-V", "--version", action="version", version=version)
    command_help = "default: practice; type `%(prog)s {command} --help` for more information on a command"
    subparser_action = argument_parser.add_subparsers(
        dest="command",
        title="commands",
        help=command_help,
    )
    add_practice_command(subparser_action, config)
    add_progress_command(subparser_action, config)
    add_topics_command(subparser_action, config)
    if not {"practice", "progress", "topics", "-h", "--help", "-V", "--version"} & set(sys.argv):
        sys.argv.insert(1, "practice")  # Insert practice as default subcommand
    return argument_parser
