from Map import createMap1
import queue

class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def processMsg():
    x, y, m = createMap1()
    direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    q = queue.Queue()
    vis = [[0]*y for i in range(x)]
    for i in range(x):
        for j in range(y):
            if m[i][j].exit:
                q.put(pos(i, j))
                vis[i][j] = 1
    while not q.empty():
        cur = q.get()
        for i in range(4):
            nex = pos(cur.x + direction[i][0], cur.y + direction[i][1])
            if nex.x >= x or nex.x < 0 or nex.y >= y or nex.y < 0 or vis[nex.x][nex.y] != 0 or m[nex.x][nex.y].cap == 0:
                continue
            m[nex.x][nex.y].msg = m[cur.x][cur.y].msg + 1
            vis[nex.x][nex.y] = 1
            q.put(nex)
    return x, y, m

