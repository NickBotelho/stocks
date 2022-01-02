import torch
import pandas as pd
import numpy as np
import datetime
from torch.utils.data import Dataset

class StockDataset(Dataset):
    def __init__(self, directory, ticker, context = 5) -> None:
        super().__init__()
        self.info = []
        self.context = context

        self.info = pd.read_csv(f"{directory}/{ticker}.csv")

        self.info = np.array(self.info.values.tolist())
        self.feature_peaks = {}
                
        if len(self.info) > 1:
            for feature_col in range(1, len(self.info[0,:])):
                col = self.info[:,feature_col].astype(np.double)
                high, low, col = self.norm(col)
                self.info[:,feature_col] = col
                self.feature_peaks[feature_col] = (low, high)

    def __len__(self):
        return len(self.info) - self.context if len(self.info) > self.context else len(self.info)
    def __getitem__(self, index):
        index+=self.context
        res = []

        for day in self.info[index-self.context: index]:
            time = self.transformDay(day[0])
            res.append(np.concatenate((day[1:].astype(np.double) , time), axis = 0))
            # res.append(day[1:])

        
        previousDays = torch.Tensor(res)
        closingPrice = torch.tensor(float(self.info[index][4])).float()
        return previousDays, closingPrice
    def transformDay(self, date):

        dt = datetime.datetime.strptime(date, "%Y-%m-%d")
        res = [dt.weekday(), dt.day, dt.month]
        return np.array(res)
    def norm(self, feature):
        high, low = max(feature), min(feature)
        for i in range(len(feature)):
            feature[i] = round(((feature[i]-low)/(high-low)), 4)
        return high, low, feature
    def reverse(self, output):
        return ((output)*(self.feature_peaks[4][1]-self.feature_peaks[4][0])) + self.feature_peaks[4][0]
    def getLatest(self):
        res = []

        for day in self.info[len(self.info)-self.context: len(self.info)]:
            time = self.transformDay(day[0])
            res.append(np.concatenate((day[1:].astype(np.double) , time), axis = 0))
            # res.append(day[1:])

        res = np.array(res)
        previousDays = torch.Tensor(res)
        return previousDays


