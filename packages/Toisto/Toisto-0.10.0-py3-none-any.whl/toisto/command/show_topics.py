"""Command to show concepts."""

from itertools import chain

from rich.table import Table

from toisto.model.language import Language
from toisto.model.language.iana_language_subtag_registry import ALL_LANGUAGES
from toisto.model.language.label import Labels
from toisto.model.quiz.topic import Topic, Topics
from toisto.ui.text import console


def enumerate_labels(labels: Labels) -> str:
    """Enumerate the labels."""
    return "\n".join(chain.from_iterable(label.spelling_alternatives for label in labels))


def topic_table(target_language: Language, source_language: Language, topic: Topic) -> Table:
    """Show the concepts of the topic."""
    table = Table(title=f"Topic {topic.name}")
    target_language_name, source_language_name = ALL_LANGUAGES[target_language], ALL_LANGUAGES[source_language]
    for column in (target_language_name, source_language_name, "Grammatical categories", "Language level"):
        table.add_column(column)
    for concept in topic.concepts:
        for leaf_concept in concept.leaf_concepts():
            target_labels = leaf_concept.labels(target_language)
            source_labels = leaf_concept.labels(source_language)
            if target_labels or source_labels:
                table.add_row(
                    enumerate_labels(target_labels),
                    enumerate_labels(source_labels),
                    "/".join(leaf_concept.grammatical_categories()),
                    leaf_concept.level,
                )
        table.add_section()
    return table


def show_topics(language: Language, source_language: Language, topics: Topics) -> None:
    """Show the concepts of the topics."""
    with console.pager():
        for topic in topics:
            console.print(topic_table(language, source_language, topic))
