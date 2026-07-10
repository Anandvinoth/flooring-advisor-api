from pathlib import Path
from bs4 import BeautifulSoup
import json

BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"


def get_meta(soup, name=None, prop=None):
    if name:
        tag = soup.find("meta", attrs={"name": name})
    else:
        tag = soup.find("meta", attrs={"property": prop})

    return tag.get("content", "").strip() if tag else ""


def extract_site(site_name):
    html_path = CRAWL_DIR / site_name / "homepage.html"
    html = html_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "lxml")

    data = {
        "site": site_name,
        "title": soup.title.string.strip() if soup.title else "",
        "meta_description": get_meta(soup, name="description"),
        "robots": get_meta(soup, name="robots"),
        "canonical": soup.find("link", rel="canonical").get("href", "") if soup.find("link", rel="canonical") else "",
        "h1": [h.get_text(" ", strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(" ", strip=True) for h in soup.find_all("h2")],
        "schema_count": len(soup.find_all("script", type="application/ld+json")),
        "internal_links": len([a for a in soup.find_all("a", href=True) if site_name in a["href"] or a["href"].startswith("/")]),
        "images": len(soup.find_all("img")),
        "images_with_alt": len([img for img in soup.find_all("img") if img.get("alt")]),
        "word_count": len(soup.get_text(" ", strip=True).split()),
        "livermore_mentions": soup.get_text(" ", strip=True).lower().count("livermore"),
        "flooring_mentions": soup.get_text(" ", strip=True).lower().count("flooring"),
        "mohawk_mentions": soup.get_text(" ", strip=True).lower().count("mohawk"),
    }

    out_path = CRAWL_DIR / site_name / "metadata.json"
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    extract_site("lattafloors")
    extract_site("flooring-solutions")