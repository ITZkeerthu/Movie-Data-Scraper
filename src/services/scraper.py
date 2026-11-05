import re
from typing import Optional
from urllib.parse import quote
from bs4 import BeautifulSoup
from ..utils.http_client import get_client

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"


def fetch_wikipedia_page(title: str, year: int) -> str:
    # Wikipedia page format: Title_(year_film)
    page_title = quote(f"{title.strip().replace(' ', '_')}_({year}_film)", safe="_()")
    url = WIKIPEDIA_BASE_URL + page_title
    client = get_client()
    resp = client.get(url)
    return resp.text


def _absolute_url(src: Optional[str]) -> Optional[str]:
    """Normalise an <img> src to an absolute https URL (None if unusable)."""
    if not src:
        return None
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return "https://en.wikipedia.org" + src
    if src.startswith(("http://", "https://")):
        return src
    return None


def _infobox_image_urls(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return []
    urls = (_absolute_url(img.get("src")) for img in infobox.find_all("img"))
    return [u for u in urls if u]


def parse_poster_url(html: str) -> Optional[str]:
    urls = _infobox_image_urls(html)
    return urls[0] if urls else None


def parse_synopsis(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    # Try to find the plot section
    plot_header = soup.find(id=re.compile("plot", re.I))
    if plot_header:
        plot_section = plot_header.find_next("p")
        if plot_section:
            return plot_section.get_text(strip=True)
    # Fallback: first paragraph
    first_p = soup.find("p")
    if first_p:
        return first_p.get_text(strip=True)
    return None


def parse_film_image_url(html: str) -> Optional[str]:
    urls = _infobox_image_urls(html)
    if len(urls) > 1:
        return urls[1]
    return urls[0] if urls else None
