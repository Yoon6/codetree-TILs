import java.io.*;
import java.util.*;

class Point {

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int x;
    public int y;
}

public class Main {
    static int n = 0;
    static int m = 0;
    static int k = 0;
    static int round = 0;
    static int[][] table = null;
    static int[][] attackCount = null;
    static boolean[][] visited = null;
    static int[][][] route = null;
    static int activeCount = 0;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        n = Integer.parseInt(st.nextToken());
        m = Integer.parseInt(st.nextToken());
        k = Integer.parseInt(st.nextToken());

        table = new int[n][m];
        attackCount = new int[n][m];
        visited = new boolean[n][m];
        route = new int[n][m][2];

        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < m; j++) {
                table[i][j] = Integer.parseInt(st.nextToken());
                attackCount[i][j] = 0;
                visited[i][j] = false;
                route[i][j][0] = -1;
                route[i][j][1] = -1;
                if (table[i][j] > 0) {
                    activeCount++;
                }
            }
        }

        while (k-- > 0) {
            Point attacker = findAttacker();
            Point target = findTarget(attacker);

            findRazerRoute(attacker, target);

            if (route[target.x][target.y][0] != -1) {
                attackByRazer(attacker, target);
            } else {
                attackByBomb(attacker, target);
            }

            repair();
            if (activeCount <= 1) {
                break;
            }
            resetRoute();
        }
        int max = -1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (table[i][j] > max) {
                    max = table[i][j];                    
                }
            }
        }
        System.out.println(max);
    }

    public static void resetRoute() {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                route[i][j][0] = -1;
                route[i][j][1] = -1;
                visited[i][j] = false;
            }
        }
    }

    public static Point findAttacker() {
        int x = -1;
        int y = -1;
        int min = 9999;
        int count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (table[i][j] <= 0) continue;
                if (table[i][j] > min) continue;
                if (table[i][j] == min) {
                    if (attackCount[i][j] < count) continue;
                    if (attackCount[i][j] == count) {
                        if (i + j < x + y) continue;
                        if (i + j == x + y) {
                            if (j <= y) continue;
                        }
                    }                    
                }

                min = table[i][j];
                count = attackCount[i][j];
                x = i;
                y = j;
            }
        }

        attackCount[x][y] = ++round;
        table[x][y] += (n + m);

        return new Point(x, y);
    }

    public static Point findTarget(Point attacker) {
        int x = n;
        int y = m;
        int max = -1;
        int count = round;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (i == attacker.x && j == attacker.y) continue;
                if (table[i][j] <= 0) continue;
                if (table[i][j] < max) continue;
                if (table[i][j] == max) {
                    if (attackCount[i][j] > count) continue;
                    if (attackCount[i][j] == count) {
                        if (i + j > x + y) continue;
                        if (i + j == x + y) {
                            if (j > y) continue;
                        }
                    }
                }

                max = table[i][j];
                count = attackCount[i][j];
                x = i;
                y = j;
            }
        }

        return new Point(x, y);
    }

    public static int[][] get4Direction(int x, int y) {
        int[][] result = new int[4][2];

        int[][] offset = {
            {0, 1},
            {1, 0},
            {0, -1},
            {-1, 0}
        };

        for (int i = 0; i < offset.length; i++) {
            int nx = x + offset[i][0];
            int ny = y + offset[i][1];

            if (nx >= n) nx = 0;
            if (nx < 0) nx = n - 1;
            if (ny >= m) ny = 0;
            if (ny < 0) ny = m - 1;

            result[i][0] = nx;
            result[i][1] = ny;
        }

        return result;
    }


    public static void findRazerRoute(Point attacker, Point target) {
        Queue<int[]> q = new LinkedList<>();

        q.add(new int[]{ attacker.x, attacker.y });
        route[attacker.x][attacker.y][0] = -2;
        route[attacker.x][attacker.y][1] = -2;

        while (!q.isEmpty()) {
            int[] cur = q.remove();
            int x = cur[0];
            int y = cur[1];

            if (x == target.x && y == target.y) {
                break;
            }

            int[][] offset = {
                {0, 1},
                {1, 0},
                {0, -1},
                {-1, 0}
            };

            int[][] range = getDirection(x, y, offset);

            for (int i = 0; i < range.length; i++) {
                int nx = range[i][0];
                int ny = range[i][1];
                if (table[nx][ny] > 0 && route[nx][ny][0] == -1) {
                    q.add(new int[]{nx, ny});
                    route[nx][ny][0] = x;
                    route[nx][ny][1] = y;
                }
            }
        }
    }

    public static void attackByRazer(Point attacker, Point target) {
        int attack = table[attacker.x][attacker.y];
        int x = target.x;
        int y = target.y;

        while (true) {
            visited[x][y] = true;

            if (x == attacker.x && y == attacker.y) break;
            if (x == target.x && y == target.y) {
                table[x][y] -= attack;
            } else {
                table[x][y] -= (attack / 2);
            }

            int[] temp = route[x][y];
            x = temp[0];
            y = temp[1];
        }
    }

    public static int[][] getDirection(int x, int y, int[][] offset) {
        int[][] result = new int[offset.length][2];

        for (int i = 0; i < offset.length; i++) {
            int nx = x + offset[i][0];
            int ny = y + offset[i][1];

            if (nx >= n) nx = 0;
            if (nx < 0) nx = n - 1;
            if (ny >= m) ny = 0;
            if (ny < 0) ny = m - 1;

            result[i][0] = nx;
            result[i][1] = ny;
        }

        return result;
    }

    public static void attackByBomb(Point attacker, Point target) {
        int[][] offset = {
            {1, 0},
            {1, 1},
            {0, 1},
            {1, -1},
            {-1, 0},
            {-1, -1},
            {0, -1},
            {-1, 1}
        };


        int[][] attackRange = getDirection(target.x, target.y, offset);
        int attack = table[attacker.x][attacker.y];
        visited[attacker.x][attacker.y] = true;
        visited[target.x][target.y] = true;
        table[target.x][target.y] -= attack;

        for (int i = 0; i < 8; i++) {
            int x = attackRange[i][0];
            int y = attackRange[i][1];
            if (table[x][y] <= 0) continue; 
            visited[x][y] = true;
            if (x == attacker.x && y == attacker.y) continue;
            table[x][y] -= (attack/2); 
        }
    }

    public static void repair() {
        activeCount = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (table[i][j] > 0 && !visited[i][j]) {
                    table[i][j] += 1;
                }
                if (table[i][j] > 0) {
                    activeCount++;
                }

            }
        }
    }

}