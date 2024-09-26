from dataclasses import dataclass
from enum import Enum
from collections import deque

MAX_RC = 70
R, C, K = 0, 0, 0
table = [[0] * MAX_RC for i in range(MAX_RC + 3)]

golems = []
score = 0


def is_valid(r, c):
    global table

    if 0 <= r <= R + 3 - 1 and 0 <= c <= C - 1 and table[r][c] == 0:
        return True

    return False


def reset_table():
    global table
    table = [[0] * MAX_RC for i in range(MAX_RC + 3)]


def get_score(golem):
    global table

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    r, c = golem.r, golem.c

    queue = deque([(r, c)])
    visited = set([(r, c)])

    final_row = r
    while queue:
        x, y = queue.popleft()
        if x >= final_row:
            final_row = x

        cur = table[x][y]
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx <= R + 3 - 1 and 0 <= ny <= C - 1:
                if (nx, ny) not in visited:
                    exit_x, exit_y = golems[cur-1].get_exit()
                    if exit_x == x and exit_y == y:
                        if table[nx][ny] != 0:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                    elif table[nx][ny] == cur:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

    return final_row


@dataclass
class Golem:
    id: int
    r: int
    c: int
    exit: int

    def get_exit(self) -> (int, int):
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        return self.r + dx[self.exit], self.c + dy[self.exit]

    def can_move(self):
        if is_valid(self.r + 1, self.c - 1) and is_valid(self.r + 2, self.c) and is_valid(
                self.r + 1, self.c + 1):
            return Moving.SOUTH

        if is_valid(self.r - 1, self.c - 1) and is_valid(self.r, self.c - 2) and is_valid(
                self.r + 1, self.c - 1) and is_valid(self.r + 1, self.c - 2) and is_valid(
            self.r + 2, self.c - 1):
            return Moving.WEST

        if is_valid(self.r - 1, self.c + 1) and is_valid(self.r, self.c + 2) and is_valid(
                self.r + 1, self.c + 1) and is_valid(self.r + 1, self.c + 2) and is_valid(self.r + 2,
                                                                                          self.c + 1):
            return Moving.EAST
        return Moving.NONE

    def move(self, moving):
        if moving is Moving.SOUTH:
            self.r += 1
        elif moving is Moving.WEST:
            self.r += 1
            self.c -= 1
            self.exit -= 1
            if self.exit < 0:
                self.exit = 3
        elif moving is Moving.EAST:
            self.r += 1
            self.c += 1
            self.exit += 1
            if self.exit > 3:
                self.exit = 0

    def is_in_table(self):
        return self.r >= 4

    def mark_in_table(self):
        global table
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        table[self.r][self.c] = self.id
        for i in range(4):
            table[self.r + dx[i]][self.c + dy[i]] = self.id


class Moving(Enum):
    NONE = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


def main():
    global R, C, K, score
    R, C, K = map(int, input().split())

    for i in range(K):
        ci, di = map(int, input().split())
        golems.append(Golem(id=i + 1, r=1, c=ci - 1, exit=di))

    for i in range(K):
        golem = golems[i]
        moving = golem.can_move()
        while moving is not Moving.NONE:
            golem.move(moving)
            moving = golem.can_move()

        if golem.is_in_table():
            golem.mark_in_table()
            score += get_score(golem) - 2
        else:
            reset_table()

    print(score)


if __name__ == '__main__':
    main()