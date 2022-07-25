"""
HTML report parsing and validation
"""
from pathlib import Path
from typing import List

from lxml import html  # pylint:disable=import-error
from lxml.etree import _Element  # pylint:disable=import-error

from pytest_bdd_html.plugin import DESCRIPTION_COLUMN_INDEX, DESCRIPTION_COLUMN_LABEL, CssClasses

from .plugin_test_file import PluginTestFile
from .stylesheet import Stylesheet


def get_node_text(element: _Element) -> str:
    """Get all HTML element's text"""
    return "".join(element.xpath(".//text()"))


class HtmlReport:
    """ "Representing HTML report and assertions on it"""

    def __init__(self, path: Path) -> None:
        self.html = html.parse(path)

    def validate(
        self,
        test_file: PluginTestFile,
        stylesheet: Stylesheet,
    ) -> None:
        """
        Check that HTML report contains BDD info and styles from bdd-html plugin
        """
        css_style_in_report = get_node_text(self.html.xpath("//head/style")[0])
        assert stylesheet.is_in_text(css_style_in_report)
        try:
            results_table: _Element = list(self.html.xpath('//table[@id="results-table"]'))[0]
        except AssertionError as exc:
            raise ValueError(
                "pytest-html plugin must be enabled, check if you have '-p no:html'"
            ) from exc
        description_column = list(
            results_table.xpath(f"thead/tr[1]/th[{DESCRIPTION_COLUMN_INDEX + 1}]/text()")
        )
        assert description_column and description_column[0] == DESCRIPTION_COLUMN_LABEL
        rows: List[_Element] = list(
            results_table.xpath(f'tbody/tr[1]/td[@class="{CssClasses.CELL.value}"]/div[1]')
        )
        # we have 3 tests in test_foo in test_plugin, expect 3 rows in the report
        assert len(rows) == test_file.number_of_tests
        for cell in rows:
            test_file.validate(cell, get_node_text(cell).strip())
