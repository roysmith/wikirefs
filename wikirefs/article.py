"""A parsed article."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional, Mapping


from bs4 import BeautifulSoup, Tag, NavigableString

from wikirefs.statement import Statement
from wikirefs.citation import Citation


class State(Enum):
    """The last thing we've seen.  There is no explicit start state;
    we start in STRING, which effectively means that last thing we've
    seen is an empty string.

    """

    STRING = 1
    CITATION = 2


@dataclass(frozen=True)
class Article:
    soup: BeautifulSoup

    @staticmethod
    def from_html(html: str):
        """Construct an Article from parsed HTML, i.e. what you would get
        back from https://www.mediawiki.org/wiki/API:Parsing_wikitext.

        """
        return Article(BeautifulSoup(html, features="lxml"))

    def get_statements(self) -> Iterator[Statement]:
        """Find all the statements in a document.  In theory, all
        user-visible text is enclosed in <p> tags; this (intentionally)
        excludes text outside of that.

        """
        for p in self.soup.find_all("p"):
            for statement in Article.get_paragraph_statements(p):
                yield statement

    @staticmethod
    def get_paragraph_statements(p: Tag) -> Iterator[Statement]:
        """Find all the statements in a single paragraph"""
        words = []
        citations = []
        state = State.STRING
        for node in p.descendants:
            if not isinstance(node, NavigableString):
                continue
            if node.string.strip() == "":
                continue
            match state:
                case State.STRING:
                    if cid := Article.citation_id(node):
                        citations.append(Citation.from_id(cid))
                        state = State.CITATION
                    else:
                        words.extend(node.string.split())
                case State.CITATION:
                    if cid := Article.citation_id(node):
                        citations.append(Citation.from_id(cid))
                    else:
                        text = " ".join(words)
                        yield Statement(text, citations)
                        words = node.string.split()
                        citations = []
                        state = State.STRING
                case _:
                    raise RuntimeError(f"Unknown state: {state}")

        # We're reached the end of the paragraph, but we might need
        # to flush the last statement collected.
        if words or citations:
            text = " ".join(words)
            yield Statement(text, citations)

    @staticmethod
    def citation_id(node: Tag) -> Optional[str]:
        """If this is a citation marker, return the id of the enclosing
        <sup> tag.  Otherwise, return None.

        """
        if isinstance(node, NavigableString) and node.parent.name == "a":
            node2 = node.parent.parent
            return (
                node2.name == "sup"
                and node2.get("class") == ["reference"]
                and node2.get("id")
            )

    def get_reference_for_ref_id(self, ref_id: str) -> Tag:
        sup_tag = self.soup.find("sup", id=ref_id)
        note_fragment = sup_tag.find("a").get("href")
        note_id = note_fragment.removeprefix("#")
        li_tag = self.soup.find("li", id=note_id)
        cite_tag = li_tag.find("span", class_="reference-text")
        return cite_tag

    def build_citation_map(self, statements: list[Statement]) -> Mapping[str, Tag]:
        citation_map = {}
        for statement in statements:
            for citation in statement.citations:
                ref_id = citation.ref_id
                citation_map[ref_id] = self.get_reference_for_ref_id(ref_id)
        return citation_map
