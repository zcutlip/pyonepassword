from typing import Set

"""
Module for classes & functions related to item valiation policy.

In some cases `op` may return item JSON that is not strictly conforming.
Examples include fields with empty-string IDs, duplicate sections, and
other anomalies.

In this case we have no control of the anomalous data, so we must relax validation
in order to instantiate useful item objects without raising exceptions

This module provides mechanisms to enable/disable relaxed validation globaly, or on a
per-class basis
"""


class _OPItemValidationPolicy:
    """
    Class representing the active policy whether a 1Password item object should
    enforce strict validation policy when processing a dictionary from JSON
    """
    _relaxed_item_classes: Set[type] = set()
    _relaxed_validation: bool = False

    @classmethod
    def _enable_relaxed_validation(cls) -> None:
        """
        Enable relaxed validation policy globally
        """
        cls._relaxed_validation = True

    @classmethod
    def _disable_relaxed_validation(cls) -> None:
        """
        Disable relaxe validation policy globally

        Per-class relaxed validation will still apply
        """
        cls._relaxed_validation = False

    @classmethod
    def _get_relaxed_validation(cls, item_class: type = None) -> bool:
        """
        Get the validation policy taking into a account global policy and optionally 'item_class':
            True if either is true

        Note: if item_class is not provided, then only global validation policy is consulted

        Parameters
        ----------
        item_class : type, optional
            Any OPAbstractItem class, by default None

        Returns
        -------
        bool
            Whether the relaxed validation policy is enabled
        """
        global_relaxed = cls._relaxed_validation

        class_relaxed = cls._get_relaxed_validation_for_class(item_class)

        # Union of global and class policy
        relaxed = global_relaxed or class_relaxed

        return relaxed

    @classmethod
    def _get_relaxed_validation_for_class(cls, item_class: type) -> bool:
        """
        Get the validation policy only for 'item_class'

        Parameters
        ----------
        item_class : type
            Any OPAbstractItem class

        Returns
        -------
        bool
            Whether relaxed validation is set for 'item_class'
        """
        relaxed = False
        # is obj_or_class, one of the classes (or a subclass of)
        # for which validation is relaxed?
        if issubclass(item_class, tuple(cls._relaxed_item_classes)):
            relaxed = True
        return relaxed

    @classmethod
    def _set_relaxed_validation_for_class(cls, item_class) -> None:
        """
        Enable relaxed validation policy for 'item_class'

        Parameters
        ----------
        item_class : type
            Any OPAbstractItem class
        """
        cls._relaxed_item_classes.add(item_class)

    @classmethod
    def _set_strict_validation_for_class(cls, item_class) -> None:
        """
        Disable relaxed validation policy for 'item_class'

        Parameters
        ----------
        item_class : type
            Any OPAbstractItem class
        """
        if item_class in cls._relaxed_item_classes:
            cls._relaxed_item_classes.remove(item_class)


def enable_relaxed_validation() -> None:
    """
    Convenience method to enable relaxed validation policy globally
    """
    _OPItemValidationPolicy._enable_relaxed_validation()


def disable_relaxed_validation() -> None:
    """
    Convenience method to disable relaxed validation policy globally.

    Per-class relaxed validation policy still applies
    """
    _OPItemValidationPolicy._disable_relaxed_validation()


def get_relaxed_validation(item_class=None) -> bool:
    """
    Get relaxed validation policy.

    If optional 'item_class' is provided, the returned value represents the union of global
    item validation policy, and the class-specific item validation policy.

    This is to say True is returned if either is true

    Parameters
    ----------
    item_class : type, optional
        Any OPAbstractItem class, by default None

    Returns
    -------
    bool
        The union of the global item validation policy and the class's item validation policy
    """
    return _OPItemValidationPolicy._get_relaxed_validation(item_class=item_class)


def get_relaxed_validation_for_class(item_class) -> bool:
    """
    Get item validation policy for a specific op item class

    Parameters
    ----------
    item_class : type
        Any OPAbstractItem class

    Returns
    -------
    bool
        True of relaxed validation policy is set for this class
    """
    return _OPItemValidationPolicy._get_relaxed_validation_for_class(item_class)


def set_relaxed_validation_for_class(item_class) -> None:
    """
    Set item validation policy for the specified op item class

    Parameters
    ----------
    item_class : type
        Any OPAbstractItem class
    """
    _OPItemValidationPolicy._set_relaxed_validation_for_class(item_class)


def set_strict_validation_for_class(item_class) -> None:
    """
    Remove the specified op item class from the relaxed validation list

    Note: relaxed validation may still occur if it has been set globally

    Parameters
    ----------
    item_class : type
        Any OPAbstractItem class
    """
    _OPItemValidationPolicy._set_strict_validation_for_class(item_class)
