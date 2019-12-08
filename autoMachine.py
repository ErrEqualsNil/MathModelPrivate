import Astar
import copy
import queue
direction = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]


def movechoose(m, tmp, x, y, person, number, maxx, maxy):
    ret = [0, 0, 0, 0, 0]
    if number == 0:
        return ret
    v = 1  # adult
    if person == 0:
        v = 2  # old
    elif person == 1:
        v = 1.5  # young
    elif person == 3:
        v = 3  # disabled
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
        right = (m[x][y].msg - m[newx][newy].msg) * v * 2 + remain_vol
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
        except ZeroDivisionError:
            ret[i] = 0
    for i in range(5):
        number -= ret[i]
    if number > 0:
        ret[maxProb_ID] += number
    return ret


def process(iter_time):
    flows = 3
    cot = 1
    x, y, m = Astar.processMsg()
    print("Initial Number of People".format(cot))
    for i in range(x):
        for j in range(y):
            print(m[i][j].totalPerson(), end=" ")
        print()
    print()
    while cot <= iter_time:
        tmp = copy.deepcopy(m)
        vis = [[0] * y for i in range(x)]
        q = queue.Queue()
        while not q.empty():
            q.get()
        for i in range(x):
            for j in range(y):
                if m[i][j].exit:
                    q.put(Astar.pos(i, j))
                    vis[i][j] = 1
        while not q.empty():
            cur = q.get()
            i, j = cur.x, cur.y
            if m[i][j].cap == 0:
                continue
            if m[i][j].exit:
                needflow = flows
                for k in range(4):
                    if m[i][j].person[k] <= needflow:
                        needflow -= m[i][j].person[k]
                        tmp[i][j].person[k] -= m[i][j].person[k]
                    elif m[i][j].person[k] > needflow:
                        tmp[i][j].person[k] -= needflow
                        needflow = 0
                        break
                if flows - needflow != 0:
                    print("{} leave at x = {};y = {}; remain {}".format(flows - needflow,
                                                                        i, j, tmp[i][j].totalPerson()))
            else:
                for person in range(4):
                    change = movechoose(m, tmp, i, j, person, m[i][j].person[person], x, y)
                    for k in range(5):
                        newx = i + direction[k][0]
                        newy = j + direction[k][1]
                        if newx < 0 or newx >= x or newy < 0 or newy >= y or m[newx][newy].cap == 0:
                            continue
                        change[k] = min(tmp[newx][newy].remain_vol(), change[k])
                        tmp[newx][newy].person[person] += change[k]
                        tmp[i][j].person[person] -= change[k]
                        if change[k] != 0:
                            print("{} move from x = {};y = {} to x = {};y = {}".format(change[k], i, j, newx, newy))
            for flag in range(4):
                newnode = Astar.pos(i + direction[flag][0], j + direction[flag][1])
                if newnode.x < 0 or newnode.y < 0 or newnode.x >= x or newnode.y >= y or vis[newnode.x][newnode.y] != 0:
                    continue
                vis[newnode.x][newnode.y] = 1
                q.put(newnode)
        m = copy.deepcopy(tmp)
        print("Total Number of People after {} iterations".format(cot))
        for i in range(x):
            for j in range(y):
                print(m[i][j].totalPerson(), end=" ")
            print()
        print()
        cot += 1


itertimes = input("Please input time of iterations:")
try:
    itertimes = int(itertimes)
    process(itertimes)
except:
    print("Invalid Input! Please try again\n")

