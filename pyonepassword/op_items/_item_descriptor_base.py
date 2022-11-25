import datetime
from abc import ABCMeta, abstractmethod
from typing import Optional

from .._datetime import fromisoformat_z
from ..json import safe_unjson
from ..op_objects import OPVaultDescriptor


class OPAbstractItemDescriptor(dict):
    __metaclass__ = ABCMeta
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict_or_json):
        item_dict = safe_unjson(item_dict_or_json)
        super().__init__(item_dict)
        vault_dict = self.get("vault")
        if vault_dict:
            self._vault = OPVaultDescriptor(vault_dict)
        else:
            self._vault = None

    @property
    def vault(self) -> OPVaultDescriptor:
        return self._vault

    @property
    def unique_id(self) -> str:
        return self["id"]

    @property
    def title(self) -> str:
        title = self["title"]
        return title

    @property
    def created_at(self) -> datetime.datetime:
        created = self["created_at"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self) -> datetime.datetime:
        updated = self["updated_at"]
        updated = fromisoformat_z(updated)
        return updated

    @property
    def last_edited_by(self) -> str:
        return self["last_edited_by"]

    @property
    def vault_id(self) -> str:
        return self.vault.unique_id

    @property
    def state(self) -> Optional[str]:
        return self.get("state")

    @property
    def archived(self) -> bool:
        return self.state == "ARCHIVED"

    @property
    def favorite(self) -> Optional[bool]:
        fav = self.get("favorite", False)
        return fav

    @property
    def version(self) -> int:
        return self["version"]

    @property
    def category(self) -> str:
        return self["category"]
