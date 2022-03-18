import datetime

from abc import ABC, abstractmethod

from .._datetime import fromisoformat_z


class OPAbstractItemDescriptor(ABC):
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        self._from_template = False
        self._item_dict = item_dict

    @property
    def uuid(self) -> str:
        return self._item_dict["uuid"]

    @property
    def title(self) -> str:
        title = self._overview["title"]
        return title

    @property
    def created_at(self) -> datetime.datetime:
        created = self._item_dict["createdAt"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self) -> datetime.datetime:
        updated = self._item_dict["updatedAt"]
        updated = fromisoformat_z(updated)
        return updated

    @property
    def changer_uuid(self) -> str:
        return self._item_dict["changerUuid"]

    @property
    def vault_uuid(self) -> str:
        return self._item_dict["vaultUuid"]

    @property
    def trashed(self) -> bool:
        trashed: str = self._item_dict["trashed"]
        if trashed.lower() == "y":
            trashed = True
        elif trashed.lower() == "n":
            trashed = False
        return trashed
