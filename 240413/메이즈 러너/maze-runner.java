import java.io.*;
import java.util.*;

public class Main {
    private int n, m, k;
    private int[][] table;
    private int[][] players;
    private int[] exit;
    private boolean[] moved;
    private int count = 0;

    Main(int n, int m, int k, int[][] table, int[][] players, int[] exit) {
        this.n = n;
        this.m = m;
        this.k = k;
        this.table = table;
        this.players = players;
        this.exit = exit;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        int[][] table = new int[n][n];
        int[][] players = new int[m][2];
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++) {
                table[i][j] = Integer.parseInt(st.nextToken());
            }
        }

        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken()) - 1;
            int y = Integer.parseInt(st.nextToken()) - 1;

            players[i][0] = x;
            players[i][1] = y;
        }
        st = new StringTokenizer(br.readLine());
        int x = Integer.parseInt(st.nextToken()) - 1;
        int y = Integer.parseInt(st.nextToken()) - 1;

        int[] exit = new int[]{x, y};

        Main instance = new Main(n,m,k,table, players, exit);
        instance.run();
        br.close();
    }

    int getDistance(int r1, int c1, int r2, int c2) {
        return Math.abs(r1 - r2) + Math.abs(c1 - c2);
    }

    List<int[]> getPlayerMoveRoutes() {
        List<int[]> routes = new ArrayList<>();
        int[][] offset = {
            {-1, 0},
            {1, 0},
            {0, 1},
            {0, -1}
        };


        for (int i = 0; i < players.length; i++) {
            int x = players[i][0];
            int y = players[i][1];
            int max = getDistance(x, y, exit[0], exit[1]);

            for (int k = 0; k < offset.length; k++) {
                int nx = x + offset[k][0];
                int ny = y + offset[k][1];

                if (nx < 0 || nx >= n || ny < 0 || ny >= n) {
                    continue;
                }

                if (table[nx][ny] != 0) {
                    continue;
                }

                int distance = getDistance(nx, ny, exit[0], exit[1]);
                if (distance >= max) {
                    continue;
                }

                x = nx;
                y = ny;
                break;
            }
            if (x != players[i][0] || y != players[i][1]) {
                routes.add(new int[]{players[i][0], players[i][1], x, y});
            }
        }

        return routes;
    }

    void movePlayers(List<int[]> routes) {
        if (routes.size() == 0) {
            return;
        }
        

        for (int[] r : routes) {
            int r1 = r[0];
            int c1 = r[1];
            int r2 = r[2];
            int c2 = r[3];
            for (int j = 0; j < players.length; j++) {
                if (players[j][0] == r1 && players[j][1] == c1) {
                    if (exit[0] == r2 && exit[1] == c2) {
                        r2 = -1;
                        c2 = -1;
                    }
                    players[j][0] = r2;
                    players[j][1] = c2;
                    break;
                }
            }
            count++;
        }
    }
    
    boolean hasPlayer() {
        for (int i = 0; i < m; i++) {
            if (players[i][0] != -1) {
                return true;
            }
        }
        return false;
    }

    int[] getRotateRange() {
        int[] range = new int[]{exit[0], exit[1], -1, -1};

        int min = 99;
        for (int i = 0; i < players.length; i++) {
            int r = players[i][0];
            int c = players[i][1];

            if (r == -1) continue;
            int temp = Math.max(Math.abs(range[0]-r), Math.abs(range[1]-c));
            if (range[2] == -1 || min > temp) {
                min = temp;
                range[2] = r;
                range[3] = c;
                continue;
            };

            if (min == temp) {
                if (range[2] > r) {
                    min = temp;
                    range[2] = r;
                    range[3] = c;
                    continue;
                }
                if (range[2] == r) {
                    if (range[3] > c) {
                        min = temp;
                        range[2] = r;
                        range[3] = c;
                        continue;
                    }
                }
            }
        }

        int width = Math.abs(range[0] - range[2]);
        int height = Math.abs(range[1] - range[3]);
        int size = Math.max(width, height);
        boolean isEnd = false;
        for (int i = 0; i < n - size; i++) {
            for (int j = 0; j < n - size; j++) {
                if (range[0] < i || range[0] > i + size) continue;
                if (range[1] < j || range[1] > j + size) continue;
                if (range[2] < i || range[2] > i + size) continue;
                if (range[3] < j || range[3] > j + size) continue;

                range[0] = i;
                range[1] = j;
                range[2] = i + size;
                range[3] = j + size;
                isEnd = true;
                break;
            }
            if (isEnd) break;
        }
        return range;
    }

    void rotateRange(int r1, int c1, int r2, int c2) {
        int[][] rotatedTable = new int[n][n];

        moved = new boolean[m];
        boolean isExitMoved = false;
        for (int i = 0; i < m; i++) moved[i] = false;
        for (int i = r1; i <= r2; i++) {
            for (int j = c1; j <= c2; j++) {
                rotatedTable[j + r1 - c1][c1 + r2 - i] = table[i][j];
                for (int k = 0; k < m; k++) {
                    if (!moved[k] && players[k][0] == i && players[k][1] == j) {
                        players[k][0] = j + r1 - c1;
                        players[k][1] = c1 + r2 - i;
                        moved[k] = true;
                    }
                }
                if (!isExitMoved && exit[0] == i && exit[1] == j) {
                    //System.out.printf("i = %d, j = %d, r2-i = %d\n", i, j, r2-i);
                    exit[0] = j + r1 - c1;
                    exit[1] = c1 + r2 - i;
                    isExitMoved = true;
                }
            }
        }

        for (int i = r1; i <= r2; i++) {
            for (int j = c1; j <= c2; j++) {
                table[i][j] = rotatedTable[i][j];
                if (table[i][j] > 0) {
                    table[i][j] -= 1;
                }
            }
        }
    }



    void run() {
        while (k-- > 0) {
            //System.out.println("============");
            List<int[]> routes = getPlayerMoveRoutes();
            /*
            for (int[] r : routes) {
                System.out.println(Arrays.toString(r));
            }
            */
            movePlayers(routes);
            /*
            for (int[] p : players) {
                System.out.println("players="+Arrays.toString(p));
            }
            */
            if (!hasPlayer()) {
                break;
            }
            int[] range = getRotateRange();
            rotateRange(range[0], range[1], range[2], range[3]);

/*
            System.out.printf("range= %d, %d <-> %d, %d\n", range[0], range[1], range[2], range[3]);
            System.out.printf("exit= %d, %d\n", exit[0], exit[1]);
            for (int[] p : players) {
                System.out.println("players="+Arrays.toString(p));
            }

            for (int i = 0; i < n; i++) {
                System.out.println(Arrays.toString(table[i]));
            }
            */
        }

        System.out.println(count);
        System.out.println((exit[0]+1) + " " + (exit[1]+1));
    }
}