"""
模块名:   A_star
功能：    使用A*搜索求解八数码问题，并记录相关信息
"""
import math
import time
#空白方格转移表
dict_shifts = {0:[1, 3], 1:[0, 2, 4], 2:[1, 5],
               3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
               6:[3,7],  7:[4,6,8], 8:[5,7]}

#交换数组a内的两个元素
def swap_char(a, i, j):
    if i > j:
        i, j = j, i
    #得到ij交换后的数组
    b = a[:i] + a[j] + a[i+1:j] + a[i] + a[j+1:]
    return b

#第一种启发函数：cost=不在位数字个数
def h1(curState,goalState):
    cost=0
    for i in range(len(goalState)):
        if curState[i]!=goalState[i] and curState[i]!=0:
            cost+=1
    return cost
#第二种启发函数：cost=到目标位置曼哈顿距离和
def h2(curState,goalState):
    cost=0
    for i in range(1,len(goalState)):
        a=curState.index(str(i))
        b=goalState.index(str(i))
        cost+=abs(a//3-b//3)+abs(a%3-b%3)
    return cost
#第三种启发函数：cost=对应位置的数字差值之和
def h3(curState,goalState):
    n=0
    for i in range(len(goalState)):
        n+=abs(int(goalState[i])-int(curState[i]))
    return n
#第四种启发函数：cost=对应数字的位置差值之和
def h4(curState,goalState):
    n=0
    for i in range(len(goalState)):
        if i!='0':
            n+=abs(curState.index(curState[i])-goalState.index(curState[i]))
    return n
#第五种启发函数：cost=到目标位置欧几里得距离和
def h5(curState,goalState):
    cost=0
    for i in range(1,len(goalState)):
        a=curState.index(str(i))
        b=goalState.index(str(i))
        cost+=math.sqrt((a//3-b//3)**2+(a%3-b%3)**2)
    return cost
#第六种启发函数：cost=到目标位置切比雪夫距离和
def h6(curState,goalState):
    cost=0
    for i in range(1,len(goalState)):
        a=curState.index(str(i))
        b=goalState.index(str(i))
        cost+=max(abs(a//3-b//3),abs(a%3-b%3))
    return cost
#第七种启发函数：cost=max{i*h1+j*h2+k*h3+l*h4+m*h5+n*h6}其中i、j、k、m是通过网格搜索得到的
def h7(curState,goalState,index):
    return index[0]*h1(curState,goalState)+index[1]*h2(curState,goalState)+index[2]*h3(curState,goalState)+index[3]*h4(curState,goalState)+index[4]*h5(curState,goalState)+index[5]*h6(curState,goalState)

def h(curState,goalState,choice,index):
    if choice==1:
        return h1(curState,goalState)
    elif choice==2:
        return h2(curState,goalState)
    elif choice==3:
        return h3(curState,goalState)
    elif choice==4:
        return h4(curState,goalState)
    elif choice==5:
        return h5(curState,goalState)
    elif choice==6:
        return h6(curState,goalState)
    elif choice==7:
        return h7(curState,goalState,index)

#寻找代价最小的节点
def find_min_cost(listf):
    min_cost=listf[0]
    for state in listf:
        if state[1]<min_cost[1]:
            min_cost=state
    return min_cost
      
#A*搜索函数
def A_star(initState,goalState,choice=1,index=[1,3,0,0,0,0]):
    print("选择了A"+str(choice))
    #开始计时
    startTime=time.time()
    #首先先判断八数码问题是否可解
    src=0;dest=0
    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if initState[j]>initState[i] and initState[i]!='0':
              fist=fist+1
        src=src+fist
    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if goalState[j]>goalState[i] and goalState[i]!='0':
              fist=fist+1
        dest=dest+fist
    if (src%2)!=(dest%2):#一个奇数一个偶数，不可达
        return 0,None,None,None,None

    #初始化字典
    tree={}#树字典，用列表存储状态的后继节点，叶子节点的后继为空列表
    tree[initState]=[]#初始状态根节点初始化为空列表
    tree_parent = {}#亲代字典，存储状态的父亲节点
    tree_parent[initState] = -1#初始状态根节点的父亲节点不存在，标记为-1
    list_f = []#记录列表，临时存放未拓展节点及其f(n)估价函数
    gn={}#gn列表记录每个节点的g(n)实际代价
    fn={}#fn列表记录每个节点的f(n)估价函数
    gn[initState]=0#初始状态根节点的g(n)实际代价为0
    fn[initState]=gn[initState]+h(initState,goalState,choice,index)#初始状态根节点的估价函数为实际代价+启发函数得出的到目标的最小代价
    
    list_f.append([initState,fn[initState]])#当前状态存入列表
    node_unextended=1#待拓展结点数
    node_extended=0#已拓展结点数
    while len(list_f)>0:#当当前未拓展节点数大于0时
        min_cost=find_min_cost(list_f)#从当前未拓展节点中寻找f(n)估价函数最小的节点
        list_f.remove(min_cost)#并从未拓展节点中删除     
        curState=min_cost[0]#更新当前状态
        
        if curState==goalState:#如果当前状态为目标状态则搜索成功
            break
        
        zero_index=curState.index('0')#找到空白方格的位置
        lst_shifts=dict_shifts[zero_index]#查找空白方格所能到达的位置
        tag=1
        for n in lst_shifts:#遍历当前状态所有可能的后继状态
            newState=swap_char(curState,n,zero_index)#根据空白方格到达的位置算出新的状态
            if tree_parent.get(newState) == None:#判断交换后的状态是否已经查询过
                if tag==1:
                    node_unextended=node_unextended-1#未拓展节点-1
                    node_extended=node_extended+1#已拓展节点+1
                    tag=0
                gn[newState]=gn[curState]+1#计算新节点的g(n)实际代价
                fn[newState]=gn[newState]+h(newState,goalState,choice,index)#计算新节点的f(n)估价函数
                tree[curState].append(newState)#将新节点作为当前节点的子节点存入字典
                tree[newState]=[]#初始化新状态为空列表
                tree_parent[newState] = curState#将当前节点作为新节点的根节点存入字典
                list_f.append([newState,fn[newState]])#将新节点及其f(n)存入未拓展节点列表
                node_unextended=node_unextended+1#未拓展节点数+1
        
    lst_steps=[]#初始化解路径列表
    lst_steps.append(curState)#将当前节点也就是目标节点存入解路径
    while tree_parent[curState] != -1:#存入路径
        curState = tree_parent[curState]#回溯父亲节点，并存入解路径
        lst_steps.append(curState)
    lst_steps.reverse()#此时的解路径时从目标节点到初始节点的因此要转置列表
    solution_length=len(lst_steps)-1#计算解步长
    runtime=time.time()-startTime#计算求解时间
    lst_meg=[solution_length,node_extended,node_unextended,runtime]
    draw_tree=[gn,fn,tree]
    return 1,lst_steps,lst_meg,draw_tree,tree_parent

"""
模块名:   caculate
功能：    计算搜索树各个节点的坐标，为搜索树的绘制做准备
"""
#搜索树坐标计算函数
def caculate(root,dest,gn,tree,tree_parent,node_unextend):
    X_bondary=50#水平方向边框宽度
    Y_bondary=50#竖直方向边框宽度
    X_unit=100#水平方向长度单位
    Y_unit=150#竖直方向长度单位
    rootsnode=[]#非叶子节点列表
    treexy={}#节点坐标字典
    curState=root#初始化当前节点为根节点
    deep=max(gn.values())#搜索树的最大深度
    for node in tree:#寻找非叶子节点
        if len(tree[node])!=0:
            rootsnode.append(node)           
    unit_x_step=0#记录已计算的叶子节点
    X=X_unit*node_unextend+2*X_bondary#计算窗口长度
    Y=Y_unit*deep+2*Y_bondary#计算窗口高度
    #深度优先遍历，计算节点坐标
    while True:
        down=False
        for nextState in list(tree[curState]):#遍历当前节点的孩子节点
            if nextState not in treexy.keys():#孩子节点坐标未生成
                if nextState in rootsnode:#孩子节点不是叶子节点
                    down=True#继续深度遍历
                    break
                else:
                    treexy[nextState]=[int(X_bondary+unit_x_step*X_unit),int(Y_bondary+gn[nextState]*Y_unit)]#计算叶子节点坐标
                    unit_x_step+=1
        if down:#继续优先遍历
            curState=nextState#当前状态下推
        else:#当前节点的所有孩子节点均生成了坐标
            sum_children_x=0
            count_children=len(tree[curState])
            for child in tree[curState]:
                sum_children_x+=treexy[child][0]
            #当前节点的x坐标为其孩子节点横坐标的平均值，y坐标根据其g(n)实际代价计算
            treexy[curState]=[int(sum_children_x/max(1,count_children)),int(Y_bondary+gn[curState]*Y_unit)]
            curState=tree_parent[curState]#回溯到当前节点的父亲节点
            if(curState==-1):#没有父亲节点代表计算完成
                break
    return treexy,X,Y

if __name__ == "__main__":
    srcLayout  = "536702418"#运行快的序列
    destLayout = "123456780"
    a,b,c,d,e=A_star(srcLayout,destLayout,7)
    print(c)