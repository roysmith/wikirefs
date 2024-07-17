import pytest

from wikirefs.citation import Citation


@pytest.mark.parametrize(
    "id_string, expected",
    [
        ("cite_ref-1", Citation("cite_ref-1", "1")),
        ("cite_ref-foo_1-0", Citation("cite_ref-foo_1-0", "1", "foo", "0")),
        ("cite_ref-foo_1-2", Citation("cite_ref-foo_1-2", "1", "foo", "2")),
        ("cite_ref-:0_1-2", Citation("cite_ref-:0_1-2", "1", ":0", "2")),
        (
            "cite_ref-FOOTNOTEHendel200018_7-0",
            Citation(
                "cite_ref-FOOTNOTEHendel200018_7-0",
                "7",
                "FOOTNOTEHendel200018",
                "0",
            ),
        ),
        (
            "cite_ref-internal_underscores_15-0",
            Citation(
                "cite_ref-internal_underscores_15-0",
                "15",
                "internal_underscores",
                "0",
            ),
        ),
    ],
)
def test_from_id(id_string, expected):
    citation = Citation.from_id(id_string)
    assert citation == expected


@pytest.mark.parametrize(
    "id_string",
    [
        (""),
        ("1"),
        ("foo"),
    ],
)
def test_from_id_parse_failure(id_string):
    with pytest.raises(ValueError, match="cannot parse ref_id"):
        Citation.from_id(id_string)


@pytest.mark.parametrize(
    "citation, expected",
    [
        (Citation("", "", suffix=None), ""),
        (Citation("", "", suffix="0"), "a"),
        (Citation("", "", suffix="1"), "b"),
        (Citation("", "", suffix="25"), "z"),
        (Citation("", "", suffix="26"), "aa"),
        (Citation("", "", suffix="27"), "ab"),
        (Citation("", "", suffix="52"), "ba"),
        (Citation("", "", suffix="53"), "bb"),
    ],
)
def test_rendered_suffix(citation, expected):
    rendered = citation.rendered_suffix()
    assert rendered == expected


@pytest.mark.parametrize(
    "n, expected_string",
    [
        (1, "a"),
        (2, "b"),
        (26, "z"),
        (27, "aa"),
    ],
)
def test_bijective_exavigesimal(n, expected_string):
    assert Citation.bijective_hexavigesimal(n) == expected_string
