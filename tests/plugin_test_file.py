"""
Testing of plugin itself
"""
from typing import Any

from lxml.etree import _Element  # pylint:disable=import-error

from pytest_bdd_html.plugin import NO_DESCRIPTION, CssClasses

from .faker import Faker
from .feature import FeatureFile


class PluginTestFile:
    """
    Test file used to test the plugin itself
    """

    def __init__(self, pytester: Any, faker: Faker) -> None:
        self.feature_file = FeatureFile(pytester.mkdir("features"), faker)
        self.non_bdd_test_description = faker.sentence()
        pytester.makepyfile(
            test_foo=f"""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('{self.feature_file.root}')

def test_not_bdd_test():
    '''{self.non_bdd_test_description}'''
    pass

def test_not_bdd_test_without_description():
    pass

# generate dummy fixtures just not to pollute the tets report

@given(parsers.re(".+"))
def _given_any():
    pass

@when(parsers.re(".+"))
def _when_any():
    pass

@then(parsers.re(".+"))
def _then_any():
    pass
"""
        )
        # one in features_root + test_not_bdd_test + test_not_bdd_test_without_description
        self.number_of_tests = 3

    def validate(self, cell: _Element, text: str) -> None:
        """
        Ensure all cells in the plugin-generated column are as expected
        """
        if cell.get("class") == CssClasses.NON_BDD.value:
            assert text == self.non_bdd_test_description
        elif cell.get("class") == CssClasses.MISSING.value:
            assert text == NO_DESCRIPTION
        else:
            self.feature_file.validate(text)
