import time
import requests
import os
import torch
from StockDataset import StockDataset
import architectures
import sys
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
model = architectures.Seq2Seq()
model.load_state_dict(torch.load('VanillaSeq2Seq.pt',map_location=torch.device('cpu')))
model.eval()

if not os.path.exists('predict/'):
    os.mkdir('predict/')
checking = "DKNG" if len(sys.argv) <= 1 else sys.argv[1].upper()

today = int(time.time())
# endPoint = 1577836800 #earlier date 2019
endPoint = 1609459200 #2020

url =f'https://query1.finance.yahoo.com/v7/finance/download/\
{checking}?period1={endPoint}&period2={today}&interval=1d&events=history&includeAdjustedClose=true'

try:
    res = requests.get(url, headers=headers, allow_redirects=True)
    open(f'predict/{checking}.csv', 'wb').write(res.content)

    print(f"Analyzing {checking}...")
    data = StockDataset("predict", checking)

    x = data.getLatest()

    x = x.unsqueeze(0)
    output = model(x)
    nextClose = data.reverse(output.item())
    previousClosings = [round(data.reverse(sample[4].item()), 2) if sample[4].item() != 0 else "LOWEST SINCE 2020" for sample in x.squeeze(0)]
    history = ""
    previousClosings.reverse()
    for i, day in enumerate(previousClosings):
        history+= f"{i+1} Day Ago: ${day}\n"
    print(history)
    print(f"Tomorrows closing price: ${round(nextClose, 2)}")
    if os.path.exists(f"predict/{checking}.csv"):
        os.remove(f"predict/{checking}.csv")
except:
    pass
    print("Error Grabbing {}".format(checking))