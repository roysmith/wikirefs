from pywikibot import Site, Page

site = Site("en")
page = Page(site, "User:RoySmith/sandbox")
print(page)
html = page.get_parsed_page()
print(html)
