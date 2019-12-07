import Astar
import Map
import random
import copy
direction = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]


def moveChoose(m, tmp, x, y, person, number, maxx, maxy):
    ret = [0, 0, 0, 0, 0]
    if number == 0:
        return ret
    v = 1  # adult
    if person == 0:
        v = 1.5  # old
    elif person == 1:
        v = 1.3  # young
    elif person == 3:
        v = 2  # disabled
    moveProb = [0, 0, 0, 0, 0]
    maxProb_ID = 0
    for i in range(5):
        newx = x + direction[i][0]
        newy = y + direction[i][1]
        if newx < 0 or newx >= maxx or newy < 0 or newy >= maxy or m[newx][newy].cap == 0:
            continue
        remain_vol = tmp[newx][newy].remain_vol()
        if remain_vol <= 0:
            continue
        right = (m[x][y].msg - m[newx][newy].msg) * v + remain_vol
        if right > moveProb[maxProb_ID]:
            maxProb_ID = i
        if right < 0:
            right = 0
        moveProb[i] = right
    Probsum = 0
    for e in moveProb:
        Probsum += e
    for i in range(5):
        try:
            ret[i] = int((number * moveProb[i]) / Probsum)
        except:
            ret[i] = 0
    for i in range(5):
        number -= ret[i]
    if number > 0:
        ret[maxProb_ID] += number
    return ret


def process(iter_time):
    cot = 0
    x, y, m = Astar.processMsg()
    while cot <= iter_time:
        print("Total Number of People after {} iterations".format(cot))
        for i in range(x):
            for j in range(y):
                print(m[i][j].totalPerson(), end=" ")
            print()
        print()
        tmp = copy.deepcopy(m)
        for i in range(x):
            for j in range(y):
                if m[i][j].cap == 0 or m[i][j].exit:
                    continue
                for person in range(4):
                    change = moveChoose(m, tmp, i, j, person, m[i][j].person[person], x, y)
                    for k in range(5):
                        newx = i + direction[k][0]
                        newy = j + direction[k][1]
                        if newx < 0 or newx >= x or newy < 0 or newy >= y or m[newx][newy].cap == 0:
                            continue
                        change[k] = min(tmp[newx][newy].remain_vol(), change[k])
                        tmp[newx][newy].person[person] += change[k]
                        tmp[i][j].person[person] -= change[k]
        m = copy.deepcopy(tmp)
        cot += 1

process(30)