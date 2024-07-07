from pathlib import Path

import pytest
from bs4 import BeautifulSoup

import wikirefs


@pytest.fixture
def ref_sample_1():
    with Path(__file__).parent / "ref-sample-1.html" as datafile:
        return datafile.read_text()


def parse(text):
    return BeautifulSoup(text, features="lxml")


class TestParseParagraph:
    def test_no_text(self):
        p = parse("<p></p>")
        assert wikirefs.parse_paragraph(p) == []

    def test_one_statement(self):
        p = parse(
            """<p>statement.
            <sup id="cite_ref-1" class="reference">
            <a href="#cite_note-1">&#91;1&#93;</a>
            </sup> </p>"""
        )
        statements = wikirefs.parse_paragraph(p)
        assert statements == [wikirefs.Statement("statement.", ["1"])]
