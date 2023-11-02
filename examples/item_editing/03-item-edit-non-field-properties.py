from pyonepassword import OP


def edit_non_field_properites(op: OP):
    """
    You can edit/set the following non-field properties:
    - favorite (set/unset)
    - tags (You can set, remove, or add to an item's et of tags)
    - autofill URL property for Login items (this does not set URLs on arbitrary fields)
    - generate new password for Login or Password items (this does not generate passwords for arbitrary fields)
    """

    item = "Example Login Item 104"
    new_item_label = "New Login Item 104"
    favorite = True
    tags = ["tag_1", "tag_2"]
    autofill_url = "https://new-url/login.html"
    vault = "Test Data 2"

    # Toggle item favorite flag
    op.item_edit_favorite(item,
                          favorite,
                          vault=vault)

    # Set or replace item's list of tags
    op.item_edit_tags(item,
                      tags,
                      append_tags=False,
                      vault=vault)

    # for Login items, set the website/URL property
    op.item_edit_url(item,
                     autofill_url,
                     vault=vault)

    # set new item titel
    op.item_edit_title(item,
                       new_item_label,
                       vault=vault)


if __name__ == "__main__":
    # see README.md for sign-in process
    op: OP = OP()
    edit_non_field_properites(op)
