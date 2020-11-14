import requests
from time import time
from multiprocessing.pool import ThreadPool
import numpy as np
import datetime
from dateutil import parser


def test_get_response():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    date = datetime.datetime.now(datetime.timezone.utc)
    params = {
      'start':'1',
      'limit':'10',  
      'convert':'USD',
      'sort': "volume_24h",
      'sort_dir': "desc",
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '4e32f839-b0a5-4c0f-9013-a3b77c4e1536', 
    }

    start = time()
    r = requests.get(url, params=params, headers=headers)
    finish = time()

    assert r.status_code == 200, {**r.json(), ** params} 
    assert finish - start < 0.5, "Test proceeded more than 500 ms"
    for el in r.json()['data']:

        assert (date - parser.parse(el['last_updated'])).total_seconds() / 3600 < 24, f"outdated data: {el['last_updated']}"
    assert len(r.content) <= 10 * 1024, f"size of response content more than 10KB: {len(r.content)/1024}KB"
    return finish - start


def test_parallel():

    with ThreadPool(8) as p:
        times = list(p.starmap(test_get_response, [() for _ in range(8)]))


    assert len(times) / sum(times) > 5, f"rps is less than 5: {len(times) / sum(times)}"
    assert np.percentile(times, 80) < 0.45, f"0.8 percentile is more than 450 ms" 
