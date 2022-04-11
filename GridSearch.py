"""
模块名:   GridSearch
功能：    针对h5的权值参数进行网格搜索，并对不同权值参数进行评判和筛
"""
from A_star import A_star
import random

#网格搜索
def GridSearch(size,choice_range,goalState,index_lim):
    record={}
    #进行size次测试
    for i in range(size):
        #生成随机初始序列
        while True:
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
        #遍历所有可取参数
        for i in range(index_lim+1):
            for j in range(index_lim+1):
                for k in range(index_lim+1):
                    for l in range(index_lim+1):
                        for m in range(index_lim+1):
                            for n in range(index_lim+1):
                                if i==0 and j==0 and k==0 and l==0 and m==0 and n==0:
                                    continue
                                else:
                                    index=i*100000+j*10000+k*1000+l*100+m*10+n
                                    a,b,lst_meg,d,e=A_star(initState,goalState,7,[i,j,k,l,m,n])
                                    if index not in record:
                                        record[index]=lst_meg
                                    else:
                                        for p in range(4):
                                            record[index][p]+=lst_meg[p]
    #求均值
    for index in record:
        for p in range(4):
            record[index][p]/=size
    return record

#从网格搜索的所有结果中寻找局部最优解和整体最优解    
def findbest(record):
    minstep=record[1][0]
    minstep_r={}
    minnode=record[1][1]+record[1][2]
    minnode_r={}
    minruntime=record[1][3]
    minruntime_r={}
    for i in record:
        if record[i][0]<minstep:
            minstep=record[i][0]
        if record[i][1]+record[i][2]<minnode:
            minnode=record[i][1]+record[i][2]
        if record[i][3]<minruntime:
            minruntime=record[i][3]
    
    #单项选优
    for i in record:
        if record[i][0]==minstep:
            minstep_r[i]=(record[i])
        if record[i][1]+record[i][2]==minnode:
            minnode_r[i]=(record[i])
        if record[i][3]==minruntime:
            minruntime_r[i]=(record[i])
    
    #设定综合选优阀值
    t=20
    while True:
        bestrecord=[]
        for i in record:
            if record[i][0]<minstep*t and record[i][1]+record[i][2]<minnode*t and record[i][3]<minruntime*t:
                bestrecord.append(i)
        if len(bestrecord)>1:
            t-=0.01
        else:
            t+=0.01
            for i in record:
                if record[i][0]<minstep*t and record[i][1]+record[i][2]<minnode*t and record[i][3]<minruntime*t:
                    bestrecord.append(i)
            break
    
    return t,bestrecord,minstep_r,minnode_r,minruntime_r


if __name__=="__main__":
    #goalState='123456780'
    record=GridSearch(10,6,'123456780',3)
    for i in record:
        print("%04d"%i,' ',record[i])
    t,bestrecord,minstep,minnode,minruntime=findbest(record)  
    print('minstep')
    for i in minstep:
        print("%06d"%i,' ',minstep[i])
    print('minnode')
    for i in minnode:
        print("%06d"%i,' ',minnode[i])
    print('minruntime')
    for i in minruntime:
        print("%06d"%i,' ',minruntime[i])
    print('bestrecord')
    print(t)
    for i in bestrecord:
        print("%06d"%i)
   
# minstep
# 0100   [21.9, 1253.7, 767.8, 0.13822665214538574]
# 1000   [21.9, 14616.2, 8093.1, 9.406787276268005]
# 1100   [21.9, 539.9, 341.0, 0.035102343559265135]
# 2000   [21.9, 4943.1, 3000.3, 1.5432256698608398]
# minnode
# 0401   [29.1, 119.9, 86.2, 0.006086111068725586]
# minruntime
# 0501   [29.1, 121.4, 87.2, 0.005379533767700196]
# bestrecord
# 1.329999999999674
# 0401
# 0501
        
# minstep
# 0100   [20.1, 579.3, 361.8, 0.03441653251647949]
# 1000   [20.1, 7176.7, 4231.7, 2.148137927055359]
# minnode
# 0500   [25.5, 137.7, 98.6, 0.006391286849975586]
# minruntime
# 1500   [25.7, 144.3, 102.0, 0.006082725524902344]
# bestrecord
# 1.149999999999674
# 0200
# 0200
# 0300

# minstep
# 1000   [21.4, 12531.4, 7015.1, 6.756692361831665]
# minnode
# 1313   [36.8, 150.1, 105.8, 0.006385517120361328]
# minruntime
# 1313   [36.8, 150.1, 105.8, 0.006385517120361328]
# bestrecord
# 1.6099999999996744
# 3201
# 1301
# 3201
# 4201
 
# minstep
# 1000   [19.9, 7760.8, 4525.9, 2.724651312828064]
# minnode
# 0500   [27.9, 174.4, 123.1, 0.007978224754333496]
# minruntime
# 0500   [27.9, 174.4, 123.1, 0.007978224754333496]
# bestrecord
# 1.4099999999996742
# 0500
# 1500    
   
# minstep
# 0100   [22.2, 1825.8, 1078.5, 0.3690191745758057]
# 1000   [22.2, 16608.5, 8776.2, 16.598266625404356]
# minnode
# 1411   [38.4, 247.8, 168.2, 0.012070107460021972]
# minruntime
# 0432   [41.0, 252.1, 166.2, 0.011777877807617188]
# bestrecord
# 1.4999999999996743
# 0500
# 0500
# 2400

# minstep
# 1000   [20.9, 6655.7, 3985.9, 1.537082314491272]
# minnode
# 0510   [34.5, 186.2, 123.0, 0.008214950561523438]
# minruntime
# 0510   [34.5, 186.2, 123.0, 0.008214950561523438]
# bestrecord
# 1.3899999999996742
# 1300
# 2300

# minstep
# 0100   [21.2, 952.5, 594.4, 0.0671051025390625]
# 1000   [21.2, 8658.1, 5111.3, 2.808738136291504]
# minnode
# 0511   [35.6, 198.2, 133.2, 0.009376811981201171]
# minruntime
# 0511   [35.6, 198.2, 133.2, 0.009376811981201171]
# bestrecord
# 1.3699999999996741
# 0400
# 1400
# 2400     

# minstep
# 000001   [21.0, 3325.3, 1961.4, 0.803508186340332]
# 000010   [21.0, 1681.4, 1024.7, 0.28324792385101316]
# 010000   [21.0, 1166.0, 708.5, 0.17681868076324464]
# 100000   [21.0, 9536.8, 5445.0, 4.663604140281677]
# minnode
# 030003   [29.4, 165.8, 115.0, 0.015862011909484865]
# minruntime
# 010032   [29.4, 168.3, 115.1, 0.013973164558410644]
# bestrecord
# 1.3499999999996741
# 010022
# 020003
# 100032
# 110013