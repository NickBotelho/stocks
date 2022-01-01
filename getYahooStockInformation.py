import json
import requests
import time
import csv
import threading
import tqdm
from datetime import datetime
from tickers import getTickers

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def getStockPrice(ticker):
    # print("Getting {}...".format(ticker))
    start = 1262304000 #2010
    end = 1640476800 #2021

    url =f'https://query1.finance.yahoo.com/v7/finance/download/\
{ticker}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true'
    try:
        res = requests.get(url, headers=headers, allow_redirects=True)
        open(f'data/{ticker}.csv', 'wb').write(res.content)
    except:
        pass
        # print("Error Grabbing {}".format(ticker))
    finally:
        return



tickers = getTickers()
i = 0
rm = tickers.index("SDACU")
tickers = tickers[rm:]
for ticker in tqdm.tqdm(tickers):
    t = threading.Thread(target=getStockPrice, args=((ticker,)))
    t.start()
    i+=1
    if i % 5 == 0:
        # print('sleeping..')
        time.sleep(5)
        i=0

