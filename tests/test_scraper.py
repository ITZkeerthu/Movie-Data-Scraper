from src.services import scraper

HTML = """
<html><body><p>Intro paragraph.</p>
<table class="infobox"><tr><td>
<img src="//upload.wikimedia.org/poster.jpg"/>
<img src="/static/still.png"/>
</td></tr></table>
<h2 id="Plot">Plot</h2><p>The plot text.</p></body></html>
"""


def test_poster_url_protocol_relative():
    assert scraper.parse_poster_url(HTML) == "https://upload.wikimedia.org/poster.jpg"


def test_film_image_uses_second_image_and_resolves_relative():
    assert scraper.parse_film_image_url(HTML) == "https://en.wikipedia.org/static/still.png"


def test_single_image_falls_back_to_first():
    html = '<table class="infobox"><img src="https://x.org/a.jpg"></table>'
    assert scraper.parse_film_image_url(html) == "https://x.org/a.jpg"


def test_no_infobox_or_missing_src_returns_none():
    assert scraper.parse_poster_url("<p>hi</p>") is None
    assert scraper.parse_poster_url('<table class="infobox"><img></table>') is None
    assert scraper.parse_film_image_url('<table class="infobox"><img></table>') is None


def test_synopsis_prefers_plot_section_then_first_paragraph():
    assert scraper.parse_synopsis(HTML) == "The plot text."
    assert scraper.parse_synopsis("<p>Only para</p>") == "Only para"
    assert scraper.parse_synopsis("<div></div>") is None


def test_page_title_is_url_quoted(monkeypatch):
    seen = {}

    class C:
        def get(self, url):
            seen["url"] = url
            class R: text = "x"
            return R()

    monkeypatch.setattr(scraper, "get_client", lambda: C())
    scraper.fetch_wikipedia_page("Amélie & Co", 2001)
    assert seen["url"] == "https://en.wikipedia.org/wiki/Am%C3%A9lie_%26_Co_(2001_film)"
