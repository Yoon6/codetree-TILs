import copy

K, M = 0, 0
next_arr = []
next_idx = 0
scores = []
maps = [[0]*5 for i in range(5)]

def print_result():
    global K
    for i in range(len(scores)):
        if i is not len(scores)-1:
            print(scores[i], end=' ')
        else:
            print(scores[i])


def get_pieces_count(rotated_map):
    visited = set()
    score = 0
    for r in range(5):
        for c in range(5):
            if (r, c) not in visited:
                result = dfs(rotated_map, r, c, visited)
                if len(result) >= 3:
                    score += len(result)

    return score

def calculate(r, c):
    global maps
    max_score = 0
    angle = 0

    maps90 = rotate(maps, r, c)
    score = get_pieces_count(maps90)
    if score > max_score:
        max_score = score
        angle = 90

    maps180 = rotate(maps90, r, c)
    score = get_pieces_count(maps180)
    if score > max_score:
        max_score = score
        angle = 180

    maps270 = rotate(maps180, r, c)
    score = get_pieces_count(maps270)
    if score > max_score:
        max_score = score
        angle = 270


    return max_score, angle

def rotate(maps2, r, c):
    rotated_map = copy.deepcopy(maps2)

    sub_matrix = [row[c-1:c+2] for row in maps2[r-1:r+2]]
    rotated_sub_matrix = list(zip(*sub_matrix[::-1]))
    for i in range(3):
        rotated_map[r-1 + i][c-1:c+2] = rotated_sub_matrix[i]

    return rotated_map

def dfs(maps2, r, c, visited):
    stack = [(r,c)]
    result = []
    cur = maps2[r][c]
    visited.add((r,c))
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    while stack:
        x, y = stack.pop()

        result.append((x, y))

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx < 5 and 0 <= ny <5:
                if maps2[nx][ny] == cur and (nx, ny) not in visited:
                    stack.append((nx, ny))
                    visited.add((nx, ny))


    return result


def remove_pieces():
    global maps

    visited = set()
    score = 0
    for r in range(5):
        for c in range(5):
            if (r, c) not in visited:
                result = dfs(maps, r, c, visited)
                if len(result) >= 3:
                    score += len(result)
                    for (rr, cc) in result:
                        maps[rr][cc] = 0

    return score

def fill_pieces():
    global maps, next_arr, next_idx
    for c in range(5):
        for r in reversed(range(5)):
            if maps[r][c] == 0:
                maps[r][c] = next_arr[next_idx]
                next_idx += 1


def explore():
    global maps, scores
    opt_r = 1
    opt_c = 1
    opt_a = 0
    max_score = 0
    for r in range(1, 4):
        for c in range(1, 4):
            score, angle = calculate(r, c)
            if score > max_score:
                max_score = score
                opt_a = angle
                opt_r = r
                opt_c = c
            elif score == max_score:
                if angle < opt_a:
                    max_score = score
                    opt_a = angle
                    opt_r = r
                    opt_c = c
                elif angle == opt_a:
                    if c < opt_c:
                        max_score = score
                        opt_a = angle
                        opt_r = r
                        opt_c = c
                    elif c == opt_c:
                        if r < opt_r:
                            max_score = score
                            opt_a = angle
                            opt_r = r
                            opt_c = c

    if opt_a == 90:
        maps = rotate(maps, opt_r, opt_c)
    elif opt_a == 180:
        maps = rotate(maps, opt_r, opt_c)
        maps = rotate(maps, opt_r, opt_a)
    elif opt_a == 270:
        maps = rotate(maps, opt_r, opt_c)
        maps = rotate(maps, opt_r, opt_a)
        maps = rotate(maps, opt_r, opt_c)
    sum_score = 0

    while True:
        count = remove_pieces()
        if count == 0:
            break
        sum_score += count
        fill_pieces()

    if sum_score > 0:
        scores.append(sum_score)


def main():
    global K, M, next_arr, maps
    K, M = map(int, input().split())
    for i in range(5):
        maps[i] = list(map(int, input().split()))

    next_arr = list(map(int, input().split()))

    for i in range(K):
        explore()
    print_result()




if __name__ == "__main__":
    main()