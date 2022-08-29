from pathlib import Path

TEST_DATA_PATH = Path("tests", "data")
TEST_CONFIG_PATH = Path("tests", "config")

MOCK_OP_CONFIG_PATH = Path(TEST_CONFIG_PATH, "mock-op")
RESP_DIRECTORY_PATH = Path(MOCK_OP_CONFIG_PATH, "response-directory.json")
ALT_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "alternate-response-directory.json")
UNAUTH_RESP_DIRECTORY_PATH = Path(
    MOCK_OP_CONFIG_PATH, "unauth-response-directory.json")
VALID_DATA_REGISTRY_PATH = Path(TEST_DATA_PATH, "valid-data-registry.json")
VALID_DATA_PATH = Path(TEST_DATA_PATH, "valid-data")
INVALID_DATA_REGISTRY_PATH = Path(TEST_DATA_PATH, "invalid-data-registry.json")
INVALID_DATA_PATH = Path(TEST_DATA_PATH, "invalid-data")
EXPECTED_DATA_REGISTRY_PATH = Path(
    TEST_DATA_PATH, "expected-data-registry.json")
EXPECTED_DATA_PATH = Path(TEST_DATA_PATH, "expected-data")
