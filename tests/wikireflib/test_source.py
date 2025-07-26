import pytest
import mwparserfromhell as mwp


from wikireflib import Source


def test_construct():
    code = mwp.parse("foo")
    source = Source(code, "my name")
    assert source.code == code
    assert source.name == "my name"
