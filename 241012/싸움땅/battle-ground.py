n, m, k = map(int, input().split())

gun = [
    [[] for _ in range(n)]
    for _ in range(n)
]

for i in range(n):
    nums = list(map(int, input().split()))
    for j in range(n):
        if nums[j] != 0:
            gun[i][j].append(nums[j])

players = []
for i in range(m):
    x, y, d, s = map(int, input(). split())
    players.append((i, x-1, y-1, d, s, 0))

# ↑, →, ↓, ←
dxs = [-1, 0, 1,  0]
dys = [ 0, 1, 0, -1]

# 플레이어들의 포인트 정보를 기록합니다.
points = [0] * m

def is_valid(x, y):
    return 0 <= x < n and 0 <= y < n

def get_next(x, y, d):
    nx, ny = x + dxs[d], y + dys[d]
    if not is_valid(nx, ny):
        d = d+2 if d < 2 else d-2
        nx, ny = x + dxs[d], y + dys[d]
    return nx, ny, d

def find_player(pos):
    for i in range(m):
        _, x, y, _, _, _ = players[i]
        if pos == (x, y):
            return players[i]
    return None

def update(player):
    num, _, _, _, _, _ = player
    for i in range(m):
        num_i, _, _, _, _, _ = players[i]
        if num_i == num:
            players[i] = player

def move(player, pos):
    num, x, y, d, s, a = player
    nx, ny = pos

    gun[nx][ny].append(a)
    gun[nx][ny].sort(reverse=True)
    a = gun[nx][ny][0]
    gun[nx][ny].pop(0)

    p = (num, nx, ny, d, s, a)
    update(p)

def loser_move(player):
    num, x, y, d, s, a = player

    gun[x][y].append(a)
    for i in range(4):
        ndir = (d+i)%4
        nx, ny = x + dxs[ndir], y + dys[ndir]
        if is_valid(nx, ny) and find_player((nx, ny)) is None:
            p = (num, x, y, d, s, 0)
            move(p, (nx, ny))
            break


def duel(curr_player, next_player, pos):
    num1, _, _, d1, s1, a1 = curr_player
    num2, _, _, d2, s2, a2 = next_player

    if (s1 + a1, s1) > (s2 + a2, s2):
        points[num1] += (s1 + a1) - (s2 + a2)
        loser_move(next_player)
        move(curr_player, pos)
    else:
        points[num2] += (s2 + a2) - (s1 + a1)
        loser_move(curr_player)
        move(next_player, pos)

def simulate():
    for i in range(m):
        num, x, y, d, s, a = players[i]

        nx, ny, ndir = get_next(x, y, d)
        next_player = find_player((nx, ny))
        curr_player = (num, nx, ny, ndir, s, a)
        update(curr_player)

        if next_player is None:
            move(curr_player, (nx, ny))
        else:
            duel(curr_player, next_player, (nx, ny))


for _ in range(k):
    simulate()

for point in points:
    print(point, end = " ")