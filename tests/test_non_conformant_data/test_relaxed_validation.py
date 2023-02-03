from pyonepassword.op_items._op_item_type_registry import OPItemFactory


def test_relaxed_validation_items_registered_01():
    """
    Verify that all item types registered with OPItemFactory also have a relaxed validation variant
    """
    missing_item_types = []
    for item_type in OPItemFactory._TYPE_REGISTRY.keys():
        if item_type not in OPItemFactory._RELAXED_TYPE_REGISTRY:
            missing_item_types.append(item_type)

    assert len(
        missing_item_types) == 0, f"Missing relaxed validation item types: {missing_item_types}"
