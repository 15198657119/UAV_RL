import torch
import pandas as pd
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

######################################################################################################################
#读取数据，划分数据集以及输入输出
data = pd.read_csv(r'./generated1.csv')  # 读取数据并赋予列名
data = pd.read_csv(r'./data_co_1.csv')  # 读取数据并赋予列名
data = pd.read_csv(r'./data/generated.csv')  # 读取数据并赋予列名
print(data.shape)
#前250条数据作为训练数据，250后面的数据做测试数据
# #数据的12列到231列作为输入数据，231到271这40列数据作为输出
# train_x=data.iloc[1:250,12:231]
# train_y=data.iloc[1:250,231:271]
# test_x=data.iloc[250:,12:231]
# test_y=data.iloc[250:,231:271]
train_x=data.iloc[1:250,12:233]
train_y=data.iloc[1:250,234:475]
test_x=data.iloc[250:,12:233]
test_y=data.iloc[250:,234:475]


train_x=data.iloc[1:80,12:233]
train_y=data.iloc[1:80,234:475]
test_x=data.iloc[80:,12:233]
test_y=data.iloc[80:,234:475]



train_x= torch.unsqueeze(torch.FloatTensor(np.array(train_x).tolist()), dim=1)
train_y= torch.unsqueeze(torch.FloatTensor(np.array(train_y).tolist()), dim=1)
test_x= torch.unsqueeze(torch.FloatTensor(np.array(test_x).tolist()), dim=1)
test_y= torch.unsqueeze(torch.FloatTensor(np.array(test_y).tolist()), dim=1)


######################################################################################################################
#定义网络
class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.hidden1 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)
        self.hidden3 = torch.nn.Linear(n_hidden, n_hidden)
        #self.hidden4 = torch.nn.Linear(n_hidden, n_hidden)
        self.out = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))
        x = F.relu(self.hidden3(x))
        #x = F.relu(self.hidden4(x))
        x = self.out(x)
        return x

#按输入维度调用模型，定义学习率和损失函数
net = Net(221, 10, 241)
print(net)
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)  #0.05
loss_func = torch.nn.MSELoss()  # 均方差
x=train_x
y=train_y
a=0

########
#训练测试模型
for t in range(10000):
    prediction = net(x)

    loss = loss_func(prediction, y)  # 一定要prediction在前, y在后

    optimizer.zero_grad()  # 梯度降零
    loss.backward()
    optimizer.step()
    if t % 5 == 0:
	    # 数据测试
        print("loss",loss.data.numpy())
        a=net(test_x[1]).int()
        print("y_label",test_y[1].int())
        print("predict",a)
