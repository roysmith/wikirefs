from dataclasses import dataclass
from collections.abc import Iterable

import mwparserfromhell as mwp

from .citation import Citation
from .source import Source


@dataclass(frozen=True)
class Article:
    text: str
    code: mwp.wikicode.Wikicode

    def build(text):
        code = mwp.parse(text)
        return Article(text, code)

    def citations(self) -> Iterable[Citation]:
        for ref_node in self.code.filter_tags(matches=lambda node: node.tag == "ref"):
            yield Citation.build(ref_node)

    def sources(self) -> Iterable[Source]:
        for citation in self.citations():
            if citation.ref.contents:
                yield Source(citation.ref.contents, citation.name())
