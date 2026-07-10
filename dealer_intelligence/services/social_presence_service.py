from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from dealer_intelligence.config.social_platforms import SOCIAL_PLATFORMS


def _domain_matches(url: str, domains: list[str]) -> bool:
    try:
        hostname = (urlparse(url).hostname or "").lower()

        return any(
            hostname == domain or hostname.endswith(f".{domain}")
            for domain in domains
        )
    except ValueError:
        return False


def analyze_social_presence(html_path: Path) -> dict:
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    links = [
        tag.get("href", "").strip()
        for tag in soup.find_all("a", href=True)
    ]

    platforms = {}

    for key, config in SOCIAL_PLATFORMS.items():
        matched_urls = [
            url
            for url in links
            if url.startswith(("http://", "https://"))
            and _domain_matches(url, config["domains"])
        ]

        found = bool(matched_urls)

        platforms[key] = {
            "label": config["label"],
            "status": "FOUND" if found else "NOT_DETECTED",
            "score": config["weight"] if found else 0,
            "max_score": config["weight"],
            "evidence": matched_urls,
            "recommendation": (
                ""
                if found
                else f"Create or connect an active {config['label']} profile."
            ),
        }

    earned_points = sum(item["score"] for item in platforms.values())
    available_points = sum(item["max_score"] for item in platforms.values())

    return {
        "category": "Social Presence",
        "score": round((earned_points / available_points) * 100, 2),
        "earned_points": earned_points,
        "available_points": available_points,
        "platforms": platforms,
    }