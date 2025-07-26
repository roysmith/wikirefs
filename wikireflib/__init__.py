"""
This parses a wikipedia article, extracting claims and the citations which
support those claims.  A claim is just a run of text.  It is terminated by
one or more citations or (in the pathological case) by the end of a paragraph.

Each citation points to a source.  There are some unusual citation styles
where a single citation contains multiple sources.  It's not clear how
these should be handled; one possibility is to internally split them into
multiple citations.

There may be multiple citations pointing to the same source.  In this case,
the enclosing <ref> tags will all have the same 'name' attribute.  Only
one of them will be a <ref>...</ref> pair, with the others being self-closing
<ref /> tags.  It is possible to have a <ref> with no 'name' attribute;
the resulting Citation will include a generated name with no semantics
beyond being unique.

In some styles, a page number is assigned to a citation using a {{rp}}
template after the <ref> tag; this is incorporated into the Citation.
"""

from .article import Article
from .citation import Citation
from .source import Source
