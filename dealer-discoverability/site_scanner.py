import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SITES = {
    "lattafloors": "https://www.lattafloors.com",
    "flooring-solutions": "https://www.flooring-solutions.com",
}

BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"


def fetch(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code, r.text
    except Exception as e:
        return 0, str(e)


def schema_types(html):
    soup = BeautifulSoup(html, "lxml")
    types = []

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "{}")
            items = data if isinstance(data, list) else [data]
            for item in items:
                t = item.get("@type")
                if isinstance(t, list):
                    types.extend(t)
                elif t:
                    types.append(t)
        except Exception:
            pass

    return sorted(set(types))


def scan_site(name, base_url):
    output_dir = CRAWL_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)

    homepage_status, homepage_html = fetch(base_url)
    robots_status, robots_text = fetch(urljoin(base_url, "/robots.txt"))
    sitemap_status, sitemap_text = fetch(urljoin(base_url, "/sitemap.xml"))

    text = BeautifulSoup(homepage_html, "lxml").get_text(" ", strip=True).lower()

    result = {
        "site": name,
        "url": base_url,
        "homepage_status": homepage_status,
        "robots_found": robots_status == 200,
        "sitemap_found": sitemap_status == 200,
        "schema_types": schema_types(homepage_html),
        "has_faq_text": "faq" in text or "frequently asked" in text,
        "has_contact_text": "contact" in text,
        "has_about_text": "about" in text,
        "has_brand_text": "brand" in text or "brands" in text,
        "has_mohawk_text": "mohawk" in text,
        "has_livermore_text": "livermore" in text,
        "service_area_mentions": len(re.findall(r"livermore|pleasanton|dublin|san ramon|bay area|alameda", text)),
    }

    out = output_dir / "site_scan.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    for name, url in SITES.items():
        scan_site(name, url)