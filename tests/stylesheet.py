"""
Create and match CSS stylesheet in test report
"""
import re
from pathlib import Path
from typing import Optional

from typing_extensions import Self

from pytest_bdd_html.plugin import BDD_HTML_CSS_DEFAULT


class Stylesheet:
    """CSS stylesheet for testing"""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path
        self.expected_pattern = self.path.name if self.path else None

    def write(self) -> Self:
        """Write stylesheet into file"""
        assert self.path
        self.path.open("w").write(f"""/* {self.expected_pattern} */""")
        return self

    def format_option(self) -> str:
        """ "Format CLI option for stylesheet"""
        return f"--bdd-html-css={self.path}" if self.path else ""

    def is_in_text(self, text) -> bool:
        """Either default CSS was used or the one we wrote via self.write"""
        if not self.path or not self.path.exists():
            # we expect the default stylesheet is used
            return str(BDD_HTML_CSS_DEFAULT) in text
        return bool(re.search(rf"\b{self.expected_pattern}\b", text))
