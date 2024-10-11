import sys
from collections import deque

INT_MAX = sys.maxsize
EMPTY = (-1, -1)
n, m = tuple(map(int, input().split()))

grid = [
    list(map(int, input().split()))
    for _ in range(n)
]

cvs_list = []
for _ in range(m):
    x, y = map(int, input().split())
    cvs_list.append((x-1, y-1))

people = [EMPTY] * m
curr_t = 0

dxs = [-1,0,0,1]
dys = [0,-1,1,0]

step = [
    [0] * n
    for _ in range(n)
]

visited = [
    [False] * n
    for _ in range(n)
]

def is_valid(x, y):
    return 0 <= x < n and 0 <= y < n

def bfs(start_pos):

    for i in range(n):
        for j in range(n):
            step[i][j] = 0
            visited[i][j] = False

    q = deque()
    q.append(start_pos)
    sx, sy = start_pos

    visited[sx][sy] = True
    step[sx][sy] = 0

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dxs[i], y + dys[i]
            if is_valid(nx, ny) and not visited[nx][ny] and grid[nx][ny] != -1:
                visited[nx][ny] = True
                step[nx][ny] = step[x][y]+1
                q.append((nx, ny))

def simulate():
    for i in range(m):
        if people[i] == EMPTY or people[i] == cvs_list[i]:
            continue
        bfs(cvs_list[i])
        px, py = people[i]

        min_distance = INT_MAX
        min_x, min_y = -1, -1

        for j in range(4):
            nx, ny = px + dxs[j], py + dys[j]
            if is_valid(nx, ny) and visited[nx][ny] and step[nx][ny] < min_distance:
                min_distance = step[nx][ny]
                min_x, min_y = nx, ny

        people[i] = (min_x, min_y)

    for i in range(m):
        if people[i] == cvs_list[i]:
            x, y = people[i]
            grid[x][y] = -1

    if curr_t > m:
        return

    bfs(cvs_list[curr_t-1])

    min_distance = INT_MAX
    min_x, min_y = -1, -1

    for i in range(n):
        for j in range(n):
            if visited[i][j] and grid[i][j] == 1 and step[i][j] < min_distance:
                min_distance = step[i][j]
                min_x, min_y = i, j
    grid[min_x][min_y] = -1
    people[curr_t-1] = (min_x, min_y)


def end():
    for i in range(m):
        if people[i] != cvs_list[i]:
            return False
    return True

while True:
    curr_t += 1
    simulate()
    if end():
        break

print(curr_t)