from typing import Any, Union


class OPItemField(dict):
    """
    Object type representing a field dictionary in a 1Password item
    """
    FIELD_TYPE: Union[str, None] = None

    def __init__(self, field_dict):
        """
        Initialize an OPItemField object

        Parameters
        ----------
        field_dict : Dict[str, Any]
            The field dictionary found inside an item dictionary
        """
        super().__init__(field_dict)

    @property
    def field_id(self) -> str:
        """
        Property corresponding the the "id" element of a field object.
        This is the unique (within a given item object) identifier of the field, and not
        the user-visible label

        Returns
        -------
        str
            The unique Field ID string
        """
        return self["id"]

    @property
    def label(self) -> str:
        """
        Property corresponding to the "label" element of a field object.
        This is the field label as assigned and seen in the 1Password UI

        Returns
        -------
        str
            The label string
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
        """
        Property corresponding to the "reference" element of a field object.
        This is the 'op://' URI allowing this field to be referenced directly by 'op'

        Returns
        -------
        Union[str, None]
            The reference URI string
        """
        return self.get("reference")

    @property
    def purpose(self) -> str:
        """
        Property corresponding to the "purpose" element of a field object.
        This value identifies the type of field, e.g., "PASSWORD," or "USERNAME"

        Returns
        -------
        str
            The purpose string
        """
        return self["purpose"]

    @property
    def entropy(self) -> Union[float, None]:
        """
        Property corresponding to the "entropy" element of a field object
        This is typicaly associated with password field types

        Returns
        -------
        Union[float, None]
            The entropy value
        """
        return self.get("entropy")

    @property
    def section_id(self) -> Union[str, None]:
        """
        The unique identifier of the section this field is associated with, if any

        Returns
        -------
        Union[str, None]
            The section ID
        """
        section_id = None
        section = self.get("section")
        if section:
            section_id = section["id"]
        return section_id
