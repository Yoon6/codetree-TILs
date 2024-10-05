from collections import deque

N, M, K = 0,0,0
count = 0
maps = []
times = []
routes = []

effected_sets = set()

def find_attacker():
    mx, my = -1, -1
    max_time = -1
    minimum = 9999
    for x in range(N):
        for y in range(M):
            if maps[x][y] <= 0:
                continue
            if maps[x][y] < minimum:
                minimum = maps[x][y]
                max_time = times[x][y]
                mx, my = x, y
            elif maps[x][y] == minimum:
                if times[x][y] > max_time:
                    max_time = times[x][y]
                    mx, my = x, y
                elif times[x][y] == max_time:
                    if x + y > mx + my:
                        mx, my = x, y
                    elif x + y == mx + my:
                        if y > my:
                            mx, my = x, y

    maps[mx][my] += (N+M)
    return mx, my

def find_target(from_x, from_y):
    mx, my = -1, -1
    min_time = 9999
    maximum = 0
    for x in range(N):
        for y in range(M):
            if maps[x][y] <= 0:
                continue
            if x == from_x and y == from_y:
                continue
            if maps[x][y] > maximum:
                maximum = maps[x][y]
                min_time = times[x][y]
                mx, my = x, y
            elif maps[x][y] == maximum:
                if times[x][y] < min_time:
                    min_time = times[x][y]
                    mx, my = x, y
                elif times[x][y] == min_time:
                    if x + y < mx + my:
                        mx, my = x, y
                    elif x + y == mx + my:
                        if y < my:
                            mx, my = x, y

    return mx, my

def get_corrected_point(x, y):
    cx, cy = x, y

    if x < 0:
        cx = N-1
    elif x >= N:
        cx = 0

    if y < 0:
        cy = M-1
    elif y >= M:
        cy = 0

    return cx, cy
def can_use_laser(from_x, from_y, to_x, to_y):
    global routes
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    routes = [[0]*M for _ in range(N)]

    queue = deque()
    queue.append((from_x, from_y))
    routes[from_x][from_y] = [-1, -1]


    while queue:
        x, y = queue.popleft()

        if x == to_x and y == to_y:
            return True

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            nnx, nny = get_corrected_point(nx, ny)
            if maps[nnx][nny] > 0 and routes[nnx][nny] == 0:
                queue.append((nnx, nny))
                routes[nnx][nny] = [x, y]

    return False

def attack_by_laser(from_x, from_y, to_x, to_y):
    global count
    power = maps[from_x][from_y]

    maps[to_x][to_y] -= power
    effected_sets.add((to_x, to_y))
    if maps[to_x][to_y] <= 0:
        count -= 1

    x, y = routes[to_x][to_y][0], routes[to_x][to_y][1]

    while True:
        if x == from_x and y == from_y:
            break

        maps[x][y] -= int(power/2)
        if maps[x][y] <= 0:
            count -= 1

        effected_sets.add((x, y))
        x, y = routes[x][y][0], routes[x][y][1]

def attack_by_bomb(from_x, from_y, to_x, to_y):
    global count
    dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
    power = maps[from_x][from_y]
    maps[to_x][to_y] -= power
    effected_sets.add((to_x, to_y))

    if maps[to_x][to_y] <= 0:
        count -= 1

    for i in range(8):
        nx, ny = to_x+dx[i], to_y+dy[i]
        nnx, nny = get_corrected_point(nx, ny)

        if nnx == from_x and nny == from_y:
            continue
        if maps[nnx][nny] <= 0:
            continue

        maps[nnx][nny] -= int(power/2)
        if maps[nnx][nny] <= 0:
            count -= 1
        effected_sets.add((nnx, nny))

def reload(from_x, from_y):
    for x in range(N):
        for y in range(M):
            if maps[x][y] <= 0:
                continue
            if x == from_x and y == from_y:
                continue
            if (x, y) in effected_sets:
                continue
            maps[x][y] += 1

    effected_sets.clear()

def print_result():
    result = 0
    for x in range(N):
        for y in range(M):
            if maps[x][y] > result:
                result = maps[x][y]
    print(result)

def main():
    global N, M, K, maps, times, count
    N, M, K = map(int, input().split())
    maps = [[0]*M for _ in range(N)]
    times = [[0]*M for _ in range(N)]

    for i in range(N):
        maps[i] = list(map(int, input().split()))

    for i in range(N):
        for j in range(M):
            if maps[i][j] > 0:
                count+=1

    for i in range(K): # i == 27

        from_x, from_y = find_attacker()
        to_x, to_y = find_target(from_x, from_y)
        if can_use_laser(from_x, from_y, to_x, to_y):
            attack_by_laser(from_x, from_y, to_x, to_y)
        else:
            attack_by_bomb(from_x, from_y, to_x, to_y)
        reload(from_x, from_y)
        times[from_x][from_y] = i+1

        if count <= 1:
            break

    print_result()

if __name__ == "__main__":
    main()