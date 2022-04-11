import datetime

from abc import ABCMeta, abstractmethod

from .._datetime import fromisoformat_z
from ._item_overview import OPItemOverview


class OPAbstractItemDescriptor(dict):
    __metaclass__ = ABCMeta
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        super().__init__(item_dict)
        self._from_template = False
        # not every item has an overview
        # in particular, items created from a template do not
        overview = self.get("overview", {})
        self._overview = OPItemOverview(overview)

    @property
    def uuid(self) -> str:
        return self["uuid"]

    @property
    def title(self) -> str:
        title = self._overview["title"]
        return title

    @property
    def created_at(self) -> datetime.datetime:
        created = self["createdAt"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self) -> datetime.datetime:
        updated = self["updatedAt"]
        updated = fromisoformat_z(updated)
        return updated

    @property
    def changer_uuid(self) -> str:
        return self["changerUuid"]

    @property
    def vault_uuid(self) -> str:
        return self["vaultUuid"]

    @property
    def trashed(self) -> bool:
        trashed: str = self["trashed"]
        if trashed.lower() == "y":
            trashed = True
        elif trashed.lower() == "n":
            trashed = False
        return trashed
