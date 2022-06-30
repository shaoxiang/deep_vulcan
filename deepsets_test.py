import math
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data.dataset import Dataset
from torch import FloatTensor
from typing import Tuple
from sklearn import preprocessing

class GNSSDATA(Dataset):
    def __init__(self):
        pass

    def __len__(self) -> int:
        return 0

    def __getitem__(self, item: int, flag: int) -> Tuple[FloatTensor, FloatTensor]:
        if flag:
            X = np.random.randint(-1, 1, size=(np.random.randint(4,50), 10))
        else:
            X = np.random.randint(-1, 1, size=(np.random.randint(1,60), 10))

        # deepsets
        Y = X.sum()
        # lable pred
        # Y = X.sum(axis = 1)

        # X = preprocessing.normalize(X)
        # return True, torch.FloatTensor(X), torch.FloatTensor(Y.reshape(-1,1))
        return True, torch.FloatTensor(X), torch.FloatTensor([Y])


train_len_ = 20000
test_len_ = 10000

print("train_len:", train_len_, "test_len:", test_len_)

train_data_x = []
train_data_y = []
test_data_x = []
test_data_y = []

train_data = GNSSDATA()

for i in range(train_len_):
    flag, x, target = train_data.__getitem__(i, 1)

    if flag:
        train_data_x.append(x)
        train_data_y.append(target)

test_data = GNSSDATA()

for i in range(test_len_):
    flag, x, target = test_data.__getitem__(i, 0)
    if flag:
        test_data_x.append(x)
        test_data_y.append(target)

train_len = len(train_data_y)
test_len = len(test_data_y)

########################################################
# DeepSets (src: https://github.com/yassersouri/pytorch-deep-sets)       
class InvariantModel(nn.Module):
    def __init__(self, phi: nn.Module, rho: nn.Module):
        super().__init__()
        self.phi = phi
        self.rho = rho

    def forward(self, x):
        # compute the representation for each data point
        x = self.phi.forward(x)
        # sum up the representations
        
        # deepsets
        x = torch.sum(x, dim=0, keepdim=False)

        # compute the output
        out = self.rho.forward(x)
        return out

class SmallPhi(nn.Module):
    def __init__(self, input_size: int, output_size: int = 1, hidden_size: int = 10):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size

        self.fc1 = nn.Linear(self.input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, self.output_size)

    def forward(self, x):
        x1 = F.tanhshrink(self.fc1(x))
        x2 = self.fc2(x1)
        return x2

class SmallRho(nn.Module):
    def __init__(self, input_size: int, output_size: int = 1, hidden_size: int = 10):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size

        self.fc1 = nn.Linear(self.input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, self.output_size)

    def forward(self, x):
        x1 = F.tanhshrink(self.fc1(x))
        x2 = F.hardtanh(self.fc2(x1), min_val = -1000.0, max_val = 1000.0)
        return x2
        
class DeepSetModel(nn.Module):
    def __init__(self, input_size: int, output_size: int = 1, hidden_size: int = 100):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        
        phi = SmallPhi(self.input_size, self.hidden_size, self.hidden_size)
        rho = SmallRho(self.hidden_size, self.output_size, self.hidden_size)
        self.net = InvariantModel(phi, rho)
    
    def forward(self, x, pad_mask=None):
        out = self.net.forward(x)
        return out

net = DeepSetModel(10, 1, 40)
print(net)

for name, parameters in net.named_parameters():
    print(name, ':', parameters.size())

optimizer = torch.optim.AdamW(net.parameters())

if torch.cuda.is_available():
    net.cuda()

loss_func = torch.nn.MSELoss()

accumulation_steps = 5

def train_1_item(item_number):
    x, target = train_data_x[item_number], train_data_y[item_number]
    if torch.cuda.is_available():
        x, target = x.cuda(), target.cuda()

    x, target = Variable(x), Variable(target)

    pred = net.forward(x)

    the_loss = F.mse_loss(pred, target)

    if item_number == 0:
        print("train:", pred, "loss:", the_loss, "target:", target)

    the_loss.backward()
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)

    the_loss_tensor = the_loss.data
    if torch.cuda.is_available():
        the_loss_tensor = the_loss_tensor.cpu()

    the_loss_numpy = the_loss_tensor.numpy().flatten()
    the_loss_float = float(the_loss_numpy[0])
    return the_loss_float

def train_1_epoch(epoch_num):
    net.train()
    loss_sum = 0
    for i in tqdm(range(train_len)):
        loss = train_1_item(i)
        loss_sum += loss
    print("epoch:",epoch_num, 'loss:', loss_sum / train_len_)

def evaluate():
    net.eval()
    loss_sum = 0
    for i in range(test_len):
        x, target = test_data_x[i], test_data_y[i]
        if torch.cuda.is_available():
            x, target = x.cuda(), target.cuda()
        
        pred = net.forward(x)

        the_loss = F.mse_loss(pred, target)
        the_loss_tensor = the_loss.data

        if torch.cuda.is_available():
            the_loss_tensor = the_loss_tensor.cpu()

        the_loss_numpy = the_loss_tensor.numpy().flatten()
        the_loss_float = float(the_loss_numpy[0])

        if i == 0:
            print("evl:", pred, "loss:", the_loss, "target:", target)

        loss_sum += the_loss_float

    print("Evl loss:",  loss_sum / test_len_)

for epoch in range(20000):
    train_1_epoch(epoch)
    evaluate()
    if (epoch + 1) % 100 == 0:
        torch.save(net, 'deep_gnss.pth')