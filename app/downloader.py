import os
import aiohttp
import asyncio
import re
from typing import List, Optional
from bs4 import BeautifulSoup
from app.models.animal import Animal
from app.config import IMAGE_DIR
from app.http_client import HttpClient


class Downloader:
    def __init__(self, http_client: Optional[HttpClient] = None, image_dir: str = IMAGE_DIR) -> None:
        """
        Initialize the Downloader with an optional custom image directory.
        :param http_client: An instance of HttpClient for making HTTP requests.
        :param image_dir: Directory where images should be saved (default: config.IMAGE_DIR).
        """
        self.http_client = http_client or HttpClient()
        self.image_dir = image_dir
        os.makedirs(self.image_dir, exist_ok=True)  # Ensure the directory exists

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Replace problematic characters in filenames with underscores to ensure valid filenames.
        """
        return re.sub(r'[<>:"/\\|?*]', "_", name)

    async def download_image(self, animal: Animal, session: aiohttp.ClientSession) -> None:
        """
        Download the first image found in the Wikipedia infobox for the given animal.
        :param animal: The Animal object containing the Wikipedia link.
        :param session: An aiohttp ClientSession instance.
        """
        if not animal.link:
            return
        try:
            page_text = await self.http_client.fetch(animal.link, session, is_text=True)
            soup = BeautifulSoup(page_text, "html.parser")
            infobox = soup.find("table", class_="infobox")
            if infobox:
                img = infobox.find("img")
                if img and img.get("src"):
                    src = img.get("src")
                    img_url = "https:" + src if src.startswith("//") else src
                    img_bytes = await self.http_client.fetch(img_url, session, is_text=False)

                    ext = os.path.splitext(img_url)[1]
                    if not ext:
                        ext = ".jpg"  # Default to JPG if no extension detected

                    # Ensure filename is valid
                    safe_name = self.sanitize_filename(animal.name)
                    file_path = os.path.join(self.image_dir, f"{safe_name}{ext}")

                    with open(file_path, "wb") as f:
                        f.write(img_bytes)

                    animal.image_path = file_path  # Update the animal object with image path

        except Exception as e:
            print(f"Error downloading image for {animal.name}: {e}")

    async def download_images(self, animals: List[Animal]) -> None:
        """
        Download images for all animals asynchronously.
        :param animals: List of Animal objects.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.download_image(animal, session) for animal in animals]
            await asyncio.gather(*tasks)
