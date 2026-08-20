from html.parser import HTMLParser
from pathlib import Path


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.links = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
            if attributes["href"].startswith("#"):
                self.refs.append(attributes["href"][1:])
        if tag == "h1":
            self.h1 += 1


page = Audit()
page.feed(Path("index.html").read_text())
assert page.h1 == 1
assert all(reference in page.ids for reference in page.refs)
assert len([link for link in page.links if link.startswith("http")]) == 9
print(f"html audit: pass ({len(page.ids)} ids, {len(page.links)} links, one h1)")
