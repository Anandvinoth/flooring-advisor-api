from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from agent_service import ask_agent
import uuid
import json
import os

LEADS_FILE = "data/leads.json"

PRODUCT_IMAGES = {
    "Raise The Woof I": "/assets/images/raise-the-woof.jpeg",
    "Raise The Woof II": "/assets/images/raise-the-woof.jpeg",
    "Cozy Companion I": "/assets/images/cozy-companion.jpeg",
    "Cozy Companion III": "/assets/images/cozy-companion.jpeg",
    "Gentle Guardian I": "/assets/images/diffurent-choice.jpeg",
    "Purrsonality I": "/assets/images/diffurent-choice.jpeg",
   "Purrsonality III": "/assets/images/diffurent-choice.jpeg",
    "Diffurent Choice I": "/assets/images/raise-the-woof.jpeg",
    "Diffurent Choice III": "/assets/images/cozy-companion.jpeg",
    "Gentle Guardian II": "/assets/images/diffurent-choice.jpeg",
    "Canine Chic":"/assets/images/raise-the-woof.jpeg"
}

app = FastAPI(
    title="Flooring Advisor API",
    version="1.0.0",
    description="API for retailer lookup and lead capture for the Pet-Proof Flooring Advisor.",
    openapi_version="3.0.3"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4201",
        "https://<your-angular-site>.azurestaticapps.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

class Retailer(BaseModel):
    name: str
    city: str
    state: str
    zip: str
    phone: str
    distance_miles: float

class RetailerResponse(BaseModel):
    zip: str
    retailers: List[Retailer]

class LeadRequest(BaseModel):
    name: str
    email: EmailStr
    zip: str
    recommended_product: str
    customer_need: Optional[str] = None

class LeadResponse(BaseModel):
    status: str
    lead_id: str
    message: str

RETAILERS = [
    {"name": "Atlanta Flooring Design Centers", "city": "Kennesaw", "state": "GA", "zip": "30144", "phone": "770-555-1001", "distance_miles": 3.2},
    {"name": "Marietta Floor Gallery", "city": "Marietta", "state": "GA", "zip": "30066", "phone": "770-555-2002", "distance_miles": 8.6},
    {"name": "North Georgia Flooring", "city": "Acworth", "state": "GA", "zip": "30101", "phone": "678-555-3003", "distance_miles": 9.4},
    {"name": "Atlanta Home Flooring", "city": "Atlanta", "state": "GA", "zip": "30309", "phone": "404-555-4004", "distance_miles": 22.1}
]

LEADS = []

@app.post("/ask")
def ask(request: AskRequest):

    answer = ask_agent(
        request.question
    )

    data = json.loads(answer)

    recommendations = data.get(
        "recommendations",
        []
    )

    for item in recommendations:

        item["image_url"] = (
            PRODUCT_IMAGES.get(
                item.get("product_name"),
                "/assets/images/raise-the-woof.jpeg"
            )
        )

    return {
        "recommendations":
            recommendations
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/retailers", response_model=RetailerResponse)
def find_retailers(zip: str):
    return {
        "zip": zip,
        "retailers": sorted(RETAILERS, key=lambda r: r["distance_miles"])[:3]
    }

@app.post("/leads", response_model=LeadResponse)
def create_lead(lead: LeadRequest):

    leads = []

    if os.path.exists(LEADS_FILE):

        with open(LEADS_FILE, "r") as f:

            content = f.read().strip()

            if content:
                leads = json.loads(content)

    # Duplicate check

    for existing in leads:

        if (
            existing["email"].lower()
            == lead.email.lower()
            and
            existing["recommended_product"]
            == lead.recommended_product
        ):

            return {
                "status": "duplicate",
                "lead_id": existing["lead_id"],
                "message": "Lead already exists."
            }

    lead_id = "L-" + uuid.uuid4().hex[:8].upper()

    lead_record = {
        "lead_id": lead_id,
        "created_at": datetime.utcnow().isoformat(),
        **lead.dict()
    }

    leads.append(lead_record)

    with open(LEADS_FILE, "w") as f:
        json.dump(
            leads,
            f,
            indent=2
        )

    return {
        "status": "success",
        "lead_id": lead_id,
        "message": "Lead created successfully."
    }

@app.get("/leads")
def get_leads():

    if not os.path.exists(LEADS_FILE):
        return []

    with open(LEADS_FILE, "r") as f:
        content = f.read().strip()

    if not content:
        return []

    return json.loads(content)