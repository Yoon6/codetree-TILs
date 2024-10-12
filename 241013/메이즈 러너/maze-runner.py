n,m,k = map(int, input().split())

board = [
    [0] * (n+1)
    for _ in range(n+1)
]

for i in range(1, n + 1):
    board[i] = [0] + list(map(int, input().split()))

next_board = [
    [0] * (n+1)
    for _ in range(n+1)
]

traveler = [(-1, -1)] + [
    tuple(map(int, input().split()))
    for _ in range(m)
]

exits = tuple(map(int, input().split()))

ans = 0

sx, sy, s_size = 0,0,0

def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def is_valid(x, y):
    return 1 <= x <= n and 1 <= y <= n

def move_all_traveler():
    global exits, ans
    dx = [-1, 1, 0, 0]
    dy = [0, 0, 1, -1]

    for i in range(1, m+1):
        if traveler[i] == exits:
            continue

        tx, ty = traveler[i]
        ex, ey = exits

        mx, my = tx, ty
        min_distance = get_distance(mx, my, ex, ey)
        for j in range(4):
            nx, ny = tx + dx[j], ty + dy[j]
            distance = get_distance(nx, ny, ex, ey)
            if is_valid(nx, ny) and board[nx][ny] == 0 and distance < min_distance:
                min_distance = distance
                mx, my = nx, ny

        if (tx, ty) != (mx, my):
            traveler[i] = (mx, my)
            ans += 1

def find_minimum_square():
    global sx, sy, s_size

    ex, ey = exits

    for sz in range(2, n+1):
        for x1 in range(1, n - sz + 2):
            for y1 in range(1, n - sz + 2):
                x2, y2 = x1 + sz - 1, y1 + sz - 1

                if not (x1 <= ex <= x2 and y1 <= ey <= y2):
                    continue

                is_traveler_in = False
                for l in range(1, m+1):
                    tx, ty = traveler[l]
                    if x1 <= tx <= x2 and y1 <= ty <= y2:
                        if not (tx == ex and ty == ey):
                            is_traveler_in = True

                if is_traveler_in:
                    sx = x1
                    sy = y1
                    s_size = sz
                    return

def rotate_square():
     for x in range(sx, sx + s_size):
         for y in range(sy, sy + s_size):
            if board[x][y] > 0:
                board[x][y] -= 1

     for x in range(sx, sx + s_size):
         for y in range(sy, sy + s_size):
             ox, oy = x - sx, y - sy
             rx, ry = oy, s_size - ox -1
             next_board[rx + sx][ry + sy] = board[x][y]

     for x in range(sx, sx + s_size):
         for y in range(sy, sy + s_size):
            board[x][y] = next_board[x][y]


def rotate_traveler_and_exit():
    global exits

    for i in range(1, m+1):
        tx, ty = traveler[i]
        if sx <= tx < sx + s_size and sy <= ty < sy + s_size:
            ox, oy = tx - sx, ty - sy
            rx, ry = oy, s_size - ox - 1

            traveler[i] = (rx + sx, ry + sy)

    ex, ey = exits
    if sx <= ex < sx + s_size and sy <= ey < sy + s_size:
        ox, oy = ex - sx, ey - sy
        rx, ry = oy, s_size - ox - 1
        exits = (rx + sx, ry + sy)


for _ in range(k):
    move_all_traveler()

    is_all_escaped = True
    for i in range(1, m + 1):
        if traveler[i] != exits:
            is_all_escaped = False
            break

    if is_all_escaped:
        break

    find_minimum_square()
    rotate_square()
    rotate_traveler_and_exit()


print(ans)
ex, ey = exits
print(ex, ey)