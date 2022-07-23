from time import time

import pytest
from faker import Faker

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def _faker():
    Faker.seed(time())
    return Faker()
