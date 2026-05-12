import pytest
import requests

BASE_URL = "http://juice-shop.herokuapp.com"

def pytest_configure(config):
    config._metadata = {
        "Project": "Security Testing Automation Suite",
        "Target": BASE_URL,
        "Tester": "VladimirRamirez07",
    }

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"User-Agent": "SecurityTestSuite/1.0"})
    return s