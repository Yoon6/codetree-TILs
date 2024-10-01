from dataclasses import dataclass


@dataclass
class Knight:
    idx: int
    r: int
    c: int
    h: int
    w: int
    k: int
    hp: int
    is_dead: bool = False


L, N, Q = 0, 0, 0
maps = []  # 벽, 함정
table = []  # 기사
knights = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def print_result():
    result = 0

    for i in range(len(knights)):
        knight = knights[i]
        if not knight.is_dead:
            result += (knight.k - knight.hp)

    print(result)

def has_wall(r, c, w, h):
    for x in range(r, r+h):
        for y in range(c, c+w):
            if x < 0 or x >= L or y < 0 or y >= L:
                return True
            if maps[x][y] == 2:
                return True
    return False

def find_effected_knights(cur, r, c, w, h):
    effected_knights = []
    for x in range(r, r+h):
        for y in range(c, c+w):
            if table[x][y] != 0 and table[x][y] != cur:
                effected_knights.append(knights[table[x][y]-1])
    return effected_knights

def move(depth, knight, direction):
    nx, ny = knight.r + dx[direction], knight.c + dy[direction]
    effected_knights = find_effected_knights(knight.idx, nx, ny, knight.w, knight.h)

    for i in range(len(effected_knights)):
        move(depth + 1, effected_knights[i], direction)

    for r in range(knight.r, knight.r + knight.h):
        for c in range(knight.c, knight.c + knight.w):
            table[r][c] = 0

    if depth != 0:
        damage = 0
        for r in range(nx, nx + knight.h):
            for c in range(ny, ny + knight.w):
                if maps[r][c] == 1:
                    damage += 1

        knight.hp -= damage
        if knight.hp <= 0:
            knight.is_dead = True

    if not knight.is_dead:
        for r in range(nx, nx + knight.h):
            for c in range(ny, ny + knight.w):
                table[r][c] = knight.idx

    knight.r = nx
    knight.c = ny


def can_move(knight, direction):
    nx, ny = knight.r + dx[direction], knight.c + dy[direction]
    effected_knights = find_effected_knights(knight.idx, nx, ny, knight.w, knight.h)

    is_movable = True
    for i in range(len(effected_knights)):
        if not can_move(effected_knights[i], direction):
            is_movable = False
            break

    if is_movable:
        if has_wall(nx, ny, knight.w, knight.h):
            is_movable = False

    return is_movable



def command_knight(knight, direction):
    if can_move(knight, direction):
        move(0, knight, direction)

def main():
    global L, N, Q, maps, table
    L, N, Q = map(int, input().split())
    maps = [[0] * L for _ in range(L)]
    table = [[0] * L for _ in range(L)]

    for i in range(L):  # 맵 정보
        maps[i] = list(map(int, input().split()))

    for i in range(1, N + 1):  # 기사 정보
        r, c, h, w, k = map(int, input().split())
        knights.append(Knight(i, r-1, c-1, h, w, k, k))
        for x in range(r-1, r+h-1):
            for y in range(c-1, c+w-1):
                table[x][y] = i

    for i in range(Q):  # 명령
        num, direction = map(int, input().split())
        command_knight(knights[num - 1], direction)

    print_result()


if __name__ == "__main__":
    main()