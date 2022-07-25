"""
BDD feature file for plugin testing
"""
import re
from pathlib import Path

from .faker import Faker


class FeatureFile:
    """
    BDD feature file for plugin testing
    """

    def __init__(self, features_root: Path, faker: Faker) -> None:
        self.name = faker.sentence()
        self.expected_then = faker.sentence()
        self.root = features_root
        self.root.joinpath("baz.feature").open("w").write(
            f"""
Feature: {self.name}
    As a user, I want to cook and be happy

Scenario: Making a butter toast
    Given a slice of bread
    And butter
    And a toaster
    And a knife
    When I toast the slice
    And smother it with butter
    Given forgot something
    Then I will have a tasty toast
    And {self.expected_then}

"""
        )

    def validate(self, text: str) -> None:
        """
        Ensure text contains BDD feature/scenario/steps info
        """
        # TODO test in more detail
        assert all(re.search(rf"\b{t}\b", text) for t in ("Feature", "Scenario", "Steps"))
        assert self.name in text
        assert self.expected_then in text
