import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"


def load(site, file_name):
    return json.loads((CRAWL_DIR / site / file_name).read_text())


def score_site(site):
    meta = load(site, "metadata.json")
    scan = load(site, "site_scan.json")

    local = 0
    if "LocalBusiness" in scan["schema_types"]:
        local += 8
    if meta["livermore_mentions"] >= 3:
        local += 6
    if scan["service_area_mentions"] >= 3:
        local += 5
    if "livermore" in meta["title"].lower():
        local += 4
    if scan["has_contact_text"]:
        local += 2

    content = 0
    if meta["word_count"] >= 500:
        content += 7
    if len(meta["h1"]) == 1:
        content += 5
    if meta["flooring_mentions"] >= 8:
        content += 5
    if meta["internal_links"] >= 50:
        content += 4
    if meta["images"] and meta["images_with_alt"] / meta["images"] >= 0.5:
        content += 4

    technical = 0
    if scan["robots_found"]:
        technical += 5
    if scan["sitemap_found"]:
        technical += 5
    if meta["canonical"]:
        technical += 5
    if meta["schema_count"] > 0:
        technical += 5
    if scan["homepage_status"] == 200:
        technical += 5

    ai = 0
    if scan["schema_types"]:
        ai += 5
    if "LocalBusiness" in scan["schema_types"]:
        ai += 6
    if meta["meta_description"]:
        ai += 4
    if meta["word_count"] >= 500:
        ai += 4
    if scan["has_livermore_text"]:
        ai += 3
    if scan["has_mohawk_text"]:
        ai += 3

    return {
        "site": site,
        "Local SEO": local,
        "Content Quality": content,
        "Technical SEO": technical,
        "AI Readiness": ai,
        "Total": local + content + technical + ai,
    }


if __name__ == "__main__":
    for site in ["lattafloors", "flooring-solutions"]:
        print(json.dumps(score_site(site), indent=2))