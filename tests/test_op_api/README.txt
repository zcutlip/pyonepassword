Test modules in this directory are intended to test API exported by the pyonepassword.OP class. Also, only tests that require a call to the 'op' CLI executable should go here.

EXAMPLES:

Testing the OPLoginItem class should not go here. It can be performed with only test input data and expected data. No call to OP.item_get() is required.

Testing OP.item_get_totp() should go here because it requires passing the argument '--fields type=otp' to the 'op' CLI executable.
