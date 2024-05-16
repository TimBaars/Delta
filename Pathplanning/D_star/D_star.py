"""
D_star 2D
@author: huiming zhou
"""

import os
import sys
import math
import matplotlib.pyplot as plt

sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory

from Pathplanning.D_star import plotting, env


class DStar:
    def __init__(self, s_start, s_goal):
        self.s_start, self.s_goal = s_start, s_goal

        self.Env = env.Env()
        self.Plot = plotting.Plotting(self.s_start, self.s_goal)

        self.u_set = self.Env.motions
        self.obs = self.Env.obs
        self.x = self.Env.x_range
        self.y = self.Env.y_range

        self.fig = plt.figure()

        self.OPEN = set()
        self.t = dict()
        self.PARENT = dict()
        self.h = dict()
        self.k = dict()
        self.path = []
        self.visited = set()
        self.count = 0

    def init(self):
        for i in range(self.Env.x_range):
            for j in range(self.Env.y_range):
                self.t[(i, j)] = 'NEW'
                self.k[(i, j)] = 0.0
                self.h[(i, j)] = float("inf")
                self.PARENT[(i, j)] = None

        self.h[self.s_goal] = 0.0
        
    def line_of_sight(self, s1, s2):
        """Check if there is a direct line of sight between two nodes, considering the obstacles."""
        x0, y0 = s1
        x1, y1 = s2
        dx = x1 - x0
        dy = y1 - y0
        f = 0
        if dy < 0:
            dy = -dy
            sy = -1
        else:
            sy = 1
        if dx < 0:
            dx = -dx
            sx = -1
        else:
            sx = 1
        if dx >= dy:
            while x0 != x1:
                f += dy
                if f >= dx:
                    if (x0 + ((sx - 1) // 2), y0 + ((sy - 1) // 2)) in self.obs:
                        return False
                    y0 += sy
                    f -= dx
                if f != 0 and (x0 + ((sx - 1) // 2), y0 + ((sy - 1) // 2)) in self.obs:
                    return False
                if dy == 0 and (x0 + ((sx - 1) // 2), y0) in self.obs and (x0 + ((sx - 1) // 2), y0 - 1) in self.obs:
                    return False
                x0 += sx
        else:
            while y0 != y1:
                f += dx
                if f >= dy:
                    if (x0 + ((sx - 1) // 2), y0 + ((sy - 1) // 2)) in self.obs:
                        return False
                    x0 += sx
                    f -= dy
                if f != 0 and (x0 + ((sx - 1) // 2), y0 + ((sy - 1) // 2)) in self.obs:
                    return False
                if dx == 0 and (x0, y0 + ((sy - 1) // 2)) in self.obs and (x0 - 1, y0 + ((sy - 1) // 2)) in self.obs:
                    return False
                y0 += sy
        return True  # If none of the conditions met, there is a line of sight

    def path_simplification(self, path):
        """Method to simplify the path."""
        simplified_path = [path[0]]
        skip = 0

        for i in range(1, len(path)):
            if skip:
                skip -= 1
                continue
            for j in range(len(path) - 1, i, -1):
                if self.line_of_sight(simplified_path[-1], path[j]):
                    simplified_path.append(path[j])
                    skip = j - i - 1
                    break
            if skip == 0 and i == len(path) - 1:
                simplified_path.append(path[i])

        return simplified_path

    def plot_path(self, path, simplified_path=None):
        """Modified method to plot both the original and simplified paths."""
        if simplified_path is None:
            simplified_path = self.path_simplification(path)
        
        # Plot the original path
        px = [x[0] for x in path]
        py = [x[1] for x in path]
        plt.plot(px, py, linewidth=2, label='Original Path')
        
        # Plot the start and goal
        plt.plot(self.s_start[0], self.s_start[1], "bs")  # Start
        plt.plot(self.s_goal[0], self.s_goal[1], "gs")    # Goal

        # Plot the simplified path
        spx = [x[0] for x in simplified_path]
        spy = [x[1] for x in simplified_path]
        plt.plot(spx, spy, linewidth=2, color='red', linestyle='--', label='Simplified Path')
        
        plt.legend()

    def run(self, s_start, s_end):
        self.init()
        self.insert(s_end, 0)

        while True:
            self.process_state()
            if self.t[s_start] == 'CLOSED':
                break

        self.path = self.extract_path(s_start, s_end)
        self.Plot.plot_grid("Dynamic A* (D*)")
        self.plot_path(self.path)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        plt.show()

    def on_press(self, event):
        x, y = event.xdata, event.ydata
        if x < 0 or x > self.x - 1 or y < 0 or y > self.y - 1:
            print("Please choose right area!")
        else:
            x, y = int(x), int(y)
            if (x, y) not in self.obs:
                print("Add obstacle at: s =", x, ",", "y =", y)
                self.obs.add((x, y))
                self.Plot.update_obs(self.obs)

                s = self.s_start
                self.visited = set()
                self.count += 1

                while s != self.s_goal:
                    if self.is_collision(s, self.PARENT[s]):
                        self.modify(s)
                        continue
                    s = self.PARENT[s]

                self.path = self.extract_path(self.s_start, self.s_goal)

                plt.cla()
                self.Plot.plot_grid("Dynamic A* (D*)")
                self.plot_visited(self.visited)
                self.plot_path(self.path)

            self.fig.canvas.draw_idle()

    def extract_path(self, s_start, s_end):
        path = [s_start]
        s = s_start
        while True:
            s = self.PARENT[s]
            path.append(s)
            if s == s_end:
                return path

    def process_state(self):
        s = self.min_state()  # get node in OPEN set with min k value
        self.visited.add(s)

        if s is None:
            return -1  # OPEN set is empty

        k_old = self.get_k_min()  # record the min k value of this iteration (min path cost)
        self.delete(s)  # move state s from OPEN set to CLOSED set

        # k_min < h[s] --> s: RAISE state (increased cost)
        if k_old < self.h[s]:
            for s_n in self.get_neighbor(s):
                if self.h[s_n] <= k_old and \
                        self.h[s] > self.h[s_n] + self.cost(s_n, s):

                    # update h_value and choose parent
                    self.PARENT[s] = s_n
                    self.h[s] = self.h[s_n] + self.cost(s_n, s)

        # s: k_min >= h[s] -- > s: LOWER state (cost reductions)
        if k_old == self.h[s]:
            for s_n in self.get_neighbor(s):
                if self.t[s_n] == 'NEW' or \
                        (self.PARENT[s_n] == s and self.h[s_n] != self.h[s] + self.cost(s, s_n)) or \
                        (self.PARENT[s_n] != s and self.h[s_n] > self.h[s] + self.cost(s, s_n)):

                    # Condition:
                    # 1) t[s_n] == 'NEW': not visited
                    # 2) s_n's parent: cost reduction
                    # 3) s_n find a better parent
                    self.PARENT[s_n] = s
                    self.insert(s_n, self.h[s] + self.cost(s, s_n))
        else:
            for s_n in self.get_neighbor(s):
                if self.t[s_n] == 'NEW' or \
                        (self.PARENT[s_n] == s and self.h[s_n] != self.h[s] + self.cost(s, s_n)):

                    # Condition:
                    # 1) t[s_n] == 'NEW': not visited
                    # 2) s_n's parent: cost reduction
                    self.PARENT[s_n] = s
                    self.insert(s_n, self.h[s] + self.cost(s, s_n))
                else:
                    if self.PARENT[s_n] != s and \
                            self.h[s_n] > self.h[s] + self.cost(s, s_n):

                        # Condition: LOWER happened in OPEN set (s), s should be explored again
                        self.insert(s, self.h[s])
                    else:
                        if self.PARENT[s_n] != s and \
                                self.h[s] > self.h[s_n] + self.cost(s_n, s) and \
                                self.t[s_n] == 'CLOSED' and \
                                self.h[s_n] > k_old:

                            # Condition: LOWER happened in CLOSED set (s_n), s_n should be explored again
                            self.insert(s_n, self.h[s_n])

        return self.get_k_min()

    def min_state(self):
        """
        choose the node with the minimum k value in OPEN set.
        :return: state
        """

        if not self.OPEN:
            return None

        return min(self.OPEN, key=lambda x: self.k[x])

    def get_k_min(self):
        """
        calc the min k value for nodes in OPEN set.
        :return: k value
        """

        if not self.OPEN:
            return -1

        return min([self.k[x] for x in self.OPEN])

    def insert(self, s, h_new):
        """
        insert node into OPEN set.
        :param s: node
        :param h_new: new or better cost to come value
        """

        if self.t[s] == 'NEW':
            self.k[s] = h_new
        elif self.t[s] == 'OPEN':
            self.k[s] = min(self.k[s], h_new)
        elif self.t[s] == 'CLOSED':
            self.k[s] = min(self.h[s], h_new)

        self.h[s] = h_new
        self.t[s] = 'OPEN'
        self.OPEN.add(s)

    def delete(self, s):
        """
        delete: move state s from OPEN set to CLOSED set.
        :param s: state should be deleted
        """

        if self.t[s] == 'OPEN':
            self.t[s] = 'CLOSED'

        self.OPEN.remove(s)

    def modify(self, s):
        """
        start processing from state s.
        :param s: is a node whose status is RAISE or LOWER.
        """

        self.modify_cost(s)

        while True:
            k_min = self.process_state()

            if k_min >= self.h[s]:
                break

    def modify_cost(self, s):
        # if node in CLOSED set, put it into OPEN set.
        # Since cost may be changed between s - s.parent, calc cost(s, s.p) again

        if self.t[s] == 'CLOSED':
            self.insert(s, self.h[self.PARENT[s]] + self.cost(s, self.PARENT[s]))

    def get_neighbor(self, s):
        nei_list = set()

        for u in self.u_set:
            s_next = tuple([s[i] + u[i] for i in range(2)])
            if s_next not in self.obs:
                nei_list.add(s_next)

        return nei_list

    def cost(self, s_start, s_goal):
        """
        Calculate Cost for this motion
        :param s_start: starting node
        :param s_goal: end node
        :return:  Cost for this motion
        :note: Cost function could be more complicate!
        """

        if self.is_collision(s_start, s_goal):
            return float("inf")

        return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])

    def is_collision(self, s_start, s_end):
        if s_start in self.obs or s_end in self.obs:
            return True

        if s_start[0] != s_end[0] and s_start[1] != s_end[1]:
            if s_end[0] - s_start[0] == s_start[1] - s_end[1]:
                s1 = (min(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
            else:
                s1 = (min(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), min(s_start[1], s_end[1]))

            if s1 in self.obs or s2 in self.obs:
                return True

        return False

    def plot_visited(self, visited):
        color = ['gainsboro', 'lightgray', 'silver', 'darkgray',
                 'bisque', 'navajowhite', 'moccasin', 'wheat',
                 'powderblue', 'skyblue', 'lightskyblue', 'cornflowerblue']

        if self.count >= len(color) - 1:
            self.count = 0

        for x in visited:
            plt.plot(x[0], x[1], marker='s', color=color[self.count])

def main():
    s_start = (15, 5)
    s_goal = (250, 250)
    dstar = DStar(s_start, s_goal)
    dstar.run(s_start, s_goal)

    # Simplify the path
    simplified_path = dstar.path_simplification(dstar.path)
    # Print the simplified path
    print("Simplified path from start to goal:")
    for node in simplified_path[1:-1]:
        print(f"Node: x={node[0]}, y={node[1]}")

if __name__ == '__main__':
    main()

