# import get_all_tickers
# from get_all_tickers import get_tickers
from get_all_tickers import get_tickers as gt
# import get_all_tickers

# print(gt.get_tickers(NYSE=True, NASDAQ=False, AMEX=False))
gt.save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv')