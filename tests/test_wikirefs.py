from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from wikirefs import get_statements, get_paragraph_statements, Citation, Statement


def parse(text):
    return BeautifulSoup(text, features="lxml")


class TestCitation:
    @pytest.mark.parametrize(
        "id_string, expected",
        [
            ("cite_ref-1", Citation("cite_ref-1", "1")),
            ("cite_ref-:foo_1-0", Citation("cite_ref-:foo_1-0", "1", "foo", "0")),
            ("cite_ref-:foo_1-2", Citation("cite_ref-:foo_1-2", "1", "foo", "2")),
            ("cite_ref-:0_1-2", Citation("cite_ref-:0_1-2", "1", "0", "2")),
        ],
    )
    def test_from_id(self, id_string, expected):
        citation = Citation.from_id(id_string)
        assert citation == expected

    @pytest.mark.parametrize(
        "id_string",
        [
            (""),
            ("1"),
            ("foo"),
        ],
    )
    def test_from_id_parse_failure(self, id_string):
        with pytest.raises(ValueError, match="cannot parse ref_id"):
            Citation.from_id(id_string)

    @pytest.mark.parametrize(
        "citation, expected",
        [
            (Citation("", "", suffix=None), ""),
            (Citation("", "", suffix="0"), "a"),
            (Citation("", "", suffix="1"), "b"),
            (Citation("", "", suffix="25"), "z"),
            (Citation("", "", suffix="26"), "aa"),
            (Citation("", "", suffix="27"), "ab"),
            (Citation("", "", suffix="52"), "ba"),
            (Citation("", "", suffix="53"), "bb"),
        ],
    )
    def test_rendered_suffix(self, citation, expected):
        rendered = citation.rendered_suffix()
        assert rendered == expected

    @pytest.mark.parametrize(
        "n, expected_string",
        [
            (1, "a"),
            (2, "b"),
            (26, "z"),
            (27, "aa"),
        ],
    )
    def test_bijectiveHexavigesimal(self, n, expected_string):
        assert Citation.bijectiveHexavigesimal(n) == expected_string


class TestGetParagraphStatements:
    def test_no_text(self):
        p = parse("<p></p>")
        assert list(get_paragraph_statements(p)) == []

    def test_one_statement(self):
        p = parse(
            """
            <p>statement.
                <sup id="cite_ref-1" class="reference"><a href="#cite_note-1">&#91;1&#93;</a></sup>
            </p>
            """
        )
        statements = list(get_paragraph_statements(p))
        assert statements == [Statement("statement.", [Citation("cite_ref-1", "1")])]

    def test_two_citations(self):
        p = parse(
            """
            <p>
                Statement
                <sup id="cite_ref-1" class="reference"><a href="#cite_note-1">&#91;1&#93;</a></sup>
                <sup id="cite_ref-2" class="reference"><a href="#cite_note-2">&#91;2&#93;</a></sup>
            </p>
        """
        )
        statements = list(get_paragraph_statements(p))
        assert statements == [
            Statement(
                "Statement",
                [
                    Citation("cite_ref-1", "1"),
                    Citation("cite_ref-2", "2"),
                ],
            ),
        ]


class TestGetStatements:
    def test_sample_1(self):
        sample = Path(__file__).parent / "data/sample-1.html"
        text = sample.read_text()
        soup = BeautifulSoup(text, "lxml")
        statements = list(get_statements(soup))
        expected_statements = [
            Statement(
                "This is the first statement.",
                [
                    Citation("cite_ref-:2_1-0", number="1", name="2", suffix="0"),
                    Citation("cite_ref-:0_2-0", number="2", name="0", suffix="0"),
                    Citation("cite_ref-:1_3-0", number="3", name="1", suffix="0"),
                ],
            ),
            Statement(
                "And this is the second.",
                [
                    Citation("cite_ref-:0_2-1", number="2", name="0", suffix="1"),
                ],
            ),
            Statement(
                "And the third.",
                [
                    Citation("cite_ref-:1_3-1", number="3", name="1", suffix="1"),
                ],
            ),
            Statement(
                "Another paragraph",
                [
                    Citation("cite_ref-:2_1-1", number="1", name="2", suffix="1"),
                ],
            ),
            Statement(
                "with some citations.",
                [
                    Citation("cite_ref-:0_2-2", number="2", name="0", suffix="2"),
                ],
            ),
            Statement(
                "And a new section!",
                [
                    Citation("cite_ref-:1_3-2", number="3", name="1", suffix="2"),
                ],
            ),
        ]
        assert statements == expected_statements
