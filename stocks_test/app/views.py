from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

import asyncio
import pandas as pd
import asyncio
from typing import Coroutine
from http import HTTPStatus

from .parser import fetch_data


def home(request: HttpRequest) -> render:
    try:
        data: str = asyncio.run(fetch_data('AAPL'))  # AAPL по дефолту

        chart_data_json = get_chart_data(data)

        return render(request, 'app/index.html', {'chart_data': chart_data_json})
    except Exception as e:
        print(e)

def switch_ticker(ticker: str) -> str:
    loop: Coroutine = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data: str = ""
    try:
        data = asyncio.run(fetch_data(ticker))
    finally:    
        loop.close()
    
    return data


@require_POST
def send_chart_data(request: HttpRequest):
    ticker: str = request.POST.get('ticker')
    
    data: str = switch_ticker(ticker)

    df_data: str = get_chart_data(data)

    return JsonResponse({'df_data' : df_data})
    
    
def get_chart_data(data: str) -> str:
    df = pd.DataFrame(data['results'])
    df = df.rename(columns={
        'v': 'volume',
        'vw':'volume_weighted_price',
        'o': 'open_price',
        'c': 'close_price',
        'h': 'high_price',
        'l': 'low_price',
        't': 'timestamp',
        'n': 'number_of_trades'
    })

    return df[['timestamp', 'open_price', 'high_price', 'low_price', 'close_price']].to_json(orient='records')

