from pathlib import Path


class DealerPipeline:

    def __init__(self, site_id: str, url: str):

        self.site_id = site_id
        self.url = url

        self.output_dir = (
            Path("data")
            / "crawls"
            / site_id
        )

    def crawl(self):

        print(f"Crawling {self.url}")

    def extract(self):

        print("Extracting")

    def index(self):

        print("Indexing")

    def score(self):

        print("Scoring")

    def recommend(self):

        print("Recommendations")