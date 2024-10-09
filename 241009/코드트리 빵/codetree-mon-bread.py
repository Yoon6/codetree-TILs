from dataclasses import dataclass
from enum import Enum

n, m = 0,0

maps = []
stores = []
players = []
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

class State(Enum):
    READY=0
    PLAYING=1
    FINISHED=2

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

def can_placing(x, y):
    return maps[x][y] != -1

def is_all_finished():
    all_finished = True

    for i in range(m):
        if players[i].state != State.FINISHED:
            all_finished = False
            break

    return all_finished

def move_to_store(player):
    mx, my = player.x, player.y
    tx, ty = player.get_target_pos()
    m_distance = get_distance(mx, my, tx, ty)
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

def init(player):
    tx, ty = player.get_target_pos()
    mx, my = 0, 0
    m_distance = 999
    for x in range(n):
        for y in range(n):
            if maps[x][y] != 1:
                continue
            distance = get_distance(x, y, tx, ty)
            if distance < m_distance:
                m_distance = distance
                mx, my = x, y
            elif distance == m_distance:
                if x < mx:
                    mx, my = x, y
                elif x == mx:
                    if y < my:
                        my, mx = x, y

    player.x, player.y = mx, my
    player.state = State.PLAYING
    maps[mx][my] = 0

def move(time):
    for i in range(m):
        if players[i].state == State.PLAYING:
            move_to_store(players[i])
        if time-1 == i:
            init(players[i])

def main():
    global n, m, maps
    n, m = map(int, input().split())

    maps = [[0]*n for _ in range(n)]
    for i in range(n):
        maps[i] = list(map(int, input().split()))
    for i in range(m):
        x, y = map(int, input().split())
        stores.append((x-1, y-1))
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