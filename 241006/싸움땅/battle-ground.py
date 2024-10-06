import dataclasses
from dataclasses import dataclass

n, m, k = 0, 0, 0
players = []
p_map = []
g_map = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


@dataclass
class Player:
    idx: int
    x: int
    y: int
    direction: int
    stat: int
    gun: int = 0
    point: int = 0
    def get_power(self):
        return self.stat + self.gun

def is_valid(x, y):
    return 0 <= x < n and 0 <= y < n

def get_reversed_direction(direction):
    if direction > 1:
        return direction - 2
    else:
        return direction + 2


def move_from_to(player, to_x, to_y):
    from_x, from_y = player.x, player.y
    p_map[to_x][to_y] = player.idx

    if p_map[from_x][from_y] == player.idx:
        p_map[from_x][from_y] = 0

    player.x, player.y = to_x, to_y

def exchange_gun(player):
    x, y = player.x, player.y

    guns = g_map[x][y]
    if isinstance(guns, int):
        if guns != 0 and guns > player.gun:
            old_gun = player.gun
            player.gun = guns
            g_map[x][y] = old_gun

    elif isinstance(guns, list):
        max_gun = player.gun
        idx = -1
        for i in range(len(guns)):
            if guns[i] > max_gun:
                max_gun = guns[i]
                idx = i

        if idx != -1:
            new_guns = []
            for i in range(len(guns)):
                if i != idx:
                    new_guns.append(guns[i])
            if player.gun > 0:
                new_guns.append(player.gun)
            player.gun = max_gun
            g_map[x][y] = new_guns

def drop_gun(player, x, y):
    guns = g_map[x][y]

    if player.gun == 0:
        return

    if isinstance(guns, int):
        new_guns = [guns, player.gun]
        player.gun = 0
        g_map[x][y] = new_guns
    elif isinstance(guns, list):
        guns.append(player.gun)
        player.gun = 0

def get_next_direction(direction):
    if direction + 1 >= 4:
        return 0
    return direction + 1

def move_loser(winner, loser, x, y):
    to_x, to_y = x + dx[loser.direction], y + dy[loser.direction]
    while True:
        if not is_valid(to_x, to_y):
            direction = get_next_direction(loser.direction)
            to_x, to_y = x + dx[direction], y + dy[direction]
            loser.direction = direction

        if p_map[to_x][to_y] == 0 or p_map[to_x][to_y] == winner.idx:
            break
        direction = get_next_direction(loser.direction)
        to_x, to_y = x + dx[direction], y + dy[direction]
        loser.direction = direction

    move_from_to(loser, to_x, to_y)
    exchange_gun(loser)

def move(player, to_x, to_y):
    if p_map[to_x][to_y] != 0:
        enemy = players[p_map[to_x][to_y] - 1]

        player_power = player.get_power()
        enemy_power = enemy.get_power()
        diff = abs(player_power - enemy_power)
        # enemy 가 원래 to_x, to_y 에 있던 애
        # player는 아직 to_x, to_y 로 옮기지 않음(코드상)
        if player_power < enemy_power: # winner = enemy
            drop_gun(player, to_x, to_y)
            move_loser(enemy, player, to_x, to_y)
            exchange_gun(enemy)
            enemy.point += diff
        elif player_power > enemy_power: # winner = player
            drop_gun(enemy, to_x, to_y)
            move_loser(player, enemy, to_x, to_y)
            move_from_to(player, to_x, to_y)
            exchange_gun(player)
            player.point += diff
        else:
            if player.stat < enemy.stat: # winner = enemy
                drop_gun(player, to_x, to_y)
                move_loser(enemy, player, to_x, to_y)
                exchange_gun(enemy)
                enemy.point += diff
            else: # winner = player
                drop_gun(enemy, to_x, to_y)
                move_loser(player, enemy, to_x, to_y)
                move_from_to(player, to_x, to_y)
                exchange_gun(player)
                player.point += diff

    else:
        move_from_to(player, to_x, to_y)
        exchange_gun(player)


def do_round():
    for i in range(m):
        player = players[i]
        nx, ny = player.x + dx[player.direction], player.y + dy[player.direction]

        if is_valid(nx, ny):
            move(player, nx, ny)
        else:
            r_direction = get_reversed_direction(player.direction)
            player.direction = r_direction
            nx, ny = player.x + dx[r_direction], player.y + dy[r_direction]
            move(player, nx, ny)


def print_result():
    for i in range(m):
        print(players[i].point, end=' ')

def main():
    global n, m, k, players, p_map, g_map
    n, m, k = map(int, input().split())

    p_map = [[0] * n for _ in range(n)]
    g_map = [[0] * n for _ in range(n)]

    for i in range(n):
        g_map[i] = list(map(int, input().split()))

    for i in range(1, m + 1):
        x, y, d, s = map(int, input().split())
        players.append(Player(i, x - 1, y - 1, d, s))
        p_map[x - 1][y - 1] = i

    for i in range(k):
        do_round()

    print_result()

if __name__ == '__main__':
    main()