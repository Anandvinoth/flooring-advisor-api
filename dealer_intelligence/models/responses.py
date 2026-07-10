from pydantic import BaseModel


class DealerAnalysisResponse(BaseModel):
    status: str
    dealer: str
    url: str
    message: str