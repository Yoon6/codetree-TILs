from collections import deque
from dataclasses import dataclass

n,m,k = map(int, input().split())

board = [
    list(map(int, input().split()))
    for _ in range(n)
]

rec = [
    [0] * m
    for _ in range(n)
]

turn = 0
dxs, dys = [0, 1, 0, -1], [1, 0, -1, 0]
dxs2, dys2 = [0, 0, -1, -1, -1, 1, 1, 1], [-1, 1, 0, -1, 1, 0, -1, 1]

# 공격과 무관했는지 여부를 저장합니다.
is_active = [
    [False] * m
    for _ in range(n)
]

visited = [
    [False] * m
    for _ in range(n)
]

back_x = [
    [0] * m
    for _ in range(n)
]
back_y = [
    [0] * m
    for _ in range(n)
]


@dataclass
class Turret:
    x: int
    y: int
    r: int # 공격 기록
    p: int # 공격력

live_turret = []

def init():
    global turn
    turn += 1

    for i in range(n):
        for j in range(m):
            is_active[i][j] = False
            visited[i][j] = False



def awake():
    live_turret.sort(key = lambda x: (x.p, -x.r, -(x.x + x.y), -x.y))
    weak_turret = live_turret[0]
    x, y = weak_turret.x, weak_turret.y

    board[x][y] += (n + m)
    rec[x][y] = turn
    weak_turret.r = rec[x][y]
    weak_turret.p = board[x][y]
    is_active[x][y] = True

    live_turret[0] = weak_turret

def laser_attack():
    weak_turret = live_turret[0]
    sx, sy = weak_turret.x, weak_turret.y
    power = weak_turret.p

    strong_turret = live_turret[-1]
    ex, ey = strong_turret.x, strong_turret.y

    q = deque()
    visited[sx][sy] = True
    q.append((sx, sy))

    can_attack = False

    while q:
        x, y = q.popleft()

        if (x, y) == (ex, ey):
            can_attack = True
            break

        for i in range(4):
            nx = (x + dxs[i] + n) % n
            ny = (y + dys[i] + m) % m

            if not visited[nx][ny] and board[nx][ny] != 0:
                visited[nx][ny] = True
                q.append((nx, ny))
                back_x[nx][ny] = x
                back_y[nx][ny] = y


    if can_attack:
        board[ex][ey] -= power
        if board[ex][ey] < 0:
            board[ex][ey] = 0
        is_active[ex][ey] = True

        cx, cy = back_x[ex][ey], back_y[ex][ey]

        while True:
            if (cx, cy) == (sx, sy):
                break
            board[cx][cy] -= power//2
            if board[cx][cy] < 0:
                board[cx][cy] = 0
            is_active[cx][cy] = True
            cx, cy = back_x[cx][cy], back_y[cx][cy]
    return can_attack

def bomb_attack():
    weak_turret = live_turret[0]
    sx, sy = weak_turret.x, weak_turret.y
    power = weak_turret.p

    strong_turret = live_turret[-1]
    ex, ey = strong_turret.x, strong_turret.y

    board[ex][ey] -= power
    if board[ex][ey] < 0:
        board[ex][ey] = 0
    is_active[ex][ey] = True

    for i in range(8):
        nx = (ex + dxs2[i] + n) % n
        ny = (ey + dys2[i] + m) % m

        if (sx, sy) == (nx, ny):
            continue
        board[nx][ny] -= power // 2
        if board[nx][ny] < 0:
            board[nx][ny] = 0
        is_active[nx][ny] = True

def reverse():
    for i in range(n):
        for j in range(m):
            if not is_active[i][j] and board[i][j] > 0:
                board[i][j] += 1


for _ in range(k):
    live_turret = []
    for i in range(n):
        for j in range(m):
            if board[i][j]:
                live_turret.append(Turret(i, j, rec[i][j], board[i][j]))

    if len(live_turret) <= 1:
        break

    init()
    awake()
    is_success = laser_attack()
    if not is_success:
        bomb_attack()
    reverse()


ans = 0
for i in range(n):
    for j in range(m):
        ans = max(ans, board[i][j])
print(ans)