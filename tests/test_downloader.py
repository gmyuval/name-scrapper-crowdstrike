import pytest
import os
import tempfile
import aiohttp

from app.http_client import HttpClient
from app.models.animal import Animal
from app.downloader import Downloader


# Mock client for testing purposes
class MockHttpClient(HttpClient):
    async def fetch(self, url: str, session: aiohttp.ClientSession, is_text: bool = True):
        # When fetching the animal's page, return an HTML page with an infobox and an image tag.
        if "wiki" in url:
            return """
            <html>
                <body>
                    <table class="infobox">
                        <tr><td><img src="//fakeimage.jpg"/></td></tr>
                    </table>
                </body>
            </html>
            """
        # When fetching the image URL, return some fake image bytes.
        elif "fakeimage.jpg" in url:
            return b"fakeimagebytes"
        raise Exception("Unexpected URL in FakeHttpClient")


class TestDownloader:
    @pytest.mark.asyncio
    async def test_downloader_image_download(self, monkeypatch):
        # Use a temporary directory to override the IMAGE_DIR in config
        with tempfile.TemporaryDirectory() as temp_dir:
            animal = Animal(name="FakeAnimal", collateral_adjective="fakey", link="http://example.com/wiki/FakeAnimal")
            downloader = Downloader(http_client=MockHttpClient(), image_dir=temp_dir)

            async with aiohttp.ClientSession() as session:
                await downloader.download_image(animal, session)

            # Assert that the image_path is set and that the file was written
            assert animal.image_path is not None
            assert os.path.exists(animal.image_path)

            with open(animal.image_path, "rb") as f:
                content = f.read()
            assert content == b"fakeimagebytes"
