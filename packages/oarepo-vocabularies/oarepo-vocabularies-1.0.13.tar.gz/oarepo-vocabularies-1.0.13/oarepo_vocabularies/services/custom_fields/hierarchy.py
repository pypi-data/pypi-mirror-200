from invenio_records_resources.services.custom_fields.base import BaseCF
from invenio_records_resources.services.custom_fields.number import IntegerCF
from invenio_records_resources.services.custom_fields.text import KeywordCF
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import fields as ma_fields


class HierarchyCF:
    def update(self, record, parent):
        pass


class HierarchyLevelCF(HierarchyCF, IntegerCF):
    def update(self, record, parent):
        record.hierarchy["level"] = (parent["hierarchy"]["level"] + 1) if parent else 1


class HierarchyTitleCF(HierarchyCF, BaseCF):
    def update(self, record, parent):
        titles = [record["title"]]
        if parent:
            titles.extend(parent["hierarchy"]["title"])
        record.hierarchy["title"] = titles

    @property
    def mapping(self):
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        return ma_fields.List(i18n_strings)


class HierarchyAncestorsCF(HierarchyCF, KeywordCF):
    def update(self, record, parent):
        if parent:
            record.hierarchy["ancestors"] = [
                parent["id"],
                *parent["hierarchy"]["ancestors"],
            ]
        else:
            record.hierarchy["ancestors"] = []
