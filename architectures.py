import torch
import torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, num_hidden = 128, num_layers = 1, context = 5, features = 9, dropout = 0.1) -> None:
        super().__init__()
        self.rnn = nn.GRU(features, num_hidden, num_layers, batch_first = True)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.dropout(x)
        output, state = self.rnn(x)
        return output, state

class PlainDecoder(nn.Module):
    def __init__(self, num_hidden = 128, num_layers = 1, context = 5, features = 9, dropout = 0.1) -> None:
        super().__init__()
        self.rnn = nn.GRU(features, num_hidden, num_layers, batch_first = True)
        self.dense = nn.Linear(num_hidden, 1)
        self.dropout = nn.Dropout(dropout)


    def forward(self, x, state):

        # x = self.dropout(x)
        output, state = self.rnn(x, state)
        output = self.dense(output)
        return output

class Seq2Seq(nn.Module):
    def __init__(self, num_hidden = 128, num_layers = 1, context = 5, features = 9, dropout = 0.1) -> None:
        super().__init__()
        self.encoder = Encoder()
        self.decoder = PlainDecoder()
    def forward(self, x):
        # print(x.shape)
        encoder_output, encoder_hidden = self.encoder(x)# hidden --> layer, batch, hidden dim
        most_recent_day = x[:,-1,:].unsqueeze(1) #batch, days, features
        output = self.decoder(most_recent_day, encoder_hidden).squeeze(2)
        return output


class PlainModel(nn.Module):
    def __init__(self, num_hidden = 128, num_layers = 1, context = 5, features = 9, dropout = 0.1) -> None:
        super().__init__()
        self.rnn = nn.GRU(features, num_hidden, num_layers, batch_first = True)
        self.dense = nn.Linear(num_hidden, 1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.dropout(x)
        output, state = self.rnn(x)
        output = self.dense(output)
        return output[:,-1]
