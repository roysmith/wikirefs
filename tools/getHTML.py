from pywikibot import Site, Page

site = Site("en")
page = Page(site, "User:RoySmith/sandbox")
print(f"<!-- Created from {page.create_short_link(permalink=True)} -->")
html = page.get_parsed_page()
print(html)
