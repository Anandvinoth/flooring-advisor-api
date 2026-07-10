from pydantic import BaseModel, HttpUrl


class DealerAnalysisRequest(BaseModel):
    dealer_name: str
    url: HttpUrl