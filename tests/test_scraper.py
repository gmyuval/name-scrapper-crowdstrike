import pytest
from bs4 import BeautifulSoup
from app.scraper import Scraper
from app.models.animal import Animal


class TestScraper:
    def test_parse_table_single_adjective(self):
        html = """
        <table class="wikitable">
          <tr>
            <th>Animal</th>
            <th>Collateral adjectives</th>
          </tr>
          <tr>
            <td><a href="/wiki/Lion">Lion</a></td>
            <td>leo</td>
          </tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="wikitable")
        data = Scraper.parse_table(table)
        expected = [Animal(name="Lion", collateral_adjective="leo", link="https://en.wikipedia.org/wiki/Lion")]
        assert data == expected

    def test_parse_table_multiple_adjectives(self):
        html = """
        <table class="wikitable">
          <tr>
            <th>Animal</th>
            <th>Collateral adjectives</th>
          </tr>
          <tr>
            <td><a href="/wiki/Cow">Cow</a></td>
            <td>bovine; cowish</td>
          </tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="wikitable")
        data = Scraper.parse_table(table)
        expected = [
            Animal(name="Cow", collateral_adjective="bovine", link="https://en.wikipedia.org/wiki/Cow"),
            Animal(name="Cow", collateral_adjective="cowish", link="https://en.wikipedia.org/wiki/Cow"),
        ]
        assert data == expected
