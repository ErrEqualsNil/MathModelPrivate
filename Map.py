import numpy as np
import random


class node:
    # 构造函数：cap为整型值，表示每个节点可容纳的最大人数, 若为0，为墙壁；
    #          exit为boolean值， true为出口，false则不是出口；
    #          msg为double值， 表示信息素的值；
    #          person = [old, young, adult, disabled] 分别表示各类人的数量；
    def __init__(self, cap, exit, msg, old, young, adult, disabled):
        self.cap = cap
        self.exit = exit
        self.msg = msg
        self.person = [old, young, adult, disabled]
    def remain_vol(self):
        ret = self.cap
        for e in self.person:
            ret -= e
        return ret
    def totalPerson(self):
        ret = 0
        for e in self.person:
            ret += e
        return ret


def createMap1():
    # 下面为地图大体轮廓生成
    sizex = 6
    sizey = 11
    m = np.empty((sizex, sizey), node)
    for i in range(sizex):
        for j in range(sizey):
            m[i][j] = node(15, False, 0, random.randint(0, 4), random.randint(0, 4), random.randint(0, 7),
                           0)

    """
    接下来进行细节修饰
    """
    for i in range(4):
        m[i][0].cap = 0
        m[i][0].person = [0, 0, 0, 0]
    for i in range(9):
        m[5][i].cap = 0
        m[5][i].person = [0, 0, 0, 0]
    for i in range(2):
        for j in range(2):
            m[1+i][3+j].cap = 0
            m[1+i][3+j].person = [0, 0, 0, 0]
    for i in range(2):
        for j in range(2):
            m[2+i][7+j].cap = 0
            m[2+i][7+j].person = [0, 0, 0, 0]
    m[4][0].exit = True
    #  m[4][0].cap = 0x3f3f
    m[5][9].exit = True
    #  m[5][9].cap = 0x3f3f
    m[5][10].exit = True
    #  m[5][10].cap = 0x3f3f
    return sizex, sizey, m



