# cat > dealer_intelligence/extractor.py <<'PY'
import json
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"

def count_phrase(text: str, phrase: str) -> int:
    if not phrase or not phrase.strip():
        return 0

    pattern = rf"\b{re.escape(phrase.strip())}\b"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

def get_meta(soup, name=None, prop=None):
    if name:
        tag = soup.find("meta", attrs={"name": name})
    else:
        tag = soup.find("meta", attrs={"property": prop})

    return tag.get("content", "").strip() if tag else ""


def extract_site(
    site_id: str,
    dealer_url: str,
    city: str,
    state: str,
    brand_name: str = "Mohawk",
):
    html_path = CRAWL_DIR / site_id / "homepage.html"

    if not html_path.exists():
        raise FileNotFoundError(f"Crawl file not found: {html_path}")

    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    page_text = soup.get_text(" ", strip=True)
    page_text_lower = page_text.lower()

    hostname = (urlparse(dealer_url).hostname or "").lower()
    hostname = hostname.removeprefix("www.")

    internal_links = []

    for tag in soup.find_all("a", href=True):
        href = tag.get("href", "").strip()

        if href.startswith("/"):
            internal_links.append(href)
        elif hostname and hostname in href.lower():
            internal_links.append(href)

    images = soup.find_all("img")
    images_with_alt = [
        image
        for image in images
        if image.get("alt", "").strip()
    ]

    canonical_tag = soup.find("link", rel="canonical")

    data = {
        "site_id": site_id,
        "url": dealer_url,
        "city": city,
        "state": state,
        "brand_name": brand_name,
        "title": soup.title.string.strip() if soup.title and soup.title.string else "",
        "meta_description": get_meta(soup, name="description"),
        "robots": get_meta(soup, name="robots"),
        "canonical": canonical_tag.get("href", "") if canonical_tag else "",
        "h1": [h.get_text(" ", strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(" ", strip=True) for h in soup.find_all("h2")],
        "schema_count": len(
            soup.find_all("script", type="application/ld+json")
        ),
        "internal_links": len(internal_links),
        "images": len(images),
        "images_with_alt": len(images_with_alt),
        "word_count": len(page_text.split()),
        "city_mentions": count_phrase(page_text, city),
        "state_mentions": count_phrase(page_text, state),
        "flooring_mentions": page_text_lower.count("flooring"),
        "brand_mentions": page_text_lower.count(brand_name.lower()),
    }

    output_path = CRAWL_DIR / site_id / "metadata.json"
    output_path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    return data