from urllib.parse import urlparse

import requests


class SolrService:
    def __init__(
        self,
        base_url: str = "http://localhost:8983/solr",
        collection: str = "dealer_discoverability",
    ):
        self.collection_url = f"{base_url.rstrip('/')}/{collection}"

    def _query(self, params: dict) -> dict:
        response = requests.get(
            f"{self.collection_url}/select",
            params={
                **params,
                "wt": "json",
            },
            timeout=20,
        )

        response.raise_for_status()
        return response.json()

    def count_dealer_pages(self, dealer_url: str) -> int:
        hostname = urlparse(dealer_url).hostname or ""

        result = self._query({
            "q": f'host:"{hostname}"',
            "rows": 0,
        })

        return result["response"]["numFound"]

    def count_pages_containing(
        self,
        dealer_url: str,
        search_text: str,
    ) -> int:
        hostname = urlparse(dealer_url).hostname or ""

        result = self._query({
            "q": f'host:"{hostname}" AND content:"{search_text}"',
            "rows": 0,
        })

        return result["response"]["numFound"]

    def dealer_summary(
        self,
        dealer_url: str,
        city: str,
        brand_name: str = "Mohawk",
    ) -> dict:
        return {
            "indexed_pages": self.count_dealer_pages(dealer_url),
            "city_pages": self.count_pages_containing(
                dealer_url,
                city,
            ),
            "brand_pages": self.count_pages_containing(
                dealer_url,
                brand_name,
            ),
            "reviews_pages": self.count_pages_containing(
                dealer_url,
                "reviews",
            ),
            "financing_pages": self.count_pages_containing(
                dealer_url,
                "financing",
            ),
            "waterproof_pages": self.count_pages_containing(
                dealer_url,
                "waterproof",
            ),
        }