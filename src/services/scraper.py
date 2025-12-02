import re
from bs4 import BeautifulSoup
from ..utils.http_client import get_client

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"


def fetch_wikipedia_page(title: str, year: int) -> str:
    # Wikipedia page format: Title_(year_film)
    page_title = f"{title.replace(' ', '_')}_({year}_film)"
    url = WIKIPEDIA_BASE_URL + page_title
    client = get_client()
    resp = client.get(url)
    return resp.text


def parse_poster_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    if infobox:
        img = infobox.find("img")
        if img and img.has_attr("src"):
            return "https:" + img["src"]
    return None


def parse_synopsis(html: str) -> str:
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


def parse_film_image_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    if infobox:
        imgs = infobox.find_all("img")
        if imgs and len(imgs) > 1:
            return "https:" + imgs[1]["src"]
        elif imgs:
            return "https:" + imgs[0]["src"]
    return None
