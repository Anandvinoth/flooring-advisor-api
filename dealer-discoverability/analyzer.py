import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"


def load(site):
    return json.loads(
        (CRAWL_DIR / site / "metadata.json").read_text()
    )


def score(site):

    scores = {}

    # -----------------------
    # Local Visibility (25)
    # -----------------------
    local = 0

    if site["livermore_mentions"] >= 3:
        local += 10

    if "livermore" in site["title"].lower():
        local += 10

    if site["meta_description"]:
        local += 5

    scores["Local Visibility"] = local

    # -----------------------
    # Content Quality (25)
    # -----------------------
    content = 0

    if site["word_count"] >= 500:
        content += 10

    if len(site["h1"]) == 1:
        content += 10

    if site["flooring_mentions"] >= 8:
        content += 5

    scores["Content Quality"] = content

    # -----------------------
    # Technical SEO (25)
    # -----------------------
    technical = 0

    if site["robots"]:
        technical += 5

    if site["canonical"]:
        technical += 5

    if site["schema_count"] > 0:
        technical += 5

    if site["internal_links"] >= 50:
        technical += 5

    if site["images_with_alt"] >= 10:
        technical += 5

    scores["Technical SEO"] = technical

    # -----------------------
    # AI Readiness (25)
    # -----------------------
    ai = 0

    if site["meta_description"]:
        ai += 5

    if site["schema_count"] > 0:
        ai += 5

    if site["word_count"] >= 500:
        ai += 5

    if site["livermore_mentions"] >= 3:
        ai += 5

    if len(site["h1"]) == 1:
        ai += 5

    scores["AI Readiness"] = ai

    scores["Total"] = sum(scores.values())

    return scores


latta = score(load("lattafloors"))
fsi = score(load("flooring-solutions"))

print("\n========== AI Dealer Discoverability ==========\n")

print(f"{'Category':25} {'LATTA':>10} {'Flooring Solutions':>22}")
print("-"*60)

for category in [
    "Local Visibility",
    "Content Quality",
    "Technical SEO",
    "AI Readiness",
]:
    print(
        f"{category:25} "
        f"{latta[category]:>10}/25 "
        f"{fsi[category]:>18}/25"
    )

print("-"*60)
print(
    f"{'TOTAL':25} "
    f"{latta['Total']:>10}/100 "
    f"{fsi['Total']:>18}/100"
)