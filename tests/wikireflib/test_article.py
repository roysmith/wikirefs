from pathlib import Path

import pytest
import mwparserfromhell as mwp


from wikireflib import Article, Citation, Source


@pytest.fixture
def msbrown_wikitext():
    path = Path(__file__).parent / "Margaret_Sibella_Brown@1292332616.wiki"
    return path.read_text()


@pytest.fixture
def msbrown_article(msbrown_wikitext):
    return Article.build(msbrown_wikitext)


def test_construct(msbrown_wikitext):
    code = mwp.parse(msbrown_wikitext)
    article = Article(msbrown_wikitext, code)
    assert article.text == msbrown_wikitext


def test_build(msbrown_wikitext):
    code = mwp.parse(msbrown_wikitext)
    article = Article.build(msbrown_wikitext)
    assert article.code == code


def test_citations(msbrown_article):
    citations = list(msbrown_article.citations())
    assert citations
    for citation in citations:
        assert type(citation) == Citation


def test_get_sources_with_no_sources():
    article = Article.build("foo")
    sources = list(article.sources())
    assert len(sources) == 0


def test_get_sources_with_one_source():
    article = Article.build('<ref name="refname">foo</ref>')
    sources = list(article.sources())
    assert sources == [Source("foo", "refname")]
