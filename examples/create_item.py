import getpass

from pyonepassword import OP, OPCreateItemException
from pyonepassword import OPLoginItem


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OP(vault="Test Data", password=my_password)


def main():
    username = "testuer"
    password = "testpass"
    url = "https://example.website"
    item_name = "login 3"
    # newlogin = OPLoginItemTemplate(username, password, )

    # user-visible section title is required
    # section name (not user visible) is optional and will be randomly generated if not provided
    # section = newlogin.add_section("New Section")

    # field name is not user visible
    # field label is user visible
    # section.add_field("example field name", "example value", "string", "example field label")

    op = do_signin()
    try:
        result: OPLoginItem = op.create_login_item_(item_name, username, password, url=url, vault="Test Data 2", acknowledge_insecurity=True)
    except OPCreateItemException as e:
        print("create_item() failed")
        print(e.err_output)
        return e.returncode
    print("Created item:")
    print(f"Username: {result.username}")
    print(f"Password: {result.password}")
    print(f"Item UUID: {result.uuid}")


if __name__ == "__main__":
    exit(main())
