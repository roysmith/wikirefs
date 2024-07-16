#!/usr/bin/env python3

from lxml import etree


def main():
    input = "/Users/roysmith/Downloads/Ice–albedo feedback - Wikipedia.html"
    html = open(input, "rb").read()

    tree = etree.fromstring(html, etree.HTMLParser())
    for a in tree.cssselect("a[href^='#cite_ref-']"):
        print(a.get("href"))


if __name__ == "__main__":
    main()
