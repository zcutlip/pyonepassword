from _util.functions import get_op
from dotenv import load_dotenv

from pyonepassword.api.exceptions import OPCmdFailedException  # noqa: F401

load_dotenv("./dot_env_files/.env_pyonepassword_test_rw")

print("run: op = get_op(\"document-edit\")")

vault = "Test Data 2"
document_name = "no such document"
new_file_path = "working_data/images/replacement_image_10.png"
