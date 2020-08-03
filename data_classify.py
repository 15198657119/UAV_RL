import  numpy as np
# from Sources.RaplPowerSource import *
# from get_system_state import *
# #from freq_setting_tool_master.new_freq_set import *
# import matplotlib.pyplot as plt
# import pandas as pd
# from sklearn import linear_model
import os

def get_data():
    cmdline = "sudo python set_cpu_freq.py"
    var = os.popen(cmdline).read()
    s = []
    s1=  []
    s2=[]
    message = var.split()
    # print(message)
    for i in range(len(message)):
        if message[i] == "frequency:":
            s.append(message[i + 1])
            s1.append(message[i + 1])

    cmdline = "top -bi -n 8 -d 0.02"
    var = os.popen(cmdline).read()
    message = var.split()
    for i in range(len(message)):
        if message[i] == "%Cpu(s):":
            s.append(message[i + 1])
            s1.append(message[i + 1])
            #s.append(message[i + 1])

    if len(s)<16:
        s.append(0)

    rapl = RaplPowerSource()
    power = rapl.get_summary()
    print("power", power)
    power = power["Max Power"]
    print("power_type",type(power))

    power=power.split()
    s1.append(power[0])
    # s1 = [float(s1) for x in s1]
    # s1 = matrix(s1)
    print("s1",s1)

    # print("power", power)
    # #power = float(power.split()[0])
    # print(type(power))
    # s = [float(x) for x in s]
    # print("s",s)
    #print("s1",s1)
    return s1 #,s1

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')+"   "#去除[],这两行按数据不同，可以选择
        #s = s.replace("'",' ').replace(',',' ')    #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.write("\n")
    file.close()
    print("保存文件成功")


def loadDataSet(fileName):  # 解析文件，按tab分割字段，得到一个浮点数字类型的矩阵
    dataMat = []              # 文件的最后一个字段是类别标签
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(' ')
        print("cur",curLine)
        fltLine = list(map(float, curLine))    # 将每个元素转成float类型

        dataMat.append(fltLine)
#     return dataMat
#
#
#x=loadDataSet("clasify_data.txt")


# df=pd.read_csv("clasify_data.csv",header=None)
# print(df.shape)
# print(type(df))
# df=df[0].str.split('  ',8,True)
# y=df[8]
# print(y)
# x=df[:][:7]
# print(x)

#pd.concat([df,df[0].str.split('  ',9,True)],axis=1)
# print(df.shape)
#names=['u1','u2','u3','u4','u5','u6','u7','u8','power']
# df=pd.read_table("clasify_data.txt",header=None,)
# print("df_type",type(df))
# print(df.ix[0:3,0:1])
#
# print(type(df))
# print(df.shape)

#y=df[['power']]

#model=linear_model.LinearRegression()
#model.fit()

def read_text_data():
    data = []
    y1=[]
    with open("clasify_data.txt") as file:
        for line in file:
            d = []
            y=[]
            # d.append(float(x) for x in line.split()[0:8])
            d.append(float(line.split()[0]))
            d.append(float(line.split()[1]))
            d.append(float(line.split()[2]))
            d.append(float(line.split()[3]))
            d.append(float(line.split()[4]))
            d.append(float(line.split()[5]))
            d.append(float(line.split()[6]))
            d.append(float(line.split()[7]))
            d.append(float(line.split()[8]))
            d.append(float(line.split()[9]))
            d.append(float(line.split()[10]))
            d.append(float(line.split()[11]))
            d.append(float(line.split()[12]))
            d.append(float(line.split()[14]))
            d.append(float(line.split()[15]))
            y.append(float(line.split()[16]))
            #y.append(float(line.split()[17]))

            data.append(d)
            y1.append(y)
        print("txt data is:", data, "type is :",y1)
    data=np.array(data)

    y1=np.array(y1)
    print(data.shape)
    print(y1.shape)
    return data,y1

# x,y=read_text_data()
#
# model=linear_model.LinearRegression()
# model.fit(x,y)
# y1=model.predict(x)
# print(y1)