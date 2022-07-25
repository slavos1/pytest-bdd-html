"""
Implementation of the plugin
"""
from enum import Enum, unique
from logging import getLogger
from pathlib import Path
from typing import Iterable, Optional

import pytest
from py.xml import Tag, html  # pylint:disable=import-error,no-name-in-module
from pytest_bdd.parser import Step

PLUGIN_NAME = "bdd-html"
DESCRIPTION_COLUMN_INDEX = 2
DESCRIPTION_COLUMN_LABEL = "Description"
STEP_AND = "And"
THIS_DIR = Path(__file__).parent
BDD_HTML_CSS_OPTION = f"--{PLUGIN_NAME}-css"
BDD_HTML_CSS_DEFAULT = THIS_DIR / "resources" / "style.css"
NO_DESCRIPTION = ""

logger = getLogger(__name__)


@unique
class CssClasses(Enum):
    """CSS classes used in pytest-html-generated HTML report"""

    CELL = "col-description"
    BDD = "col-description-bdd-doc"
    NON_BDD = "col-description-func-doc"
    MISSING = "col-description-no-doc"


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add this plugin's command line options (in {PLUGIN_NAME} group)
    """
    group = parser.getgroup(
        PLUGIN_NAME, f"{PLUGIN_NAME}: add BDD scenario descriptions to HTML report"
    )
    group.addoption(
        BDD_HTML_CSS_OPTION,
        default=BDD_HTML_CSS_DEFAULT,
        type=Path,
        help="CSS style sheet used to style the Description column "
        f"(default: {BDD_HTML_CSS_DEFAULT})",
    )


def pytest_configure(config):
    """Add this plugin's CSS to pytest-html's --css option (which is an array)"""
    try:
        css: Path = config.getoption(BDD_HTML_CSS_OPTION)
        if not css.exists():
            css = BDD_HTML_CSS_DEFAULT
        config.option.css.append(css)
    except:  # pylint:disable=bare-except
        pass


def pytest_bdd_before_scenario(request, feature, scenario):
    """Hooking into pytest-bdd-defined hooks to capture feature name and scenario + its steps"""
    item = request.node
    item.user_properties.extend(
        [
            ("feature", dict(name=feature.name, description=feature.description)),
            ("scenario", dict(name=scenario.name, steps=scenario.steps)),
        ]
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint:disable=unused-argument
    """Save test feature/function documentation for later use in HTML report"""
    outcome = yield
    report = outcome.get_result()
    meta = dict(item.user_properties)
    if func_doc := item.function.__doc__:
        func_doc = func_doc.splitlines()[0]
    report.description = dict(doc=func_doc or NO_DESCRIPTION)
    if "feature" in meta:
        report.description.update(feature=meta["feature"], scenario=meta["scenario"])


def pytest_html_results_table_header(cells):
    """Create table header column for the plugin data"""
    # insert after Result, Test columns
    cells.insert(DESCRIPTION_COLUMN_INDEX, html.th(DESCRIPTION_COLUMN_LABEL))


def _bdd_div(title, *children):
    return html.div(
        html.h3(title),
        html.div(
            *children,
            Class="text",
        ),
    )


def _format_step(step: Step, prev: Optional[Step]) -> Tag:
    step_name = step.type.capitalize()
    if prev and prev.type.capitalize() == step_name:
        step_name = STEP_AND
    return html.div(
        html.span(step_name, Class=f"step-name {'step-is-and' if step_name == STEP_AND else ''}"),
        html.span(step.name, Class="step-message"),
        Class="step",
    )


def _format_steps(steps: Iterable[Step]) -> Iterable[Tag]:
    prev = None
    for step in steps:
        yield _format_step(step, prev)
        prev = step


def pytest_html_results_table_row(report, cells):
    """Create table body column for the plugin data"""
    logger.debug("start=%r", report)
    if not hasattr(report, "description"):
        # pytest_runtest_makereport has not run and this is in case of a serious run error,
        # say, when a marker is not defined in tox.ini
        return
    if "feature" in report.description:
        # we report on a BDD scenario
        description = html.div(
            *[
                _bdd_div(*args)
                for args in (
                    (
                        "Feature",
                        html.div(report.description["feature"]["name"]),
                        html.div(report.description["feature"]["description"]),
                    ),
                    ("Scenario", report.description["scenario"]["name"]),
                )
            ],
            html.div(
                html.h3("Steps"),
                html.div(
                    list(_format_steps(report.description["scenario"]["steps"])),
                    Class="steps",
                ),
            ),
            Class=CssClasses.BDD.value,
        )
    else:
        # show some sensible description for non-BDD tests
        func_doc = report.description["doc"]
        description = html.div(
            func_doc,
            Class=CssClasses.NON_BDD.value
            if func_doc != NO_DESCRIPTION
            else CssClasses.MISSING.value,
        )
        logger.debug("func_doc=%r, description=%r", func_doc, description)
    cells.insert(DESCRIPTION_COLUMN_INDEX, html.td(description, Class=CssClasses.CELL.value))
