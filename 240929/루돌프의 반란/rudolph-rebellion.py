from dataclasses import dataclass
from enum import Enum
@dataclass
class Santa:
    idx: int
    x: int
    y: int
    score: int = 0
    is_over: bool = False
    stun: int = -2 # 스턴을 받은 턴

class Direction(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

ru_x, ru_y = 0, 0
N, M, P, C, D = 0, 0, 0, 0, 0
santas = []
table = []
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]


def get_distance(r1, c1, r2, c2) -> int:
    return pow(abs(r1 - r2), 2) + pow(abs(c1 - c2), 2)

def end_turn():
    global santas
    count = 0
    total_santas = len(santas)
    for i in range(total_santas):
        santa = santas[i]
        if not santa.is_over:
            santa.score += 1
        else:
            count += 1

    return total_santas == count

def move_in_table(x1, y1, x2, y2):
    global table

    table[x2][y2] = table[x1][y1]
    table[x1][y1] = 0

def is_valid(x, y):
    global N
    return 0<=x<N and 0<=y<N

def do_interaction(direction, x, y):
    global table, santas

    order = table[x][y]
    santa = santas[order-1]

    nx = x + dx[direction]
    ny = y + dy[direction]

    if is_valid(nx, ny):
        if table[nx][ny] != 0:
            do_interaction(direction, nx, ny)

        move_in_table(santa.x, santa.y, nx, ny)
        santa.x, santa.y = nx, ny

def find_nearest_santa(x, y):
    min_distance = 9999
    result_santa = santas[0]
    for i in range(len(santas)):
        santa = santas[i]
        if santa.is_over:
            continue

        distance = get_distance(santa.x, santa.y, x, y)
        if distance < min_distance:
            min_distance = distance
            result_santa = santa
        elif distance == min_distance:
            if santa.x > result_santa.x:
                result_santa = santa
            elif santa.x == result_santa.x:
                if santa.y > result_santa.y:
                    result_santa = santa
    return result_santa

def get_next_position_of_rudolf(x, y, santa):
    min_x, min_y, min_direction = x, y, Direction.N
    min_distance = 9999

    for i in range(len(dx)):
        nx = x + dx[i]
        ny = y + dy[i]
        distance = get_distance(nx, ny, santa.x, santa.y)
        if distance < min_distance:
            min_x, min_y = nx, ny
            min_direction = i
            min_distance = distance

    return min_x, min_y, min_direction



def move_rudolf(turn):
    global ru_x, ru_y, table, C
    santa = find_nearest_santa(ru_x, ru_y)
    x, y, direction = get_next_position_of_rudolf(ru_x, ru_y, santa)

    if table[x][y] != 0: # 충돌하는 경우
        if santa.x == x and santa.y == y:
            nx = x + dx[direction]*C
            ny = y + dy[direction]*C

            if is_valid(nx, ny):
                if table[nx][ny] != 0:
                    do_interaction(direction, nx, ny)

                move_in_table(santa.x, santa.y, nx, ny)
                santa.x, santa.y = nx, ny
                santa.stun = turn
                santa.score += C

            else:
                santa.is_over = True
                santa.score += C

    move_in_table(ru_x, ru_y, x, y)
    ru_x, ru_y = x, y

def get_reversed_direction(direction):
    if direction == Direction.N.value:
        return Direction.S.value
    elif direction == Direction.S.value:
        return Direction.N.value
    elif direction == Direction.E.value:
        return Direction.W.value
    elif direction == Direction.W.value:
        return Direction.E.value

def move_santa(turn, santa):
    if santa.is_over or santa.stun == turn or santa.stun == turn-1:
        return

    min_distance = get_distance(santa.x, santa.y, ru_x, ru_y)
    direction = -1
    for i in range(0, 8, 2):
        nx, ny = santa.x + dx[i], santa.y + dy[i]
        if is_valid(nx, ny):
            distance = get_distance(nx, ny, ru_x, ru_y)
            if distance < min_distance and table[nx][ny] <= 0:
                min_distance = distance
                direction = i

    if direction == -1:
        return

    x, y = santa.x + dx[direction], santa.y + dy[direction]
    if table[x][y] != 0: # 충돌하는 경우
        reversed_direction = get_reversed_direction(direction)
        nx = x + dx[reversed_direction]*D
        ny = y + dy[reversed_direction]*D
        if is_valid(nx, ny):
            if table[nx][ny] != 0:
                do_interaction(reversed_direction, nx, ny)

            move_in_table(santa.x, santa.y, nx, ny)
            santa.x, santa.y = nx, ny
            santa.score += D
            santa.stun = turn
        else:
            santa.is_over = True
            santa.score += D
            table[santa.x][santa.y] = 0
    else:
        move_in_table(santa.x, santa.y, x, y)
        santa.x, santa.y = x, y


def start_turn(turn):
    global santas

    move_rudolf(turn)
    for i in range(len(santas)):
        move_santa(turn, santas[i])
    return end_turn()

def print_result():

    for i in range(len(santas)):
        print(santas[i].score, end=' ')

def print_table():
    for i in range(N):
        print(table[i])

    print_result()
    print()

def main():
    global N, M, P, C, D, ru_x, ru_y, santas, table
    N, M, P, C, D = map(int, input().split())
    ru_x, ru_y = map(int, input().split())
    ru_x -= 1
    ru_y -= 1

    table = [[0] * N for _ in range(N)]
    table[ru_x][ru_y] = -1

    for i in range(P):
        order, x, y = map(int, input().split())
        santas.append(Santa(order, x - 1, y - 1))
        table[x - 1][y - 1] = order

    santas.sort(key=lambda santa: santa.idx)

    game_over = False
    print_table()
    for i in range(M):
        if game_over:
            break
        game_over = start_turn(i)
        print_table()


    print_result()


if __name__ == '__main__':
    main()