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
external_links = [link for link in page.links if link.startswith("http")]
expected_links = {
    "https://brotatotes.github.io/how-a-watch-works/",
    "https://brotatotes.github.io/blade-on-the-beat/",
    "https://brotatotes.com/",
    "https://biblego.org/",
    "https://hymnsandspiritualsongs.com/",
    "https://digitize.brotatotes.com/",
    "https://food.brotatotes.com/",
    "https://brotatotes.github.io/chess-three-ways/",
    "https://brotatotes.github.io/drive-world/",
    "https://brotatotes.github.io/last-ten-minutes/",
    "https://brotatotes.github.io/clockwork-garden/",
    "https://brotatotes.github.io/forty-eight/",
    "https://brotatotes.github.io/battlebrotts-reborn/",
    "https://tictactoe.brotatotes.com/",
    "https://brotatotes.github.io/studio-arcade/",
    "https://brotatotes.github.io/brott-island/",
    "https://studio.brotatotes.com/",
}
assert set(external_links) == expected_links
assert len(external_links) == len(expected_links), "Duplicate site links"
print(f"html audit: pass ({len(page.ids)} ids, {len(page.links)} links, one h1)")
