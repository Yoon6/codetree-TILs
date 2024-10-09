from dataclasses import dataclass
from enum import Enum
from collections import deque

n, m = 0, 0

maps = []
stores = []
players = []
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]


class State(Enum):
    READY = 0
    PLAYING = 1
    FINISHED = 2


@dataclass
class Person:
    idx: int
    x: int = -1
    y: int = -1
    state: State = State.READY

    def get_target_pos(self):
        return stores[self.idx]


def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_valid(x, y):
    return 0 <= x < n and 0 <= y < n


def can_placing(player, x, y):
    return maps[x][y] != -1


def is_all_finished():
    all_finished = True

    for i in range(m):
        if players[i].state != State.FINISHED:
            all_finished = False
            break

    return all_finished


def move_to_store(player):
    tx, ty = player.get_target_pos()
    px, py = player.x, player.y

    q = deque()
    q.append((px, py))
    visited = set([(px, py)])
    routes = [[0]*n for _ in range(n)]

    routes[px][py] = (-1, -1)

    while q:
        x, y = q.popleft()

        if x == tx and y == ty:
            break

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if (nx, ny) not in visited and is_valid(nx, ny) and maps[nx][ny] != -1:
                q.append((nx, ny))
                visited.add((nx, ny))
                routes[nx][ny] = (x, y)

    x, y = tx, ty
    nx, ny = routes[x][y]

    while True:
        if nx == px and ny == py:
            break
        x, y = nx, ny
        nx, ny = routes[x][y]


    player.x, player.y = x, y
    if x == tx and y == ty:
        player.state = State.FINISHED


    """
    mx, my = 0, 0
    tx, ty = player.get_target_pos()
    m_distance = 999
    for i in range(4):
        nx, ny = player.x + dx[i], player.y + dy[i]
        if is_valid(nx, ny) and can_placing(nx, ny):
            distance = get_distance(nx, ny, tx, ty)
            if distance < m_distance:
                m_distance = distance
                mx, my = nx, ny

    player.x, player.y = mx, my
    if mx == tx and my == ty:
        player.state = State.FINISHED
        maps[tx][ty] = -1
    """


def init(player):
    tx, ty = player.get_target_pos()

    q = deque()
    q.append((tx, ty))
    visited = set([(tx, ty)])
    dis = [[-1] * n for _ in range(n)]
    dis[tx][ty] = 0

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if (nx, ny) not in visited and is_valid(nx, ny) and maps[nx][ny] != -1:
                q.append((nx, ny))
                visited.add((nx, ny))
                dis[nx][ny] = dis[x][y] + 1



    mx, my = 0, 0
    m_distance = 999
    for x in range(n):
        for y in range(n):
            if maps[x][y] != 1:
                continue
            distance = dis[x][y]
            if distance == -1:
                continue
            if distance < m_distance:
                m_distance = distance
                mx, my = x, y
            elif distance == m_distance:
                if x < mx:
                    mx, my = x, y
                elif x == mx:
                    if y < my:
                        mx, my = x, y

    player.x, player.y = mx, my
    player.state = State.PLAYING


def move(time):

    for i in range(m):
        if i == time - 1:
            continue
        if players[i].state == State.PLAYING:
            move_to_store(players[i])

    for i in range(m):
        tx, ty = players[i].get_target_pos()
        if players[i].x == tx and players[i].y == ty:
            maps[tx][ty] = -1

    if time <= m:
        init(players[time-1])
        x, y = players[time-1].x, players[time-1].y
        maps[x][y] = -1


def main():
    global n, m, maps
    n, m = map(int, input().split())

    maps = [[0] * n for _ in range(n)]
    for i in range(n):
        maps[i] = list(map(int, input().split()))
    for i in range(m):
        x, y = map(int, input().split())
        stores.append((x - 1, y - 1))
        players.append(Person(i))

    time = 0

    while True:
        if is_all_finished():
            break
        time += 1
        move(time)

    print(time)


if __name__ == "__main__":
    main()