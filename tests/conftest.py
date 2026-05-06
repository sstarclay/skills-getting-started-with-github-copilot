import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as initial_activities


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(initial_activities)
    yield
    app.activities = copy.deepcopy(original)
