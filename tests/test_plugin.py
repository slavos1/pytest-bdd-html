from pathlib import Path

from lxml import html
from lxml.etree import Element

from pytest_bdd_html.plugin import DESCRIPTION_COLUMN_INDEX, NO_DESCRIPTION, CssClasses


def get_node_text(element: Element) -> str:
    return "".join(element.xpath(".//text()"))


def test_plugin(pytester, _faker):
    """
    We do not bother really do BDD -- we want to check if we have feature rendered in HTML report
    """
    test_report = pytester.makefile(".html", "")
    pytester.makeconftest(
        """
from logging import getLogger

def pytest_configure(config):
    # switch off noisy loggers
    getLogger("faker.factory").disabled = True
"""
    )
    features: Path = pytester.mkdir("features")
    feature: Path = features.joinpath("baz.feature")
    non_bdd_test_description = _faker.paragraph(1)
    feature.open("w").write(
        """
Feature: A nice feature
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
    And I will be happy

"""
    )
    pytester.makepyfile(
        test_foo=f"""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('{features}')

def test_not_bdd_test():
    '''{non_bdd_test_description}'''
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
    pytest_args = f"""
-p bdd-html
-q -s
--log-level=DEBUG
--html={test_report}
--self-contained-html
--random-order
--random-order-bucket=global
""".split()
    result = pytester.runpytest(*pytest_args)
    parsed_html = html.parse(test_report.open())
    try:
        results_table = list(parsed_html.xpath('//table[@id="results-table"]'))
    except AssertionError as exc:
        raise ValueError(
            "pytest-html plugin must be enabled, check if you have '-p no:html'"
        ) from exc
    assert len(results_table)
    results_table = results_table[0]
    description_column = list(
        results_table.xpath(f"thead/tr[1]/th[{DESCRIPTION_COLUMN_INDEX + 1}]/text()")
    )
    assert description_column and description_column[0] == "Description"
    cell_class = CssClasses.CELL.value
    rows = list(results_table.xpath(f'tbody/tr[1]/td[@class="{cell_class}"]/div[1]'))
    # we have 3 tests, expect 3 rows in the report
    assert len(rows) == 3
    for cell in rows:
        text = get_node_text(cell).strip()
        if cell.get("class") == CssClasses.NON_BDD.value:
            assert text == non_bdd_test_description
        elif cell.get("class") == CssClasses.MISSING.value:
            assert text == NO_DESCRIPTION
        else:
            # XXX we assume a BDD test
            assert "Feature" in text
