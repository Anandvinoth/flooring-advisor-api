from fastapi import APIRouter

from dealer_intelligence.models.requests import DealerAnalysisRequest
from dealer_intelligence.models.responses import DealerAnalysisResponse


router = APIRouter(
    prefix="/api/dealer-intelligence",
    tags=["Dealer Intelligence"],
)


@router.post(
    "/analyze",
    response_model=DealerAnalysisResponse,
)
async def analyze_dealer(
    request: DealerAnalysisRequest,
) -> DealerAnalysisResponse:
    return DealerAnalysisResponse(
        status="success",
        dealer=request.dealer_name,
        url=str(request.url),
        message="Dealer analysis request accepted.",
    )