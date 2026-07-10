import json
from scoring import score_site
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"
REPORT_DIR = BASE_DIR / "data" / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(site, file_name):
    return json.loads((CRAWL_DIR / site / file_name).read_text())

def clean(value):
    return str(value).replace("|", "\\|")


latta_meta = load_json("lattafloors", "metadata.json")
fsi_meta = load_json("flooring-solutions", "metadata.json")

latta_scan = load_json("lattafloors", "site_scan.json")
fsi_scan = load_json("flooring-solutions", "site_scan.json")

latta_score = score_site("lattafloors")
fsi_score = score_site("flooring-solutions")

report = f"""
# Dealer Discoverability Evidence Report

## Query Tested
Flooring near me in Livermore, CA 94551

## Dealers Compared
- LATTA Floors
- Flooring Solutions

## Key Finding
LATTA has stronger local discoverability signals for a “flooring near me” search.

Flooring Solutions is crawlable, but its homepage signals are weaker for local residential search and AI search discovery.

## Evidence Scorecard

| Signal | LATTA Floors | Flooring Solutions |
|---|---:|---:|
| Homepage Status | {latta_scan["homepage_status"]} | {fsi_scan["homepage_status"]} |
| Robots.txt Found | {latta_scan["robots_found"]} | {fsi_scan["robots_found"]} |
| Sitemap Found | {latta_scan["sitemap_found"]} | {fsi_scan["sitemap_found"]} |
| Schema Type | {", ".join(latta_scan["schema_types"])} | {", ".join(fsi_scan["schema_types"])} |
| Page Title | {clean(latta_meta["title"])} | {clean(fsi_meta["title"])} |
| Meta Description | Present | Present |
| Livermore Mentions | {latta_meta["livermore_mentions"]} | {fsi_meta["livermore_mentions"]} |
| Service Area Mentions | {latta_scan["service_area_mentions"]} | {fsi_scan["service_area_mentions"]} |
| Word Count | {latta_meta["word_count"]} | {fsi_meta["word_count"]} |
| Internal Links | {latta_meta["internal_links"]} | {fsi_meta["internal_links"]} |
| Images With Alt Text | {latta_meta["images_with_alt"]}/{latta_meta["images"]} | {fsi_meta["images_with_alt"]}/{fsi_meta["images"]} |
| H1 Count | {len(latta_meta["h1"])} | {len(fsi_meta["h1"])} |
| Mohawk Mention | {latta_scan["has_mohawk_text"]} | {fsi_scan["has_mohawk_text"]} |

## Discoverability Score

| Category | LATTA Floors | Flooring Solutions |
|---|---:|---:|
| Local SEO | {latta_score["Local SEO"]}/25 | {fsi_score["Local SEO"]}/25 |
| Content Quality | {latta_score["Content Quality"]}/25 | {fsi_score["Content Quality"]}/25 |
| Technical SEO | {latta_score["Technical SEO"]}/25 | {fsi_score["Technical SEO"]}/25 |
| AI Readiness | {latta_score["AI Readiness"]}/25 | {fsi_score["AI Readiness"]}/25 |
| **Total** | **{latta_score["Total"]}/100** | **{fsi_score["Total"]}/100** |

## Why LATTA Has Stronger Visibility

1. LATTA uses **LocalBusiness schema**, while Flooring Solutions uses generic **WebSite schema**.
2. LATTA page title directly targets **Flooring Store + Livermore, CA**.
3. LATTA has stronger local wording and more Livermore/service-area mentions.
4. LATTA has deeper homepage content.
5. LATTA has stronger internal linking.
6. LATTA has much better image alt text coverage.
7. Flooring Solutions appears more positioned as a commercial contractor than a local residential flooring store.

## Gap for Mohawk

Neither page mentions Mohawk on the homepage.

This is important because AI tools may not confidently associate either dealer with Mohawk products.

## First Recommendation for Flooring Solutions

Create or improve a local page targeting:

**Mohawk Flooring Dealer in Livermore, CA**

Suggested content:
- Mohawk flooring products
- Livermore service area
- Residential flooring
- Pet-friendly flooring
- Waterproof flooring
- Scratch-resistant flooring
- LocalBusiness schema
- FAQ schema
- Clear CTA: request quote / visit showroom

## Proof Status
Baseline evidence collected.

Next step:
Generate a v2 discoverability score using metadata + local signals + schema + content quality.
"""

out = REPORT_DIR / "latta-vs-flooring-solutions.md"
out.write_text(report.strip(), encoding="utf-8")

print(f"Updated report created: {out}")