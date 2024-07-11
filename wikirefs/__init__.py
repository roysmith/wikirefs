from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional

from bs4 import NavigableString, Tag, BeautifulSoup

import more_itertools


@dataclass(frozen=True)
class Citation:
    """ref_id is the raw HTML "id" from the <sup> element.

    number is user-visible citation number which goes inside the []

    name is the reference name, either a name attribute supplied
        in a <ref> element, or one invented by VisualEditor.

    suffix is an optional disambguator added when a reference is used
    more than once.  "0" maps to "a", "1" to "b", etc.
    """

    ref_id: str
    number: str
    name: str = None
    suffix: str = None

    @staticmethod
    def from_id(ref_id: str):
        pattern = re.compile(
            r"""
            cite_ref-               # constant prefix
            (:(?P<name>[^_]+)_)?    # optional ref name (":0_" or ":foo_")
            (?P<number>\d+)         # user-visible ref number ("1")
            (-(?P<suffix>\d+))?     # optional ref number suffix ("-0")
            """,
            re.VERBOSE,
        )
        if m := re.fullmatch(pattern, ref_id):
            return Citation(ref_id, **m.groupdict())
        else:
            raise ValueError(f"cannot parse ref_id '{ref_id}'")

    def rendered_suffix(self):
        if self.suffix:
            return self.bijectiveHexavigesimal(int(self.suffix) + 1)
        else:
            return ""

    # Courtesy of User:Ahecht (https://w.wiki/AcQC)
    @staticmethod
    def bijectiveHexavigesimal(n: int):
        "Convert a integer (1-based) to bijective base-26"
        outStr = ""
        while n != 0:
            outStr = chr((n - 1) % 26 + 97) + outStr
            n = (n - 1) // 26
        return outStr


@dataclass(frozen=True)
class Statement:
    text: str
    citations: list[Citation]


class State(Enum):
    """The last thing we've seen.  There is no explicit start state;
    we start in STRING, which effectively means that last thing we've
    seen is an empty string.
    """

    STRING = 1
    CITATION = 2


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


def get_statements(soup: BeautifulSoup):
    for p in soup.find_all("p"):
        for statement in get_paragraph_statements(p):
            yield statement


def get_paragraph_statements(p: Tag):
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
                if cid := citation_id(node):
                    citations.append(Citation.from_id(cid))
                    state = State.CITATION
                else:
                    words.extend(node.string.split())
            case State.CITATION:
                if cid := citation_id(node):
                    citations.append(Citation.from_id(cid))
                else:
                    text = " ".join(words)
                    yield Statement(text, citations)
                    words = node.string.split()
                    citations = []
            case _:
                raise RuntimeError(f"Unknown state: {state}")

    # We're reached the end of the paragraph, but we might need
    # to flush the last statement collected.
    if words or citations:
        text = " ".join(words)
        yield Statement(text, citations)
