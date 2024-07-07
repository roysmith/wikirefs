from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Statement:
    text: str
    citations: list[str]


def parse_paragraph(paragraph):
    text = re.sub(r"\s+", " ", paragraph.text).strip()
    sups = paragraph.find_all("sup", class_="reference")
    statements = []
    working_text = text
    for sup in sups:
        ref_id = sup.get("id")
        ref_label = ref_id.removeprefix("cite_ref-")
        delim = f"[{ref_label}]"
        text, more = working_text.split(delim, maxsplit=1)
        statements.append(Statement(text.strip(), [ref_label]))
        working_text = more
    return statements
