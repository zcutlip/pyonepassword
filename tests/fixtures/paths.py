from pathlib import Path

TEST_DATA_PATH = Path("tests", "data")
TEST_INPUT_DATA_PATH = Path(TEST_DATA_PATH, "test-input-data")
TEST_CONFIG_PATH = Path("tests", "config")

MOCK_OP_CONFIG_PATH = Path(TEST_CONFIG_PATH, "mock-op")
RESP_DIRECTORY_PATH = Path(MOCK_OP_CONFIG_PATH, "response-directory.json")
ALT_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "alternate-response-directory.json")
UNAUTH_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "unauth-response-directory.json")
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

EXPECTED_ITEM_LIST_DATA_REGISTRY_PATH = Path(
    EXPECTED_DATA_PATH, "expected-item-list-data.json")
EXPECTED_ITEM_LIST_DATA_PATH = Path(
    EXPECTED_DATA_PATH, "expected-item-list-data")
