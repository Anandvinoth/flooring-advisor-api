from fastapi import APIRouter
from pathlib import Path

from dealer_intelligence.services.social_presence_service import (
    analyze_social_presence,
)
from dealer_intelligence.models.requests import DealerAnalysisRequest
from dealer_intelligence.models.responses import DealerAnalysisResponse


router = APIRouter(
    prefix="/api/dealer-intelligence",
    tags=["Dealer Intelligence"],
)

@router.post(
    "/analyze",
)
async def analyze_dealer(
    request: DealerAnalysisRequest,
):
    site_name = request.dealer_name.lower().replace(" ", "-")

    html_path = Path("data/crawls") / site_name / "homepage.html"

    if not html_path.exists():
        return {
            "status": "error",
            "dealer": request.dealer_name,
            "url": str(request.url),
            "message": "Crawl data not found for this dealer.",
        }

    social_presence = analyze_social_presence(html_path)

    return {
        "status": "success",
        "dealer": request.dealer_name,
        "url": str(request.url),
        "scores": {
            "social_presence": social_presence,
        },
    }