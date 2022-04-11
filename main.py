"""
模块名:   main
功能：    定义了mainWindow类，实现各种功能
         定义了主函数
"""
#导入相关包
import sys
import traceback
from PyQt5.QtWidgets import QMainWindow,QWidget
from PyQt5.QtWidgets import QApplication,QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QRect,Qt
from PyQt5.QtGui import QPainter,QColor
#导入项目的其他模块
from A_star import A_star,caculate
from mainUI import *

"""
函数名: swapString
参数：  i，j：两个字符的位置
       string：字符串 
功能： 交换字符串中的两个字符
"""
def swapString(string,i,j):
    temp = string[j]
    trailer = string[j+1:] if j + 1 < len(string) else ''
    string = string[0:j] + string[i] + trailer
    string = string[0:i] + temp + string[i+1:]
    return string

"""
类：显示树的窗口
"""
class TreeWindow(QWidget):
    def __init__(self):
        super().__init__() 
        self.treexy={}#结点坐标
        self.tree={}#树的结构
        self.lst_steps=[]#解步骤
        self.fn={}#评价函数
        self.X=1000#默认宽度
        self.Y=1000#默认高度
        self.isDraw=False#是否开始绘制树
        self.initUI()#初始化函数
    def initUI(self):
        self.setMinimumSize(self.X, self.Y) 
        
    """
    方法名: paintEvent
    参数：  e：事件
    功能： 执行绘制事件
    """
    def paintEvent(self, e):
        if self.isDraw:
            qp = QPainter()#定义绘制指针
            qp.begin(self)
            self.setMinimumSize(self.X, self.Y+50)#设置窗口大小
            self.drawTree(qp)#绘制树
            qp.end()
    
    """
    方法名: drawNine
    参数：  qp:绘图指针；x，y：坐标；state：状态序列
    功能：  绘制树的一个结点对应的九宫格
    """
    def drawNine(self,qp,x,y,state):
        w=30
        y=y-3*w/2
        x=x-3*w/2
        if state in self.lst_steps:
            qp.setPen(QColor(255, 0, 0))
        qp.drawText(x,y-w/3,str(self.fn[state]))
        for i in range(9):
            qp.drawRect(x+i%3*w,y+i//3*w,w,w)
            if state[i]!='0':    
                qp.drawText(x+i%3*w+w/2,y+i//3*w+w/2,state[i])
        qp.setPen(QColor(0, 0, 0))
        
    """
    方法名: drawTree
    参数：  qp:绘图指针；
    功能：  绘制树
    """        
    def drawTree(self,qp):
        w=30#每个格子的大小
        for i in self.treexy:
            self.drawNine(qp,self.treexy[i][0],self.treexy[i][1],i)#绘制结点
            child=self.tree[i]
            for j in child:
                if j in self.lst_steps:#如果是解步骤则修改画笔颜色为红色
                    qp.setPen(QColor(255, 0, 0))
                #绘制与子结点的连接线
                qp.drawLine(self.treexy[i][0],self.treexy[i][1]+3*w/2,self.treexy[j][0],self.treexy[j][1]-3*w/2)
                qp.setPen(QColor(0, 0, 0))


"""
类：主窗口
"""          
class mainWindow(QMainWindow,mainUI):#主窗口继承自QMainWindow和mainUI
    """
    构造函数
    """   
    def __init__(self,parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)#初始化UI界面
        
        #绘制树的滚动窗口
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(800, 0, 800, 900))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.treewindow=TreeWindow()
        self.scrollArea.setWidget(self.treewindow)
        self.vBar = self.scrollArea.verticalScrollBar()
        self.hBar = self.scrollArea.horizontalScrollBar()
        
        #初始化相关属性
        self.count = 0
        self.isStart=False #是否开始搜索路径
        self.flag_success=0#目标是否可达
        self.lst_steps=[] #解步骤
        self.lst_meg=[] #解的相关信息
        self.changeGoal=False #修改目标状态 or 初始状态
        self.initState = "123456780"  # 初始状态
        self.goalState = "123456780"  # 目标状态
        
        #将设置状态按钮与setState方法关联
        self.setStateButton.clicked[bool].connect(self.setState)
        #将输入状态按钮与inputState方法关联
        self.inputStateButton.clicked.connect(self.inputState)
        #将上一步按钮与lastStep方法关联
        self.lastButton.clicked.connect(self.lastStep)
        #将下一步按钮与nextStep方法关联
        self.nextButton.clicked.connect(self.nextStep)
        #将开始按钮与run方法关联
        self.Run.clicked.connect(self.run) 
        #将重置按钮与reset方法关联
        self.Reset.clicked.connect(self.reset)
        #点击继续按钮关闭对话框
        self.btn.clicked.connect(self.dialog.close)
        
        #定义计时器，用于步骤演示
        timer = QTimer()
        timer.timeout.connect(self.stepShow) # 计时器
        self.btn.clicked.connect(lambda :timer.start(1500))
        #显示窗口
        self.show()
        
    """
    方法名: reset
    参数：  
    功能：  重置程序
    """    
    def reset(self):
        self.count = 0
        self.isStart=False
        self.flag_success=0
        self.lst_steps=[]
        self.lst_meg=[]
        self.initState = "123456780"
        self.goalState = "123456780"
        self.label_1.setText("解步长:")
        self.label_2.setText("当前步数:")
        self.label_3.setText("运行时间:")
        self.label_9.setText("")
        self.label_4.setText("生成结点数:")
        self.label_5.setText("扩展结点数:")
        self.label_6.setText("未扩展数:")
        self.label_7.setText("外显率:")
        self.label_8.setText("有效分支因子:")
        self.treewindow.isDraw=False
        #重置九宫格显示
        for i in range(1, 10):
            goal = eval('self.goal' + str(i))
            goal.setPixmap(QPixmap('resource/'+str(self.goalState[i-1])+'.ico'))
            init = eval('self.init' + str(i))
            init.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))
            self_show = eval('self.show' + str(i))
            self_show.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))
            

    """
    方法名: setState
    参数：  pressde:是否按下按键
    功能：  当按下w，a，s，d是修改九宫格状态
    """               
    def setState(self,pressed):
        if pressed:
            self.changeGoal=True
            self.setStateButton.setText("设置目标状态")
        else:
            self.changeGoal=False
            self.setStateButton.setText("设置初始状态")
    
    """
    方法名: inputState
    参数：  
    功能：  通过弹出框输入状态，并修改九宫格状态
    """ 
    def inputState(self):
        sender = self.sender()
        if sender == self.inputStateButton:  
            if self.changeGoal:
                text, ok = self.inputDialog.getText(self, '修改', '请输入目标状态(123456780)：')
                #判断输入合法性
                if not(len(text)==9):
                    return
                for i in text:
                    if not (i>='0' and i<='8'):
                        return
                #修改九宫格
                if ok:
                    self.goalState=text
                    for i in range(1, 10):
                        goal = eval('self.goal' + str(i))
                        goal.setPixmap(QPixmap('resource/'+str(self.goalState[i-1])+'.ico'))
            else:
                text, ok = self.inputDialog.getText(self, '修改', '请输入初始状态(123456780)：')
                #判断输入合法性
                if not(len(text)==9):
                    return
                for i in text:
                    if not (i>='0' and i<='8'):
                        return
                #修改九宫格
                if ok:
                    self.initState=text
                    for i in range(1, 10):
                        init = eval('self.init' + str(i))
                        init.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))
                        self_show = eval('self.show' + str(i))
                        self_show.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))
                           
    """
    方法名: stepShow
    参数：  
    功能：  动态演示解步骤
    """             
    def stepShow(self):
        try:
            if not(self.stepCheckBox.isChecked()) and self.count < len(self.lst_steps)-1:  # 更新一遍八数码的值
                self.count = self.count + 1#修改当前步数
                #动态跟踪搜索树中的对应结点
                self.hBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][0]-400)
                self.vBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][1]-400)
                self.label_2.setText("当前步数:"+str(self.count))
                #修改九宫格状态
                for i in range(1, 10):
                    self_show = eval('self.show' + str(i))
                    self_show.setPixmap(QPixmap('resource/'+str(self.lst_steps[self.count][i-1])+'.ico'))   
        except:
            print(traceback.format_exc()) #输出异常信息
            pass   
    
    """
    方法名: lastStep
    参数：  
    功能：  跳到上一步
    """         
    def lastStep(self):
        try:
            if self.stepCheckBox.isChecked() and self.count > 0:
                self.count-=1
                self.label_2.setText("当前步数:"+str(self.count))
                #动态跟踪搜索树中的对应结点
                self.hBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][0]-400)
                self.vBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][1]-400)
                #修改九宫格状态
                for i in range(1, 10):
                    self_show = eval('self.show' + str(i))
                    self_show.setPixmap(QPixmap('resource/'+str(self.lst_steps[self.count][i-1])+'.ico')) 
        except:
            print("last_step error")
            print(traceback.format_exc())  #输出异常信息
            pass
    """
    方法名: nextStep
    参数：  
    功能：  跳到下一步
    """     
    def nextStep(self):
        try:
            if self.stepCheckBox.isChecked() and self.count < len(self.lst_steps)-1:
                self.count+=1
                self.label_2.setText("当前步数:"+str(self.count))
                #动态跟踪搜索树中的对应结点
                self.hBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][0]-400)
                self.vBar.setValue(self.treewindow.treexy[self.lst_steps[self.count]][1]-400)
                #修改九宫格状态
                for i in range(1, 10):
                    self_show = eval('self.show' + str(i))
                    self_show.setPixmap(QPixmap('resource/'+str(self.lst_steps[self.count][i-1])+'.ico')) 
        except:
            print("next_step error")
            print(traceback.format_exc())  #输出异常信息
            pass

    """
    方法名: run
    参数：  
    功能：  开始运行
    """         
    def run(self):
        try:          
            print(self.initState)
            print(self.goalState)
            self.isStart=True#开始运行标志
            #显示运行弹出框
            self.dialog.show()
            #执行A*算法
            self.flag_success,self.lst_steps,self.lst_meg,draw_tree,tree_parent=A_star(self.initState, self.goalState, int(self.optAlgorithm.currentText()[1]))
            #执行完毕之后使“继续”按钮生效
            self.btn.setEnabled(True)
            
            #目标不可达的情况
            if self.flag_success == 0:
                self.label_run.setText("目标不可达")
                print("fail")
            #目标可达的情况
            else:
                self.label_1.setText("解步长:"+str(self.lst_meg[0]))
                self.label_2.setText("当前步数:"+str(self.count))
                self.label_3.setText("运行时间:"+str(self.lst_meg[3]))
                self.label_9.setText("s")
                self.label_4.setText("生成结点数:"+str(self.lst_meg[1]+self.lst_meg[2]))
                self.label_5.setText("扩展结点数:"+str(self.lst_meg[1]))
                self.label_6.setText("未扩展数:"+str(self.lst_meg[2]))
                self.label_7.setText("外显率:"+str(self.lst_meg[0]/(self.lst_meg[1]+self.lst_meg[2])))
                self.label_8.setText("有效分支因子:"+str((self.lst_meg[1]+self.lst_meg[2])/max(1,self.lst_meg[1])))
                print(self.lst_steps)
                self.label_run.setText("目 标 可 达")
                print("run_success")
                #画搜索树
                self.treewindow.lst_steps=self.lst_steps
                self.treewindow.fn=draw_tree[1]
                self.treewindow.tree=draw_tree[2]
                self.treewindow.treexy,self.treewindow.X,self.treewindow.Y=caculate(self.initState,self.goalState,draw_tree[0],draw_tree[2],tree_parent,self.lst_meg[2])
                self.treewindow.isDraw=True
        #运行出错
        except:
            self.label_run.setText("运 行 出 错")
            print(traceback.format_exc())  #输出异常信息
            pass

    """
    方法名: keyPressEvent
    参数：  event：事件
    功能：  根据键盘按键 w,a,s,d 修改状态和九宫格
    """         
    def keyPressEvent(self,event):
        #当开始运行时禁用此功能
        if self.isStart:
            return
        #获取当前按键
        key=event.key()
        if self.changeGoal:
            state=self.goalState
        else:
            state=self.initState
            
        #根据w,a,s,d不同按键修改状态和九宫格
        zeroPos=state.find('0')
        if zeroPos==0:
            if key==Qt.Key_A:
                state=swapString(state,0,1)
            elif key==Qt.Key_W:
                state=swapString(state,0,3)
        elif zeroPos==1:
            if key==Qt.Key_A:
                state=swapString(state,1,2)
            elif key==Qt.Key_W:
                state=swapString(state,1,4)
            elif key==Qt.Key_D:
                state=swapString(state,0,1)
        elif zeroPos==2:
            if key==Qt.Key_W:
                state=swapString(state,2,5)
            elif key==Qt.Key_D:
                state=swapString(state,1,2)
        elif zeroPos==3:
            if key==Qt.Key_A:
                state=swapString(state,3,4)
            elif key==Qt.Key_W:
                state=swapString(state,3,6)
            elif key==Qt.Key_S:
                state=swapString(state,0,3)
        elif zeroPos==4:
            if key==Qt.Key_A:
                state=swapString(state,4,5)
            elif key==Qt.Key_D:
                state=swapString(state,3,4)            
            elif key==Qt.Key_W:
                state=swapString(state,4,7)
            elif key==Qt.Key_S:
                state=swapString(state,1,4)            
        elif zeroPos==5:
            if key==Qt.Key_D:
                state=swapString(state,4,5)            
            elif key==Qt.Key_W:
                state=swapString(state,5,8)
            elif key==Qt.Key_S:
                state=swapString(state,2,5)  
        elif zeroPos==6:
            if key==Qt.Key_A:
                state=swapString(state,6,7)
            elif key==Qt.Key_S:
                state=swapString(state,3,6)                  
        elif zeroPos==7:
            if key==Qt.Key_A:
                state=swapString(state,7,8)
            elif key==Qt.Key_D:
                state=swapString(state,6,7)            
            elif key==Qt.Key_S:
                state=swapString(state,4,7)                  
        elif zeroPos==8:
            if key==Qt.Key_D:
                state=swapString(state,7,8)            
            elif key==Qt.Key_S:
                state=swapString(state,5,8)
        if self.changeGoal:
            self.goalState=state 
            for i in range(1, 10):
                goal = eval('self.goal' + str(i))
                goal.setPixmap(QPixmap('resource/'+str(self.goalState[i-1])+'.ico'))  
        else:
            self.initState=state 
            for i in range(1, 10):
                init = eval('self.init' + str(i))
                init.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))
                self_show = eval('self.show' + str(i))
                self_show.setPixmap(QPixmap('resource/'+str(self.initState[i-1])+'.ico'))

#主函数                
if __name__ == '__main__':
    app = QApplication(sys.argv)#获取命令行参数
    myWin = mainWindow()#实例化窗口
    myWin.show()
    sys.exit(app.exec_())
  
        