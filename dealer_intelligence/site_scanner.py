import json
from pathlib import Path
from urllib.parse import urljoin
import re
import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"

def count_phrase(text: str, phrase: str) -> int:
    if not phrase or not phrase.strip():
        return 0

    pattern = rf"\b{re.escape(phrase.strip())}\b"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

def fetch(url: str):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        return response.status_code, response.text
    except Exception as exc:
        return 0, str(exc)


def schema_types(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    types = []

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "{}")
            items = data if isinstance(data, list) else [data]

            for item in items:
                if not isinstance(item, dict):
                    continue

                item_type = item.get("@type")

                if isinstance(item_type, list):
                    types.extend(item_type)
                elif item_type:
                    types.append(item_type)

        except Exception:
            continue

    return sorted(set(types))


def scan_site(
    site_id: str,
    base_url: str,
    city: str,
    state: str,
    brand_name: str = "Mohawk",
):
    output_dir = CRAWL_DIR / site_id
    output_dir.mkdir(parents=True, exist_ok=True)

    homepage_status, homepage_html = fetch(base_url)
    robots_status, _ = fetch(urljoin(base_url, "/robots.txt"))
    sitemap_status, _ = fetch(urljoin(base_url, "/sitemap.xml"))

    text = BeautifulSoup(
        homepage_html,
        "lxml",
    ).get_text(" ", strip=True).lower()

    city_value = city.lower()
    state_value = state.lower()
    brand_value = brand_name.lower()

    result = {
        "site_id": site_id,
        "url": base_url,
        "city": city,
        "state": state,
        "brand_name": brand_name,
        "homepage_status": homepage_status,
        "robots_found": robots_status == 200,
        "sitemap_found": sitemap_status == 200,
        "schema_types": schema_types(homepage_html),
        "has_faq_text": (
            "faq" in text
            or "frequently asked" in text
        ),
        "has_contact_text": "contact" in text,
        "has_about_text": "about" in text,
        "has_brand_text": (
            "brand" in text
            or "brands" in text
        ),
        "has_target_brand_text": brand_value in text,
        "city_mentions": count_phrase(text, city),
        "state_mentions": count_phrase(text, state),
        "has_city_text": count_phrase(text, city) > 0,
        "has_state_text": count_phrase(text, state) > 0,
    }

    output_path = output_dir / "site_scan.json"
    output_path.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    return result