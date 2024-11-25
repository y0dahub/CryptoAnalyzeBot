from pybit.unified_trading import HTTP
from cryptorank import CryptoRank

import asyncio
import aiohttp

class BybitApi:
    def __init__(self):
        self.urls = {
            "tickers": "https://api-testnet.bybit.com/v5/market/tickers?"
        }


    async def get_tickers(self, category = "linear", symbol = "BTCUSDT", type_of_cost = "indexPrice"):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.urls.get("tickers")}category={category}&symbol={symbol}") as response:
                dict1 = await response.json()

                result = dict1.get("result")
                list1 = result.get("list")
                
                return list1[0].get(type_of_cost)

    