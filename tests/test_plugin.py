"""Test the plugin itself"""
from .faker import Faker
from .html_report import HtmlReport
from .plugin_test_file import PluginTestFile
from .stylesheet import Stylesheet


def test_plugin(pytester, faker: Faker, stylesheet: Stylesheet):
    """
    Check if BDD feature text is rendered in HTML report

    The BDD fixtures given/when/then are defined as stubs since we do not need to do real tests;
    we are merely testing rendering of the HTML report.
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
    test_file = PluginTestFile(pytester, faker)
    pytester.runpytest(
        *(
            f"""
-p bdd-html
-q -s -vv
--log-level=DEBUG
--html={test_report}
--self-contained-html
--random-order
{stylesheet.format_option()}
""".split()
        )
    )
    HtmlReport(test_report).validate(test_file, stylesheet)
