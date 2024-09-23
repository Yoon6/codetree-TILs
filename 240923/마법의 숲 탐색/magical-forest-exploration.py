import queue
from collections import deque

R, C, K = map(int, input().split())

table = [[0] * (C + 1) for i in range(R + 1)]
score = 0

for i in range(R + 1):
    table[i][0] = -1
for i in range(C + 1):
    table[0][i] = -1

cols = [-1]
directs = [-1]
for i in range(K):
    ci, di = map(int, input().split())
    cols.append(ci)
    directs.append(di)

direction23 = ['북', '동', '남', '서']
direction = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def next(i):
    if i + 1 > 3:
        return 0
    return i + 1


def next_r(i):
    if i - 1 < 0:
        return 3
    return i - 1


def get_movable_method(table, r, c):
    if (r > -2 and r < R - 1):
        if (r == -1):
            if (table[r + 2][c] == 0):
                return 1
        else:
            if (table[r + 1][c - 1] == 0 and table[r + 2][c] == 0 and table[r + 1][c + 1] == 0):
                return 1

    if (c > 2 and r > -2 and r < R - 1):
        if r == -1:
            if (table[0][c - 1] == 0):
                return 2
        elif r == 0:
            if (table[1][c - 1] == 0 and table[1][c - 2] == 0 and table[2][c - 1] == 0):
                return 2
        elif r == 1:
            if (table[1][c - 2] == 0 and table[2][c - 1] == 0 and table[2][c - 2] == 0 and table[3][c - 1] == 0):
                return 2
        else:
            if (table[r][c - 2] == 0 and table[r - 1][c - 1] == 0 and table[r + 1][c - 1] == 0 and table[r + 1][
                c - 2] == 0 and table[r + 2][c - 1] == 0):
                return 2

    if (c < C - 1 and r > -2 and r < R - 1):
        if r == -1:
            if (table[0][c + 1] == 0):
                return 3
        elif r == 0:
            if (table[1][c + 1] == 0 and table[1][c + 2] == 0 and table[2][c + 1] == 0):
                return 3
        elif r == 1:
            if (table[1][c + 2] == 0 and table[2][c + 1] == 0 and table[2][c + 2] == 0 and table[3][c + 1] == 0):
                return 3
        else:
            if (table[r][c + 2] == 0 and table[r - 1][c + 1] == 0 and table[r + 1][c + 1] == 0 and table[r + 1][
                c + 2] == 0 and table[r + 2][c + 1] == 0):
                return 3

    return -1


def move(order, method, r, c):
    if method == 1:
        return r + 1, c
    elif method == 2:
        directs[order] = next_r(directs[order])
        return r + 1, c - 1
    elif method == 3:
        directs[order] = next(directs[order])
        return r + 1, c + 1

    return r, c

def get_score(order, table, r, c):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    queue = deque([(r, c)])
    visited = set([(r, c)])

    final_row = r
    while queue:
        x, y = queue.popleft()
        if x >= final_row:
            final_row = x

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if 1 <= nx <= R and 1 <= ny <= C:
                if (nx, ny) not in visited and table[nx][ny] == order:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    print(final_row)
    return final_row

# 1-1. 골렘 이동
#   - 구현
# 1-2. 정령 이동
#   - DFS

# 골렘 이동 후 정령 위치
fairy = [R - 1, cols[1]]
# 골렘 위치 마킹
table[fairy[0]][fairy[1]] = 1
for i in range(4):
    table[fairy[0] + direction[i][0]][fairy[1] + direction[i][1]] = 1
# 정렬 이동
fairy[0] = R
# 점수 합산
score += fairy[0]

for i in range(2, K+1):
    r, c = -1, cols[i]
    method = get_movable_method(table, r, c)
    while True:
        if method == -1:
            if r < 2:
                table = [[0] * (C + 1) for i in range(R + 1)]
                for i in range(R + 1):
                    table[i][0] = -1
                for i in range(C + 1):
                    table[0][i] = -1
            else:
                table[r][c] = i
                for j in range(4):
                    table[r + direction[j][0]][c + direction[j][1]] = i
                score += get_score(i, table, r, c)
            break
        r, c = move(i, method, r, c)
        method = get_movable_method(table, r, c)

for t in table:
    print(t)
print(score)