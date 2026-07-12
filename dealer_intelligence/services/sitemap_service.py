from urllib.parse import urljoin, urlparse
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

class SitemapService:

    def __init__(self, dealer_url: str):

        self.dealer_url = dealer_url.rstrip("/")

    def select_discoverability_urls(urls: list[str]) -> list[str]:
        selected = []

        excluded_paths = {
            "thank-you-5",
            "thank-you-contact",
            "thank-you-estimate",
            "thank-you-products",
            "search",
        }

        for url in urls:
            path = urlparse(url).path.strip("/")

            if path.startswith("d/"):
                continue

            if path in excluded_paths:
                continue

            selected.append(url)

        return sorted(set(selected))

    def write_seed_file(site_id: str,urls: list[str],
        ) -> Path:
        seed_dir = Path("data") / "nutch" / site_id / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)

        seed_file = seed_dir / "urls"
        seed_file.write_text(
            "\n".join(sorted(set(urls))) + "\n",
            encoding="utf-8",
        )
        return seed_file

    def discover(self):

        robots_url = f"{self.dealer_url}/robots.txt"

        sitemap_urls = []

        try:
            response = requests.get(
                robots_url,
                timeout=20,
                headers={"User-Agent": "Mozilla/5.0"},
            )

            if response.ok:

                for line in response.text.splitlines():

                    if line.lower().startswith("sitemap:"):
                        sitemap_path = line.split(":", 1)[1].strip()

                        sitemap_urls.append(
                            urljoin(self.dealer_url + "/", sitemap_path)
                        )

        except Exception:
            pass

        if not sitemap_urls:
            sitemap_urls.append(
                f"{self.dealer_url}/sitemap.xml"
            )

        return sitemap_urls

    def parse(self, sitemap_url):

        response = requests.get(
            sitemap_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)

        tag = root.tag.split("}")[-1]

        urls = []

        if tag == "sitemapindex":

            for loc in root.iter():

                if loc.tag.endswith("loc"):

                    urls.extend(
                        self.parse(loc.text.strip())
                    )

        elif tag == "urlset":

            for loc in root.iter():

                if loc.tag.endswith("loc"):

                    host = urlparse(loc.text).hostname

                    if host and host.endswith(
                        urlparse(self.dealer_url).hostname
                    ):

                        urls.append(loc.text.strip())

        return sorted(set(urls))

def select_discoverability_urls(urls: list[str]) -> list[str]:
    selected = []

    excluded_paths = {
        "thank-you-5",
        "thank-you-contact",
        "thank-you-estimate",
        "thank-you-products",
        "search",
    }

    for url in urls:
        path = urlparse(url).path.strip("/")

        if path.startswith("d/"):
            continue

        if path in excluded_paths:
            continue

        selected.append(url)

    return sorted(set(selected))


def write_seed_file(
    site_id: str,
    urls: list[str],
) -> Path:
    seed_dir = Path("data") / "nutch" / site_id / "seed"
    seed_dir.mkdir(parents=True, exist_ok=True)

    seed_file = seed_dir / "urls"
    seed_file.write_text(
        "\n".join(sorted(set(urls))) + "\n",
        encoding="utf-8",
    )

    return seed_file
