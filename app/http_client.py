import asyncio
import aiohttp

from app.config import CONCURRENT_REQUESTS_LIMIT, MAX_RETRIES, RETRY_BACKOFF


class HttpClient:
    def __init__(
        self,
        concurrency_limit: int = CONCURRENT_REQUESTS_LIMIT,
        max_retries: int = MAX_RETRIES,
        retry_backoff: float = RETRY_BACKOFF,
    ) -> None:
        self.concurrency_limit = concurrency_limit
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.semaphore = asyncio.Semaphore(concurrency_limit)  # We will use the semaphore to limit the number of connections

    async def fetch(self, url: str, session: aiohttp.ClientSession, is_text: bool = True) -> str | bytes | None:
        retries = self.max_retries
        for attempt in range(retries):
            async with self.semaphore:
                try:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        if is_text:
                            return await response.text()
                        else:
                            return await response.read()
                except Exception as e:
                    if attempt < retries - 1:
                        await asyncio.sleep(self.retry_backoff * (2**attempt))
                    else:
                        raise e
