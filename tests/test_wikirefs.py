from lxml import etree

import wikirefs


def test_import():
    assert wikirefs


def test_find_one_ref():
    html = r"""<html>
                    <body>
                        <sup id="cite_ref-Schneider1974_3-2" class="reference">
                            <a href="#cite_note-Schneider1974-3">
                                &#91;3&#93;
                           </a>
                        </sup>
                    </body>
                </html>"""
    tree = etree.fromstring(html, etree.HTMLParser())
    elements = tree.cssselect("sup[id^='cite_ref-']")
    assert [e.get("id") for e in elements] == ["cite_ref-Schneider1974_3-2"]


def test_find_two_refs():
    html = r"""<html>
                    <body>
                        <sup id="cite_ref-Schneider1974_3-2" class="reference">
                            <a href="#cite_note-Schneider1974-3">
                                &#91;3&#93;
                           </a>
                        </sup>
                        <sup id="cite_ref-Schneider1974_3-5" class="reference">
                            <a href="#cite_note-Schneider1974-3">
                                &#91;3&#93;
                           </a>
                        </sup>
                    </body>
                </html>"""
    tree = etree.fromstring(html, etree.HTMLParser())
    elements = tree.cssselect("sup[id^='cite_ref-']")
    assert [e.get("id") for e in elements] == [
        "cite_ref-Schneider1974_3-2",
        "cite_ref-Schneider1974_3-5",
    ]
