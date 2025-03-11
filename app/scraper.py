import re
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

from app.config import WIKIPEDIA_BASE_URL
from app.http_client import HttpClient
from app.models.animal import Animal


class Scraper:
    def __init__(self, http_client: Optional[HttpClient] = None) -> None:
        self.http_client = http_client or HttpClient()

    async def fetch_page(self, url: str, session: aiohttp.ClientSession) -> str:
        return await self.http_client.fetch(url, session, is_text=True)

    @staticmethod
    def parse_table(table: BeautifulSoup) -> list[Animal]:
        results: list[Animal] = []
        header_cells = table.find("tr").find_all("th")
        headers = [cell.get_text(strip=True).lower() for cell in header_cells]
        animal_idx: Optional[int] = None
        collat_idx: Optional[int] = None

        for i, header in enumerate(headers):
            if header == "animal":
                animal_idx = i
            if "collateral" in header and "adjective" in header:
                collat_idx = i

        if animal_idx is None or collat_idx is None:
            return results

        rows = table.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) <= max(animal_idx, collat_idx):
                continue
            animal_cell = cells[animal_idx]
            adjective_cell = cells[collat_idx]
            animal_name = animal_cell.get_text(strip=True)
            a_tag = animal_cell.find("a")
            animal_link: Optional[str] = None
            if a_tag and a_tag.get("href"):
                animal_link = WIKIPEDIA_BASE_URL + a_tag.get("href")
            adjectives_text = adjective_cell.get_text(strip=True)
            adjectives = [adj.strip() for adj in re.split(r"[;,]", adjectives_text) if adj.strip()]
            for adj in adjectives:
                results.append(Animal(name=animal_name, collateral_adjective=adj, link=animal_link))
        return results

    async def scrape(self, url: str) -> list[Animal]:
        animals: list[Animal] = []
        async with aiohttp.ClientSession() as session:
            page_text = await self.fetch_page(url, session)
            soup = BeautifulSoup(page_text, "html.parser")
            tables = soup.find_all("table", class_="wikitable")
            for table in tables:
                animals.extend(self.parse_table(table))
        return animals
