from ._op_items_base import OPAbstractItem


class _OPGenericItem(OPAbstractItem):  # pragma: no coverage
    """
    Generic item class

    This is a bit of a hack for instances when we need to 'item_get()' an item for which we
    don't have specific class in op_items, such as OPLoginItem etc.

    In those cases, OPItemFactory.op_item() will blow up when it encounters unknown item types

    But in some cases we need an item object so we can access basic things common to all item types.

    E.g., we need to access item.unique_id in order to resolve an item's title to its ID
    """

    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
