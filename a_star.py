import math
import level as lvl


def distance(cell_1, cell_2):
    return math.sqrt((cell_1.x - cell_2.x) ** 2 + (cell_1.y - cell_2.y) ** 2)


def a_star(start: lvl.Cell, destination: lvl.Cell):

    def h(cell):
        return distance(cell, destination)

    open_set = {start}
    came_from = {start: start}
    g_score = {start: 0}
    f_score = {start: h(start)}

    bigcloud = []

    while len(open_set) > 0:
        current = None

        for v in open_set:
            if current is None or f_score[v] < f_score[current]:
                current = v

        if current is None:
            print("no path")
            return None, bigcloud

        if current == destination:
            path = []

            while came_from[current] != current:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            print("path is: {}".format(path))
            return path, bigcloud

        open_set.remove(current)
        bigcloud.append(current)
        for neighbor in current.neighbors:
            tentative_gscore = g_score[current] + distance(current, neighbor)
            if neighbor not in g_score:
                g_score[neighbor] = 100000000000
            if tentative_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + h(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    print("no path")
    return None, bigcloud
