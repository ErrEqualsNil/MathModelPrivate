import Astar
import copy
import queue
direction = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]


class weight:
    def __init__(self, w, index):
        self.weight = w
        self.index = index

    def __cmp__(self, other):
        if self.weight == other.weight:
            return self.index < other.index
        return self.weight > other.weight

    def __lt__(self, other):
        if self.weight == other.weight:
            return self.index < other.index
        return self.weight > other.weight


def movechoose(m, tmp, x, y, maxx, maxy, exitlist, flows):
    for ID in range(4):
        if m[x][y].person[ID] == 0:
            continue
        alpha = 0
        if ID == 0:
            alpha = 0.7  # old
        elif ID == 1:
            alpha = 0.5  # young
        elif ID == 2:
            alpha = 0.3  # adult
        elif ID == 3:
            alpha = 1  # disabled

        weightlist = queue.PriorityQueue()
        for i in range(5):
            newx = x + direction[i][0]
            newy = y + direction[i][1]
            if newx < 0 or newx >= maxx or newy < 0 or newy >= maxy or m[newx][newy].cap == 0:
                continue
            if m[newx][newy].exit:
                w = 0x3f3f
            else:
                w = 0
                tmpw = w
                for exit in exitlist:
                    symmetry_x = 2 * exit.x - newx
                    symmetry_y = 2 * exit.y - newy
                    for tmpx in range(min(symmetry_x, newx + 1), max(symmetry_x, newx + 1)):
                        for tmpy in range(min(symmetry_y, newx + 1), max(symmetry_y, newx + 1)):
                            if tmpx < 0 or tmpx >= maxx or tmpy < 0 or tmpy >= maxy:
                                continue
                            tmpw += m[tmpx][tmpy].totalPerson()
                            tmpw = max(tmpw, m[tmpx][tmpy].msg)
                    tmpw /= float(flows)
                    w = max(w, tmpw)
                w = - w * alpha + (m[x][y].msg - m[newx][newy].msg)
            weightlist.put(weight(w, i))
        personNeedMove = m[x][y].person[ID]
        while not weightlist.empty():
            w = weightlist.get()
            newx = x + direction[w.index][0]
            newy = y + direction[w.index][1]
            change = min(tmp[newx][newy].remain_vol(), personNeedMove)
            tmp[newx][newy].person[ID] += change
            tmp[x][y].person[ID] -= change
            personNeedMove -= change
            if m[x][y].person[ID] == 0:
                break


def process():
    flows = 3
    cot = 1
    x, y, m = Astar.processMsg()
    exitpos = []
    # print("Initial Number of People".format(cot))
    for i in range(x):
        for j in range(y):
            # print(m[i][j].totalPerson(), end=" ")
            if m[i][j].exit:
                exitpos.append(Astar.pos(i, j))
        # print()
    # print()

    while True:
        tmp = copy.deepcopy(m)
        vis = [[0] * y for i in range(x)]
        q = queue.Queue()
        while not q.empty():
            q.get()
        for exit in exitpos:
            q.put(exit)
            vis[exit.x][exit.y] = 1
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
                    '''
                    if flows - needflow != 0:
                    print("{} leave at x = {};y = {}; remain {}".format(flows - needflow,
                                                                        i, j, tmp[i][j].totalPerson()))
                    '''
            else:
                movechoose(m, tmp, i, j, x, y, exitpos, flows)
            for flag in range(4):
                newnode = Astar.pos(i + direction[flag][0], j + direction[flag][1])
                if newnode.x < 0 or newnode.y < 0 or newnode.x >= x or newnode.y >= y or \
                        vis[newnode.x][newnode.y] != 0:
                    continue
                vis[newnode.x][newnode.y] = 1
                q.put(newnode)
        m = copy.deepcopy(tmp)
        count = 0
        # print("Total Number of People after {} iterations".format(cot))
        for i in range(x):
            for j in range(y):
                # print(m[i][j].totalPerson(), end=" ")
                count += m[i][j].totalPerson()
            # print()
        # print()
        if count == 0:
            print("Finish Process At Iteration {}".format(cot))
            return cot
        cot += 1

