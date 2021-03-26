import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def draw(inf,k,name_pic):
    f = open(inf,"r")
    lines = f.readlines()
    need_clum = []
    for line in lines:
        a = line.split("\t")
        b = a[6].replace("\n","")
        if b.isdigit():
            need_clum.append(int(b))
    dict={}
    for key in need_clum:
        dict[key]=dict.get(key,0) + 1
    #字典储存形式为：{长度：该长度序列的个数}。长度为横坐标
    lenths = list(dict.keys())
    #print(lenths)
    sorted_lenth = sorted(need_clum,key=int)
    #真正用于画图的长度应该是升序的，即sorted列表中的长度。
    plt.rcParams['font.sans-serif'] = ['SimHei']				# 解决中文无法显示的问题
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_theme(style="darkgrid")
    plt.hist(sorted_lenth,bins=k)
    plt.xlabel("length")
    plt.ylabel("frequency")
    plt.title(name_pic)
    plt.show()
#自动获取文件夹内所有文件
'''in_files = os.listdir(r"C:/Users/wangsiyi/Desktop/tongji")
names = []
for file in in_files:
    fname = os.path.basename(file)
    names.append(fname)'''

