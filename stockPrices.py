import json
import requests
import time
import csv
import threading
import tqdm
from datetime import datetime
from tickers import getTickers
# tickers = ['F', "GE", "AAPL"]

def getStockPrice(ticker):
    # print("Getting {}...".format(ticker))
    start = '2010-01-01'
    end = '2021-12-25'
    limit = 5000

    url = f'https://api.polygon.io\
/v2/aggs/ticker/{ticker}/range/1/day/\
{start}/{end}?adjusted=true&sort=desc&limit={limit}&apiKey=fPcPy4ipOKuWrH9iGBPB8GwJA23WqNdw'
    try:
        res = requests.get(url)
        res = res.json()
        res = res['results']
        header = ["Volume", "Open", "Close", "High", "Low", "Transactions", 'weekday','day','month']

        with open(f"data/{ticker}.csv", 'w') as file:
            file = csv.writer(file)
            file.writerow(header)
            for day in res:
                unixTime = datetime.fromtimestamp(day['t']/1000)
                weekday = unixTime.weekday() #sun = 6
                mday = unixTime.day
                month = unixTime.month
                file.writerow([day['v'], day['o'], day['c'], day['h'], day['l'], day['n'], weekday, mday, month])
    except:
        pass
        # print("Error Grabbing {}".format(ticker))
    finally:
        return

# if __name__ == '__main__':
#     tickers = getTickers()
#     with multiprocessing.Pool(5) as p:
#         p.map(getStockPrice, tickers[:200])

tickers = getTickers()
i = 0

for ticker in tqdm.tqdm(tickers):
    t = threading.Thread(target=getStockPrice, args=((ticker,)))
    t.start()
    i+=1
    if i % 5 == 0:
        # print('sleeping..')
        time.sleep(61)
        i=0

