from django.core.cache import cache

import aiohttp
import asyncio 
from typing import Dict
from datetime import datetime 

from stocks_test import settings
from .utils import url_builder, format_date, get_max_depth_date

_API_TOKEN: str = settings.API_TOKEN

async def fetch_data(ticker: str) -> str:
    current_date: str = await format_date(datetime.today())
    max_depth_date: str = await get_max_depth_date()

    if cache.get(f"{ticker}:{current_date}") is not None:
        settings.LOGGER.info(f"Gotten that info from cache - {ticker}:{current_date}")
        return cache.get(f"{ticker}:{current_date}")
    
    url: str = await url_builder(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{max_depth_date}/{current_date}?', { 'apiKey': _API_TOKEN })
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data: str = await response.json()
                settings.LOGGER.info(f"Data from API: {data} (info)")
                settings.LOGGER.info(f"Added that info to cache - {ticker}:{current_date}")
                cache.set(f"{ticker}:{current_date}", data)
                return data 
            else:
                response_text: str = await response.text()
                settings.LOGGER.info(f"Error occurred. Response code: \
                {response.status}. Response text: {response_text} (error)")
