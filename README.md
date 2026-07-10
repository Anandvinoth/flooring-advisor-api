# Flooring Advisor API

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Test retailer lookup

```bash
curl "http://127.0.0.1:8000/retailers?zip=30144"
```

## Test lead creation

```bash
curl -X POST "http://127.0.0.1:8000/leads" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Smith","email":"john@example.com","zip":"30144","recommended_product":"PetPremier","customer_need":"3 dogs and easy cleaning"}'
```

## OpenAPI URL

```text
http://127.0.0.1:8000/openapi.json
```