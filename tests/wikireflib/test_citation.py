import pytest

import mwparserfromhell as mwp
from mwparserfromhell.nodes import Node
from mwparserfromhell.nodes.extras import Attribute

from wikireflib import Citation


def make_ref_node(wikitext: str) -> Node:
    code = mwp.parse(wikitext)
    assert len(code.nodes) == 1
    node = code.nodes[0]
    assert node.tag == "ref"
    return node


def test_build():
    ref = make_ref_node('<ref name="x">foo</ref>')
    citation = Citation.build(ref)
    assert citation.ref == ref


def test_construct():
    ref = make_ref_node('<ref name="x">foo</ref>')
    citation = Citation(ref, "x")
    assert citation.ref == ref


def test_get_source():
    ref = make_ref_node('<ref name="x">foo</ref>')
    citation = Citation(ref, "x")
    assert citation.ref.attributes == [Attribute("name", "x")]
    assert citation.ref.contents == "foo"
