from bs4 import BeautifulSoup

from wikirefs.article import Article, get_reference_for_ref_id, build_citation_map
from wikirefs.citation import Citation
from wikirefs.statement import Statement


def parse(text):
    return BeautifulSoup(text, features="lxml")


def test_construct():
    article = Article("<html></html>")
    assert article.soup == "<html></html>"


class TestGetParagraphStatements:
    def test_no_text(self):
        p = parse("<p></p>")
        assert not list(Article.get_paragraph_statements(p))

    def test_one_statement(self):
        p = parse(
            """
            <p>statement.
                <sup id="cite_ref-1" class="reference"><a href="#cite_note-1">&#91;1&#93;</a></sup>
            </p>
            """
        )
        statements = list(Article.get_paragraph_statements(p))
        assert statements == [Statement("statement.", [Citation("cite_ref-1", "1")])]

    def test_statement_with_links(self):
        p = parse(
            """
                <p>After graduating from college in 1903,
                Austin worked for <a href="/wiki/General_Electric" title="General Electric">General Electric</a>
                in <a href="/wiki/Schenectady,_New_York" title="Schenectady, New York">Schenectady, New York</a>.
                <sup id="cite_ref-:3_1-0" class="reference"><a href="#cite_note-:3-1">[1]</a></sup>
                He was hired by <a href="/wiki/Pacific_Gas_and_Electric_Company" title="Pacific Gas and Electric Company">
                Pacific Gas and Electric</a>, initially acting as their eastern representative doing insulator testing.
                <sup id="cite_ref-:0_2-0" class="reference"><a href="#cite_note-:0-2">[2]</a></sup>
                <sup id="cite_ref-:3_1-1" class="reference"><a href="#cite_note-:3-1">[1]</a></sup>
            </p>
            """
        )
        statements = list(Article.get_paragraph_statements(p))
        assert [s.text for s in statements] == [
            "After graduating from college in 1903, Austin worked for General Electric in Schenectady, New York .",
            "He was hired by Pacific Gas and Electric , initially acting as their eastern representative doing insulator testing.",
        ]

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
        statements = list(Article.get_paragraph_statements(p))
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
    def test_sample_1(self, sample_1_html):
        article = Article.from_html(sample_1_html)
        statements = list(article.get_statements())
        expected_statements = [
            Statement(
                "This is the first statement.",
                [
                    Citation("cite_ref-:2_1-0", number="1", name=":2", suffix="0"),
                    Citation("cite_ref-:0_2-0", number="2", name=":0", suffix="0"),
                    Citation("cite_ref-:1_3-0", number="3", name=":1", suffix="0"),
                ],
            ),
            Statement(
                "And this is the second.",
                [
                    Citation("cite_ref-:0_2-1", number="2", name=":0", suffix="1"),
                ],
            ),
            Statement(
                "And the third.",
                [
                    Citation("cite_ref-:1_3-1", number="3", name=":1", suffix="1"),
                ],
            ),
            Statement(
                "Another paragraph",
                [
                    Citation("cite_ref-:2_1-1", number="1", name=":2", suffix="1"),
                ],
            ),
            Statement(
                "with some citations.",
                [
                    Citation("cite_ref-:0_2-2", number="2", name=":0", suffix="2"),
                ],
            ),
            Statement(
                "And a new section!",
                [
                    Citation("cite_ref-:1_3-2", number="3", name=":1", suffix="2"),
                ],
            ),
        ]
        assert statements == expected_statements


class TestGetReference:
    def test_get_reference_for_ref_id(self, sample_1_html):
        soup = BeautifulSoup(sample_1_html, "lxml")
        cite_tag = get_reference_for_ref_id(soup, "cite_ref-:2_1-0")
        assert cite_tag.name == "span"
        assert cite_tag.get("class") == ["reference-text"]

    def test_arthur_o_austin(self, arthur_o_austin_html):
        soup = BeautifulSoup(arthur_o_austin_html, "lxml")
        article = Article(soup)
        statements = list(article.get_statements())
        citation_map = build_citation_map(soup, statements)
        ref_15 = citation_map["cite_ref-15"]
        assert "issued August 7, 1934" in ref_15.text
