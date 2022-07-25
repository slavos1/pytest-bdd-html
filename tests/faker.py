"""
Customize faker.Faker
"""

from time import time

# import the "real" faker module
import faker as _faker  # pylint:disable=import-error
import pytest


class Faker(_faker.Faker):
    """Extended faker.Faker"""

    def sentence(self):
        """Shortcut generator for short text"""
        return self.paragraph(1)


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker instance fixture with randomized seed"""
    Faker.seed(time())
    return Faker()
