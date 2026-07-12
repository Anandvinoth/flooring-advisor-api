from pydantic import BaseModel, HttpUrl


class DealerAnalysisRequest(BaseModel):
    dealer_name: str
    url: HttpUrl
    city: str
    state: str
    zip_code: str | None = None