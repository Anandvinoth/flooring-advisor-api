import asyncio
from pathlib import Path
from crawl4ai import AsyncWebCrawler

SITES = {
    "lattafloors": "https://www.lattafloors.com",
    "flooring-solutions": "https://www.flooring-solutions.com",
}

BASE_DIR = Path(__file__).resolve().parents[1]
CRAWL_DIR = BASE_DIR / "data" / "crawls"


async def crawl_site(name: str, url: str):
    output_dir = CRAWL_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)

        print(result.success)
        print(result.status_code)
        print(result.error_message)

        (output_dir / "homepage.html").write_text(
            result.html or "",
            encoding="utf-8"
        )

        (output_dir / "homepage.md").write_text(
            result.markdown or "",
            encoding="utf-8"
        )

        print(f"Saved crawl for {name}: {url}")


async def main():
    for name, url in SITES.items():
        await crawl_site(name, url)


if __name__ == "__main__":
    asyncio.run(main())