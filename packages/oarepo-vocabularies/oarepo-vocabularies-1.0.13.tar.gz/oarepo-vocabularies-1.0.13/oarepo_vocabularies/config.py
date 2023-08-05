from invenio_records_resources.services.custom_fields.text import KeywordCF

from oarepo_vocabularies.fixtures import (
    VocabularyReader,
    VocabularyWriter,
    vocabularies_generator,
)
from oarepo_vocabularies.services.custom_fields import hierarchy

OAREPO_VOCABULARIES_HIERARCHY_CF = [
    hierarchy.HierarchyLevelCF("level"),
    hierarchy.HierarchyTitleCF("title"),
    hierarchy.HierarchyAncestorsCF("ancestors", multiple=True),
    KeywordCF("parent"),
]


OAREPO_VOCABULARIES_CUSTOM_CF = []

DATASTREAMS_CONFIG_GENERATOR_VOCABULARIES = vocabularies_generator

DEFAULT_DATASTREAMS_READERS = {"vocabulary": VocabularyReader}

DEFAULT_DATASTREAMS_WRITERS = {"vocabulary": VocabularyWriter}
