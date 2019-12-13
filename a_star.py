import math
import level as lvl
import heapq


def distance(cell_1, cell_2):
    return math.sqrt((cell_1.x - cell_2.x) ** 2 + (cell_1.y - cell_2.y) ** 2)


def a_star(start: lvl.Cell, destination: lvl.Cell):

    def h(cell):
        return distance(cell, destination)

    open_set = [start]
    came_from = {start: start}
    start.set_g(0)
    start.set_f(h(start))

    bigcloud = []

    while len(open_set) > 0:
        current = heapq.heappop(open_set)
        bigcloud.append(current)

        if current == destination:
            path = []

            while came_from[current] != current:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            print("path is: {}".format(path))
            return path, bigcloud

        for neighbor in current.neighbors:
            tentative_gscore = current.get_g() + distance(current, neighbor)
            if tentative_gscore < neighbor.get_g():
                came_from[neighbor] = current
                neighbor.set_g(tentative_gscore)
                neighbor.set_f(neighbor.get_g() + h(neighbor))
                heapq.heapify(open_set)
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

    print("no path")
    return None, bigcloud
