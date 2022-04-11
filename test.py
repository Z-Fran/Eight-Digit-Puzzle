"""
模块名:   test
功能：    对各个启发函数进行性能测试，得到一定规模下各启发函数各效用的数学期望和方差，并绘制柱状图
"""
from A_star import A_star
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fmgr
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#测试函数，测试size次运行下，每一种启发函数的平均效用
def test (size,choice_range,goalState):
    statistics={}
    for i in range(size):
        while True:
            #随机生成初始序列
            S=[x for x in range(0,9)]
            random.shuffle(S)
            T=map(str,S)
            initState=''.join(T)
            print(initState)           
            #判断是否可解
            src=0;dest=0
            for i in range(1,9):
                fist=0
                for j in range(0,i):
                  if initState[j]>initState[i] and initState[i]!='0':#0是false,'0'才是数字
                      fist=fist+1
                src=src+fist
            for i in range(1,9):
                fist=0
                for j in range(0,i):
                  if goalState[j]>goalState[i] and goalState[i]!='0':
                      fist=fist+1
                dest=dest+fist
            if (src%2)==(dest%2):
         
                break
        #测试每一种启发函数    
        for choice in range(1,choice_range+1):
            a,b,lst_meg,d,e=A_star(initState,goalState,choice)
            if choice not in statistics:
                statistics[choice]=[lst_meg[0],lst_meg[1],lst_meg[2],lst_meg[3],lst_meg[0]/(lst_meg[1]+lst_meg[2])]    
            else:
                statistics[choice][0]+=lst_meg[0]
                statistics[choice][1]+=lst_meg[1]
                statistics[choice][2]+=lst_meg[2]
                statistics[choice][3]+=lst_meg[3]
                statistics[choice][4]+=lst_meg[0]/(lst_meg[1]+lst_meg[2])
    
    #计算效用平均值           
    for choice in range(1,choice_range+1):
        for k in range(5):
            statistics[choice][k]/=size
    for choice in range(1,choice_range+1):
        statistics[choice].append((statistics[choice][1]+statistics[choice][2])/statistics[choice][1])
            
    return statistics


#计算调用Dxsize次test函数下，每一种启发函数的平均效用的方差
def DX(Dxsize,goalState):
    DX={1:[0,0,0,0,0,0],2:[0,0,0,0,0,0],3:[0,0,0,0,0,0],4:[0,0,0,0,0,0],5:[0,0,0,0,0,0],6:[0,0,0,0,0,0]}
    EX2={1:[0,0,0,0,0,0],2:[0,0,0,0,0,0],3:[0,0,0,0,0,0],4:[0,0,0,0,0,0],5:[0,0,0,0,0,0],6:[0,0,0,0,0,0]}
    EX={1:[0,0,0,0,0,0],2:[0,0,0,0,0,0],3:[0,0,0,0,0,0],4:[0,0,0,0,0,0],5:[0,0,0,0,0,0],6:[0,0,0,0,0,0]}
    for i in range(Dxsize):
        statistics=test(10,6,goalState)
        for j in statistics:
            for k in range(6):
                EX[j][k]+=statistics[j][k]
                EX2[j][k]+=statistics[j][k]*statistics[j][k]
    for j in statistics:
        for k in range(6):
            EX[j][k]/=Dxsize
            EX2[j][k]/=Dxsize
    for j in statistics:
        for k in range(6):
            DX[j][k]=EX2[j][k]-EX[j][k]*EX[j][k]
    return DX

if __name__=="__main__":
    testlist=test(10,6,'123456780')
    title=['平均解步长','平均已拓展节点','平均未拓展节点','平均运行时间','平均外显率','平均有效分支因子']
    for i in range(6):
        # 柱子总数
        N = 6
        # 包含每个柱子对应值的序列
        values=[]
        for j in range(1,7):
            values.append(testlist[j][i])
        # 包含每个柱子下标的序列
        index = np.arange(N)
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        plt.figure(figsize=(10, 10), dpi=80)
        # 柱子的宽度
        width = 0.45
        # 绘制柱状图, 每根柱子的颜色为紫罗兰色
        rects = plt.bar(index, values, width, label="num", color="#87CEFA")
        # 设置横轴标签
        plt.xlabel('启发函数')
        # 添加标题
        plt.title(title[i])
        # 添加纵横轴的刻度
        plt.xticks(index, ('h1', 'h2', 'h3', 'h4','h5','h6'))
        #增加数字标注
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
        plt.show()
    
    title=['解步长方差','已拓展节点方差','未拓展节点方差','运行时间方差','外显率方差','有效分支因子方差']
    dx=DX(5,'123456780')
    for i in range(6):
        # 柱子总数
        N = 6
        # 包含每个柱子对应值的序列
        values=[]
        for j in range(1,7):
            values.append(dx[j][i])
        # 包含每个柱子下标的序列
        index = np.arange(N)
        # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
        plt.figure(figsize=(10, 10), dpi=80)
        # 柱子的宽度
        width = 0.45
        # 绘制柱状图, 每根柱子的颜色为紫罗兰色
        rects = plt.bar(index, values, width, label="num", color="#87CEFA")
        # 设置横轴标签
        plt.xlabel('启发函数')
        # 添加标题
        plt.title(title[i])
        # 添加纵横轴的刻度
        plt.xticks(index, ('h1', 'h2', 'h3', 'h4','h5','h6'))
        #增加数字标注
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
        plt.show()
    
    
    
    # testlist=test(10,4,'123456780')
    # print("启发函数 平均解步长 平均已拓展节点 平均未拓展节点 平均运行时间 平均外显率")
    # for e in testlist:
    #     print(e,' ',testlist[e])
      
    # 1   [0.7719999999999914, 5475152.201599926, 1507820.9543999955, 3.5059175310836324, 9.772208039974883e-06]
    # 2   [0.7063999999999169, 57103.38639999926, 19389.493600000045, 0.0019400244226582368, 0.00023604429889279997]
    # 3   [0.8983999999999241, 1318422.2903999984, 361535.1079999991, 0.4189150128715302, 2.122570403384941e-05]
    # 4   [2.549600000000055, 302696.94959999993, 104529.4504000009, 0.019505370949708542, 6.58582079448571e-05]
   
    # dx=DX(5,'123456780')
    # for e in dx:
    #     print(e,' ',dx[e])