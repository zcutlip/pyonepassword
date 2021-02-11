from pathlib import Path

TEST_DATA_PATH = Path("tests", "data")
TEST_CONFIG_PATH = Path("tests", "config")

EXPECTED_DATA_PATH = Path(TEST_DATA_PATH, "expected-data.json")
MOCK_OP_CONFIG_PATH = Path(TEST_CONFIG_PATH, "mock-op")
RESP_DIRECTORY_PATH = Path(MOCK_OP_CONFIG_PATH, "response-directory.json")
