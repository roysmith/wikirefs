import argparse

from pywikibot import Site, Page


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    args = parser.parse_args()

    site = Site("en")
    page = Page(site, args.title)
    print(f"<!-- {page.title()} -->")
    print(f"<!-- Created from {page.create_short_link(permalink=True)} -->")
    html = page.get_parsed_page()
    print(html)


if __name__ == "__main__":
    main()
