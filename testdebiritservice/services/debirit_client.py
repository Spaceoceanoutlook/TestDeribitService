import aiohttp
from settings import settings


class DeribitClient:
    async def get_index_price(self, ticker: str) -> float:
        url = f"{settings.deribit_base_url}/public/get_index_price"
        params = {"index_name": ticker}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Deribit API error: {response.status}")

                data = await response.json()

        if "result" not in data or "index_price" not in data["result"]:
            raise Exception(f"Unexpected Deribit response: {data}")
        price = data["result"]["index_price"]
        return price
