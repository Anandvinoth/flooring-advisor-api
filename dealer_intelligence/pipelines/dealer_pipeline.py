from dealer_intelligence.services.nutch_service import NutchService
from dealer_intelligence.services.sitemap_service import (
    SitemapService,
    select_discoverability_urls,
    write_seed_file,
)


class DealerPipeline:
    def __init__(
        self,
        site_id: str,
        dealer_url: str,
    ):
        self.site_id = site_id
        self.dealer_url = dealer_url

    def run(self, crawl_rounds: int = 2) -> dict:
        sitemap_service = SitemapService(self.dealer_url)

        sitemap_urls = sitemap_service.discover()

        all_urls = []

        for sitemap_url in sitemap_urls:
            all_urls.extend(
                sitemap_service.parse(sitemap_url)
            )

        selected_urls = select_discoverability_urls(all_urls)

        if not selected_urls:
            selected_urls = [self.dealer_url]

        seed_file = write_seed_file(
            site_id=self.site_id,
            urls=selected_urls,
        )

        nutch_service = NutchService(
            site_id=self.site_id,
            dealer_url=self.dealer_url,
        )

        filter_file = nutch_service.prepare_filter()
        nutch_service.copy_inputs()
        nutch_service.crawl(rounds=crawl_rounds)
        nutch_service.index()

        return {
            "status": "success",
            "site_id": self.site_id,
            "dealer_url": self.dealer_url,
            "sitemaps_found": sitemap_urls,
            "sitemap_url_count": len(set(all_urls)),
            "selected_url_count": len(selected_urls),
            "seed_file": str(seed_file),
            "filter_file": str(filter_file),
            "crawl_rounds": crawl_rounds,
            "message": "Dealer website crawled and indexed successfully.",
        }