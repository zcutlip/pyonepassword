import copy
from typing import List, Union

from ...py_op_exceptions import OPInvalidItemException
from ..field_registry import OPItemFieldFactory
from .item_field_base import OPItemField


class OPItemFieldCollisionException(Exception):
    pass


class OPSectionCollisionException(Exception):
    pass


class OPFieldNotFoundException(Exception):
    pass


class OPSection(dict):
    """
    Object type representing a section dictionary in a 1Password item
    """

    def __init__(self, section_dict):
        """
        Initialize an OPSection object

        Parameters
        ----------
        section_dict : Dict[str, Any]
            The section dictionary found inside an item dictionary
        """
        super().__init__(section_dict)
        # shadow fields map makes it easy to detect collisions
        # by looking up a field's ID to see if it's already been registered
        self._shadow_fields = {}

    @property
    def section_id(self) -> str:
        """
        Returns the section ID which may or may not be related to
        the user-visible label
        It may be a lower-case transformation, like 'additional passwords'
        Or it may be something completely opaque, like
        'Section_967FEBAC931841BCBD2DD7CFE0B8DC82'
        """

        return self["id"]

    @property
    def label(self) -> str:
        """
        Returns the 'name' of the section as seen in the 1Password UI
        """
        return self["label"]

    @property
    def fields(self) -> List[OPItemField]:
        """
        Property representing the list of OPItemField objects associated with this section

        Returns
        -------
        List[OPItemField]
            The list of field objects
        """
        field_list = self.setdefault("fields", [])
        return field_list

    def register_field(self, field_dict: Union[OPItemField, dict], relaxed_validation: bool = False):
        if isinstance(field_dict, OPItemField):
            # make a copy of the field so we don't end up with a circular reference
            field = copy.copy(field_dict)
        else:
            field = OPItemFieldFactory.item_field(field_dict)

        try:
            field_id = field.field_id
        except KeyError as e:
            # In theory there could be non-conformant data where
            # a field dictionary is missing an "ID" element
            # and we need to optionally be robust to that
            #
            # In practice this case should never occur
            # since the item object *should* raise an exception
            # before this method is ever called
            if not relaxed_validation:
                raise OPInvalidItemException(  # pragma: no coverage
                    f"Field has no ID {field.label}") from e
            else:
                # if relaxed validation is enabled, set field_id to empty string
                # since we have log below to handle that
                field_id = ""
        if field_id in self._shadow_fields:
            if not relaxed_validation:
                raise OPItemFieldCollisionException(
                    f"Field {field_id} already registered in section {self.section_id}")
            else:
                # for code coverage visibility
                pass
        else:
            self._shadow_fields[field_id] = field
        self.fields.append(field)

    def fields_by_label(self, label: str, case_sensitive: bool = True) -> List[OPItemField]:
        """
        Returns a list of one or more fields matching the given label

        Note: Field labels are not guaranteed to be unique, so more than one field may be returned
        Parameters
        ----------
        label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match field labels case-sensitively, by default True

        Returns
        -------
        List[OPItemField]
            The list of matching fields

        Raises
        ------
        OPFieldNotFoundException
            If no matching fields are found
        """
        matching_fields = []
        f: OPItemField
        for f in self.fields:
            f_label = f.label
            if not case_sensitive:
                f_label = f_label.lower()
                label = label.lower()
            if f_label == label:
                matching_fields.append(f)
        if not matching_fields:
            raise OPFieldNotFoundException(
                f"No fields found by label '{label}'")
        return matching_fields

    def first_field_by_label(self, label: str, case_sensitive: bool = True):
        """
        Convenience function to return the first matching field

        Note: field labels are not guaranteed to be unique, or in a particular order, so there may
        be more than one match, in which case the first is returned

        Parameters
        ----------
        label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match field labels case-insensitively, by default True

        Returns
        -------
        OPItemField
            The matching field
        Raises
        ------
        OPFieldNotFoundException
            If no matching fields are found
        """
        fields = self.fields_by_label(label, case_sensitive=case_sensitive)
        f = fields[0]
        return f
