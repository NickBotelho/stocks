import json
import requests
import time
import csv
import multiprocessing
tickers = ['F', "GE", "AAPL"]

def getStockPrice(ticker):
    print("Getting {}...".format(ticker))
    start = '2010-01-01'
    end = '2021-12-25'
    limit = 5000

    url = f'https://api.polygon.io\
/v2/aggs/ticker/{ticker}/range/1/day/\
{start}/{end}?adjusted=true&sort=desc&limit={limit}&apiKey=fPcPy4ipOKuWrH9iGBPB8GwJA23WqNdw'

    res = requests.get(url)
    res = res.json()
    res = res['results']

    header = ["Volume", "Open", "Close", "High", "Low", "Transactions"]

    with open(f"{ticker}.csv", 'w') as file:
        file = csv.writer(file)
        file.writerow(header)
        for day in res:
            file.writerow([day['v'], day['o'], day['c'], day['h'], day['l'], day['n']])
    return

if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        p.map(getStockPrice, tickers)

