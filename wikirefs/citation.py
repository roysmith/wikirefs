from dataclasses import dataclass
import re

from bs4 import Tag, NavigableString


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
        """Factory function"""
        pattern = re.compile(
            r"""
            cite_ref-               # constant prefix
            ((?P<name>.+)_)?        # optional ref name (":0" or "foo")
            (?P<number>\d+)         # user-visible ref number ("1")
            (-(?P<suffix>\d+))?     # optional ref number suffix ("-0")
            """,
            re.VERBOSE,
        )
        if m := re.fullmatch(pattern, ref_id):
            return Citation(ref_id, **m.groupdict())
        else:
            raise ValueError(f"cannot parse ref_id '{ref_id}'")

    @staticmethod
    def from_reference_tag(tag: NavigableString):
        ref_id = tag.parent.parent.get("id")
        number = tag.text.removeprefix("[").removesuffix("]")
        return Citation(ref_id, number)

    def rendered_suffix(self) -> str:
        """If this citation has a suffix, return it in the format used
        by wiki references, i.e. 'a', 'b' ... 'z', 'aa', ...

        """
        if self.suffix:
            return self.bijective_hexavigesimal(int(self.suffix) + 1)
        else:
            return ""

    # Courtesy of User:Ahecht (https://w.wiki/AcQC)
    @staticmethod
    def bijective_hexavigesimal(n: int):
        "Convert a integer (1-based) to bijective base-26"
        out_str = ""
        while n != 0:
            out_str = chr((n - 1) % 26 + 97) + out_str
            n = (n - 1) // 26
        return out_str
