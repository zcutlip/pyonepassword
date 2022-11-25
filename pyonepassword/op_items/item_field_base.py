from typing import Any, Union


class OPItemField(dict):
    FIELD_TYPE: Union[str, None] = None

    def __init__(self, field_dict):
        super().__init__(field_dict)

    @property
    def field_id(self) -> str:
        return self["id"]

    @property
    def label(self) -> str:
        """
        Returns the field label as assigned and seen in the 1Password UI
        """
        return self["label"]

    @property
    def value(self) -> Any:
        """
        Returns the field's value (password, URL, etc.) as assigned and seen in the 1Password UI,
        or None if the field lacks a value
        """
        v = self.get("value")
        return v

    @property
    def field_type(self) -> str:
        """
        Returns the field's type, which affects how the field's value is rendered in 1Password
        """
        return self["type"]

    @property
    def reference(self) -> Union[str, None]:
        return self.get("reference")

    @property
    def purpose(self) -> str:
        return self["purpose"]

    @property
    def entropy(self) -> Union[float, None]:
        return self.get("entropy")

    @property
    def section_id(self) -> Union[str, None]:
        section_id = None
        section = self.get("section")
        if section:
            section_id = section["id"]
        return section_id
