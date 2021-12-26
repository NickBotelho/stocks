tickers_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
def getTickers():
    tickers = []
    with open("tickers.txt", "r") as file:
        for line in file:
            i = line.index("|")
            tick = line[:i]
            tickers.append(tick)
    return tickers




