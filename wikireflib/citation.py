from dataclasses import dataclass

import mwparserfromhell as mwp
from mwparserfromhell.nodes import Tag

from .source import Source


@dataclass(frozen=True)
class Citation:
    ref: Tag
    source: Source

    def build(ref: Tag):
        try:
            name = ref.get("name").value
        except ValueError:
            name = None
        return Citation(ref, Source(ref.contents, name))

    def name(self) -> str:
        try:
            return self.ref.get("name").value
        except ValueError:
            return None
