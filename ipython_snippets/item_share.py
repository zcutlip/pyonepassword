import os

from _util.functions import get_op
from dotenv import load_dotenv

from pyonepassword import OP
from pyonepassword.api.exceptions import OPCmdFailedException  # noqa: F401

os.environ["LOG_OP_ERR"] = "1"
# load_dotenv("./dot_env_files/.env_pyonepassword_test_rw")


item_name = "Example Login Item 22"
vault = "Test Data 1"
emails = "junkmael99@icloud.com"
op = OP()
print(open(__file__, "r").read())
