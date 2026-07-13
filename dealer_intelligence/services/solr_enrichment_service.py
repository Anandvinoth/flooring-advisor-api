import re
from urllib.parse import urlparse

import requests

from dealer_intelligence.services.page_classifier import classify_page


def count_phrase(text: str, phrase: str) -> int:
    if not phrase or not phrase.strip():
        return 0

    pattern = rf"\b{re.escape(phrase.strip())}\b"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


class SolrEnrichmentService:
    def __init__(
        self,
        base_url: str = "http://localhost:8983/solr",
        collection: str = "dealer_discoverability",
    ):
        self.collection_url = f"{base_url.rstrip('/')}/{collection}"

    def enrich_dealer_pages(
        self,
        dealer_url: str,
        city: str,
        brand_name: str = "Mohawk",
    ) -> dict:
        hostname = urlparse(dealer_url).hostname or ""

        response = requests.get(
            f"{self.collection_url}/select",
            params={
                "q": f'host:"{hostname}"',
                "fl": "id,url,title,content",
                "rows": 10000,
                "wt": "json",
            },
            timeout=30,
        )
        response.raise_for_status()

        documents = response.json()["response"]["docs"]
        updates = []

        for document in documents:
            document_id = document["id"]

            url_value = document.get("url", document_id)
            if isinstance(url_value, list):
                url_value = url_value[0] if url_value else document_id

            content = document.get("content", "")
            if isinstance(content, list):
                content = " ".join(content)

            title = document.get("title", "")
            if isinstance(title, list):
                title = " ".join(title)

            combined_text = f"{title} {content}"

            updates.append(
                {
                    "id": document_id,
                    "page_type": {"set": classify_page(url_value)},
                    "word_count": {
                        "set": len(content.split())
                    },
                    "city_mentions": {
                        "set": count_phrase(combined_text, city)
                    },
                    "brand_mentions": {
                        "set": count_phrase(combined_text, brand_name)
                    },
                    "has_reviews_signal": {
                        "set": (
                            "review" in url_value.lower()
                            or "review" in title.lower()
                        )
                    },
                    "has_financing_signal": {
                        "set": (
                            "financing" in url_value.lower()
                            or "financing" in title.lower()
                        )
                    },
                    "has_contact_signal": {
                        "set": (
                            "contact" in url_value.lower()
                            or "contact" in title.lower()
                        )
                    },
                }
            )

        if updates:
            update_response = requests.post(
                f"{self.collection_url}/update",
                params={"commit": "true"},
                json=updates,
                timeout=30,
            )
            update_response.raise_for_status()

        return {
            "hostname": hostname,
            "documents_found": len(documents),
            "documents_updated": len(updates),
        }