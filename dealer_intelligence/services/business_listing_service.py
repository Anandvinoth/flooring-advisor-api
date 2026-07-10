from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from dealer_intelligence.config.business_listings import BUSINESS_LISTINGS


PLATFORM_DOMAINS = {
    "google_business_profile": ["google.com", "goo.gl", "maps.app.goo.gl"],
    "bing_places": ["bing.com"],
    "apple_business_connect": ["maps.apple.com"],
    "yelp": ["yelp.com"],
    "bbb": ["bbb.org"],
    "yellow_pages": ["yellowpages.com", "yp.com"],
    "foursquare": ["foursquare.com"],
    "hotfrog": ["hotfrog.com"],
    "manta": ["manta.com"],
    "merchant_circle": ["merchantcircle.com"],
    "ezlocal": ["ezlocal.com"],
    "brownbook": ["brownbook.net"],
    "local_com": ["local.com"],
    "citysearch": ["citysearch.com"],
    "mapquest": ["mapquest.com"],
    "chamber": ["chamberofcommerce.com"],
    "showmelocal": ["showmelocal.com"],
    "elocal": ["elocal.com"],
    "cylex": ["cylex.us.com", "cylex.com"],
    "alignable": ["alignable.com"],
}


def _domain_matches(url: str, domains: list[str]) -> bool:
    try:
        hostname = urlparse(url).hostname or ""
        hostname = hostname.lower()

        return any(
            hostname == domain or hostname.endswith(f".{domain}")
            for domain in domains
        )
    except ValueError:
        return False


def analyze_business_listings(html_path: Path) -> dict:
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    links = [
        link.get("href", "").strip()
        for link in soup.find_all("a", href=True)
    ]

    report = {}

    for key, config in BUSINESS_LISTINGS.items():
        domains = PLATFORM_DOMAINS.get(key, [])

        matched_urls = [
            url
            for url in links
            if url.startswith(("http://", "https://"))
            and _domain_matches(url, domains)
        ]

        found = bool(matched_urls)

        report[key] = {
            "label": config["label"],
            "status": "LINKED_FROM_WEBSITE" if found else "NOT_LINKED_FROM_WEBSITE",
            "score": config["weight"] if found else 0,
            "max_score": config["weight"],
            "evidence": matched_urls,
            "recommendation": (
                ""
                if found
                else f"Verify or create the {config['label']} listing and link it from the dealer website."
            ),
        }

    total_score = sum(item["score"] for item in report.values())
    max_score = sum(item["max_score"] for item in report.values())

    percentage = round(
        (total_score / max_score) * 100,
        2,
    ) if max_score else 0

    return {
        "category": "Business Listings",
        "score": percentage,
        "earned_points": total_score,
        "available_points": max_score,
        "listings": report,
    }
