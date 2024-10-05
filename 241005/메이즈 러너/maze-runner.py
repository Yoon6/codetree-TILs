import copy
from dataclasses import dataclass

N, M, K = 0, 0, 0
miro = []
exit_x = 0
exit_y = 0
players = []
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


@dataclass
class Player:
    x: int
    y: int
    move_count: int = 0
    is_exit: bool = False


def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N


def is_empty_miro(x, y):
    return miro[x][y] == 0 or miro[x][y] == -1


def is_all_exited():
    all_exited = True
    for i in range(M):
        if not players[i].is_exit:
            all_exited = False
            break
    return all_exited


def make_smallest_square(x1, y1, x2, y2, length):
    mx = max(x1, x2)
    my = max(y1, y2)

    x = 0
    y = 0

    for i in reversed(range(length + 1)):
        if 0 <= mx - i < N:
            x = mx - i
            mx += (length - i)
            break
    for i in reversed(range(length + 1)):
        if 0 <= my - i < N:
            y = my - i
            my += (length - i)
            break

    return min(x, mx), min(y, my), max(x, mx), max(y, my)


def get_square_range():
    mx1, my1, mx2, my2 = N, N, 0, 0
    min_length = 999

    for i in range(M):
        if players[i].is_exit:
            continue

        px, py = players[i].x, players[i].y

        width = abs(exit_x - px)
        height = abs(exit_y - py)
        length = max(width, height)
        x1, y1, x2, y2 = make_smallest_square(px, py, exit_x, exit_y, length)

        if length < min_length:
            min_length = length
            mx1, my1, mx2, my2 = x1, y1, x2, y2

        elif length == min_length:
            if x1 < mx1:
                mx1, my1, mx2, my2 = x1, y1, x2, y2
            elif x1 == mx1:
                if y1 < my1:
                    mx1, my1, mx2, my2 = x1, y1, x2, y2

    return mx1, my1, mx2, my2


def get_players_in_range(x1, y1, x2, y2):
    players_in_range = []

    for i in range(len(players)):
        if players[i].is_exit:
            continue
        if x1 <= players[i].x <= x2 and y1 <= players[i].y <= y2:
            players_in_range.append(players[i])

    return players_in_range


def rotate_90_clock_wise(x1, y1, x2, y2):
    global exit_x, exit_y
    n = abs(x1 - x2) + 1
    copy_miro = [[0] * n for _ in range(n)]

    i, j = 0, 0
    for x in range(x1, x2 + 1):
        j = 0
        for y in range(y1, y2 + 1):
            copy_miro[i][j] = miro[x][y]
            j += 1
        i += 1

    players_in_range = get_players_in_range(x1, y1, x2, y2)
    is_used = [False] * len(players_in_range)
    sub_copy_miro = copy.deepcopy(copy_miro)
    for x in range(n):
        for y in range(n):
            copy_miro[x][y] = sub_copy_miro[n - y - 1][x]
            for i in range(len(players_in_range)):
                if is_used[i]:
                    continue
                px, py = players_in_range[i].x, players_in_range[i].y
                if px - x1 == n - y - 1 and py - y1 == x:
                    players_in_range[i].x, players_in_range[i].y = x + x1, y + y1
                    is_used[i] = True

    i, j = 0, 0
    for x in range(x1, x2 + 1):
        j = 0
        for y in range(y1, y2 + 1):
            miro[x][y] = copy_miro[i][j]
            j += 1
        i += 1
    # exit_x, exit_y 변경 필요.

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if miro[x][y] == -1:
                exit_x = x
                exit_y = y


def damage_to_wall(x1, y1, x2, y2):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if miro[x][y] > 0:
                miro[x][y] -= 1


def rotate():
    x1, y1, x2, y2 = get_square_range()
    rotate_90_clock_wise(x1, y1, x2, y2)
    damage_to_wall(x1, y1, x2, y2)


def find_next_pos(player):
    x, y = player.x, player.y
    min_distance = get_distance(x, y, exit_x, exit_y)
    for i in range(4):
        nx, ny = player.x + dx[i], player.y + dy[i]
        if is_valid(nx, ny) and is_empty_miro(nx, ny):
            distance = get_distance(exit_x, exit_y, nx, ny)
            if distance < min_distance:
                min_distance = distance
                x, y = nx, ny

    return x, y


def move():
    for i in range(M):
        if players[i].is_exit:
            continue
        x, y = find_next_pos(players[i])
        if players[i].x != x or players[i].y != y:
            players[i].move_count += 1
            players[i].x = x
            players[i].y = y
        if x == exit_x and y == exit_y:
            players[i].is_exit = True


def print_result():
    result = 0
    for i in range(M):
        result += players[i].move_count

    print(result)
    print(exit_x+1, exit_y+1, sep=' ')


def main():
    global N, M, K, miro, exit_x, exit_y
    N, M, K = map(int, input().split())
    miro = [[0] * N for _ in range(N)]
    for i in range(N):
        miro[i] = list(map(int, input().split()))

    for i in range(M):
        x, y = map(int, input().split())
        players.append(Player(x - 1, y - 1))

    exit_x, exit_y = map(int, input().split())
    exit_x -= 1
    exit_y -= 1
    miro[exit_x][exit_y] = -1

    for i in range(K): # i == 5
        if is_all_exited():
            break
        move()
        rotate()

    print_result()


if __name__ == '__main__':
    main()