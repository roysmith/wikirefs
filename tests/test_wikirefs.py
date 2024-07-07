from pathlib import Path
from textwrap import dedent

from lxml import etree
import pytest
from bs4 import BeautifulSoup

import wikirefs


@pytest.fixture
def ref_sample_1():
    with Path(__file__).parent / "ref-sample-1.html" as datafile:
        return datafile.read_text()


class TestParseParagraph:
    def test_no_text(self):
        p = BeautifulSoup("<p></p>")
        assert wikirefs.parse_paragraph(p) == []

    def test_one_statement(self):
        p = BeautifulSoup(
            """<p>statement.
            <sup id="cite_ref-1" class="reference">
            <a href="#cite_note-1">&#91;1&#93;</a>
            </sup> </p>"""
        )
        statements = wikirefs.parse_paragraph(p)
        assert statements == [wikirefs.Statement("statement.", ["1"])]
