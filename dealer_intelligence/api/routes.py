import re
from pathlib import Path
from dealer_intelligence.extractor import extract_site
from fastapi import APIRouter, HTTPException
from dealer_intelligence.site_scanner import scan_site
from dealer_intelligence.crawler import crawl_site
from dealer_intelligence.models.requests import DealerAnalysisRequest
from dealer_intelligence.services.business_listing_service import (
    analyze_business_listings,
)
from dealer_intelligence.services.social_presence_service import (
    analyze_social_presence,
)
from dealer_intelligence.services.local_seo_service import (
    analyze_local_seo,
)
from dealer_intelligence.pipelines.dealer_pipeline import DealerPipeline

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

    metadata = extract_site(
        site_id=site_id,
        dealer_url=dealer_url,
        city=request.city,
        state=request.state,
    )

    site_scan = scan_site(
        site_id=site_id,
        base_url=dealer_url,
        city=request.city,
        state=request.state,
    )

    local_seo = analyze_local_seo(
        metadata=metadata,
        site_scan=site_scan,
    )

    pipeline = DealerPipeline(
        site_id=site_id,
        dealer_url=dealer_url,
    )

    pipeline_result = pipeline.run(crawl_rounds=2)

    return {
        "status": "success",
        "dealer": request.dealer_name,
        "site_id": site_id,
        "url": dealer_url,
        "scores": {
            "social_presence": social_presence,
            "business_listings": business_listings,
        },
        "evidence": {
            "website_metadata": metadata,
            "site_scan": site_scan,
            "local_seo": local_seo,
            "pipeline": pipeline_result,
        },
    }