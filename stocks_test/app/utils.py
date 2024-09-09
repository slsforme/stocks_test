from dateutil.relativedelta import relativedelta

from urllib.parse import urlencode
from typing import Dict, Optional 
from datetime import datetime

# datetime modules 
async def format_date(date: datetime) -> str:
    return date.strftime('%Y-%m-%d')

async def get_max_depth_date() -> str:
    max_deep_date = datetime.today() - relativedelta(years=2)

    return await format_date(max_deep_date)

async def url_builder(base_url: str, params: Dict) -> str:
    return base_url + urlencode(params)
