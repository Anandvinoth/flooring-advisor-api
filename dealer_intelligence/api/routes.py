import re
from pathlib import Path

from fastapi import APIRouter, HTTPException

from dealer_intelligence.crawler import crawl_site
from dealer_intelligence.models.requests import DealerAnalysisRequest
from dealer_intelligence.services.business_listing_service import (
    analyze_business_listings,
)
from dealer_intelligence.services.social_presence_service import (
    analyze_social_presence,
)


router = APIRouter(
    prefix="/api/dealer-intelligence",
    tags=["Dealer Intelligence"],
)


def create_site_id(dealer_name: str) -> str:
    site_id = dealer_name.lower().strip()
    site_id = re.sub(r"[^a-z0-9]+", "-", site_id)
    return site_id.strip("-")


@router.post("/analyze")
async def analyze_dealer(request: DealerAnalysisRequest):
    site_id = create_site_id(request.dealer_name)
    dealer_url = str(request.url)

    try:
        await crawl_site(site_id, dealer_url)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to crawl dealer website: {exc}",
        ) from exc

    html_path = (
        Path("data")
        / "crawls"
        / site_id
        / "homepage.html"
    )

    if not html_path.exists():
        raise HTTPException(
            status_code=500,
            detail="Crawl completed but homepage.html was not created.",
        )

    social_presence = analyze_social_presence(html_path)
    business_listings = analyze_business_listings(html_path)

    return {
        "status": "success",
        "dealer": request.dealer_name,
        "site_id": site_id,
        "url": dealer_url,
        "scores": {
            "social_presence": social_presence,
            "business_listings": business_listings,
        },
    }