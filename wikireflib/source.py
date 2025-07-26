from dataclasses import dataclass

import mwparserfromhell as mwp
from mwparserfromhell.wikicode import Wikicode


@dataclass(frozen=True)
class Source:
    code: Wikicode
    name: str
