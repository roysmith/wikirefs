from dataclasses import dataclass

from wikirefs.citation import Citation


@dataclass(frozen=True)
class Statement:
    """A hunk of text and the citations that support it."""

    text: str
    citations: list[Citation]
