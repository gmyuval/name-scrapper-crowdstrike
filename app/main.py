import asyncio
from app.scraper import Scraper
from app.downloader import Downloader
from app.html_generator import HTMLGenerator
from app.config import WIKIPEDIA_BASE_URL


async def main_async() -> None:
    scraper = Scraper()
    print("Scraping animal data...")
    animals = await scraper.scrape(WIKIPEDIA_BASE_URL + "/wiki/List_of_animal_names")
    print(f"Found {len(animals)} animal adjective entries.")

    downloader = Downloader()
    print("Downloading images...")
    await downloader.download_images(animals)

    html_gen = HTMLGenerator()
    print("Generating HTML file...")
    html_gen.generate_html(animals)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
