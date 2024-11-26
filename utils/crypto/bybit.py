import aiohttp
import asyncio

class BybitApi:
    def __init__(self):
        self.urls = {
            "tickers": "https://api-testnet.bybit.com/v5/market/tickers?",
            "currencies": "https://api-testnet.bybit.com/v5/market/instruments-info?"
        }

    async def get_cost(self, category = "linear", symbol = "BTCUSDT", type_of_cost = "indexPrice"):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.urls.get('tickers')}category={category}&symbol={symbol}") as response:
                dict1 = await response.json()

                result = dict1.get("result")
                list1 = result.get("list")
                
                return list1[0].get(type_of_cost)

    async def get_currencies(self, category = "linear"):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.urls.get('currencies')}category={category}") as response:
                dict1 = await response.json()

                result = dict1.get("result")
                list1 = result.get("list")

                popular_currencies = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT",
                                      "BCHUSDT", "ADAUSDT", "DOTUSDT", "SOLUSDT"]

                symbols = [currency.get('symbol') for currency in list1 if currency.get('symbol') in popular_currencies]

                return symbols

# async def main():
#     bb = BybitApi()
#
#     res = await bb.get_cost(symbol="BTCUSDT")
#     print(res)
#
# asyncio.run(main())