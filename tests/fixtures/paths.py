from pathlib import Path

TEST_DATA_PATH = Path("tests", "data")
TEST_INPUT_DATA_PATH = Path(TEST_DATA_PATH, "test-input-data")
TEST_CONFIG_PATH = Path("tests", "config")

MOCK_OP_CONFIG_PATH = Path(TEST_CONFIG_PATH, "mock-op")
RESP_DIRECTORY_PATH = Path(MOCK_OP_CONFIG_PATH, "response-directory.json")
ALT_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "alternate-response-directory.json")

ITEM_DELETE_MULTIPLE_RESP_PATH = Path(
    MOCK_OP_CONFIG_PATH, "responses-item-delete-multiple")
ITEM_DELETE_MULTIPLE_STATE_CONFIG_PATH = Path(
    ITEM_DELETE_MULTIPLE_RESP_PATH, "mock-op-state-config-1.json")
ITEM_DELETE_MULTIPLE_TITLE_GLOB_STATE_CONFIG_PATH = Path(
    ITEM_DELETE_MULTIPLE_RESP_PATH, "mock-op-state-config-2.json")

UNAUTH_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "unauth-response-directory.json")

SVC_ACCT_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "svc-acct-response-directory.json"
)
SVC_ACCT_CORRUPT_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "svc-acct-corrupt-response-directory.json"
)
SVC_ACCT_REVOKED_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "svc-acct-revoked-token-directory.json"
)

VALID_DATA_REGISTRY_PATH = Path(
    TEST_INPUT_DATA_PATH, "valid-data-registry.json")
VALID_DATA_PATH = Path(TEST_INPUT_DATA_PATH, "valid-data")
INVALID_DATA_REGISTRY_PATH = Path(
    TEST_INPUT_DATA_PATH, "invalid-data-registry.json")
INVALID_DATA_PATH = Path(TEST_INPUT_DATA_PATH, "invalid-data")
NON_CONFORMANT_REGISTRY_PATH = Path(
    TEST_INPUT_DATA_PATH, "non-conformant-data-registry.json")
NON_CONFORMANT_DATA_PATH = Path(TEST_INPUT_DATA_PATH, "non-conformant-data")
EXPECTED_DATA_REGISTRY_PATH = Path(
    TEST_DATA_PATH, "expected-data-registry.json")
EXPECTED_DATA_PATH = Path(TEST_DATA_PATH, "expected-data")
