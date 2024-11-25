import aiohttp
import asyncio

class CryptoRank:
    def __init__(self, key: str):
        self.key = key
        self.urls = {
            "crypto_curriences": "https://api.cryptorank.io/v2/currencies"
        }
        self.headers = {
            "X-Api-Key": key
        }

    async def get_cryptocurriences(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.urls.get("crypto_curriences"), headers=self.headers) as response:
                result = await response.json()

                dicts = result.get("data")
                names = [dict1.get("symbol") for dict1 in dicts]

                return names

async def main():
    cr = CryptoRank(key="5ecfe312d22cf431184cb88c7d0299ee3b67c6707effc64e4f4dae159fd5")

    curr = await cr.get_cryptocurriences()

    print(curr)

if __name__ == "__main__":
    asyncio.run(main())