import math
import level as lvl

# copy pasted https://stackabuse.com/basic-ai-concepts-a-search-algorithm/


def distance(cell_1, cell_2):
    return math.sqrt((cell_1.x - cell_2.x) ** 2 + (cell_1.y - cell_2.y) ** 2)


def a_star(start: lvl.Cell, destination: lvl.Cell):
    open_list = {start}
    closed_list = set([])
    g = {start: 0}

    parents = {start: start}
    bigcloud = []

    while len(open_list) > 0:
        best = None

        for v in open_list:
            if best is None or g[v] + distance(v, destination) < g[best] + distance(best, destination):
                best = v

        if best is None:
            print("no path")
            return None

        if best == destination:
            path = []

            while parents[best] != best:
                path.append(best)
                best = parents[best]

            path.append(start)
            path.reverse()

            print("path is: {}".format(path))
            return path, bigcloud

        bigcloud.append(best)
        for m in best.neighbors:
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = best
                g[m] = g[best] + best.neighbors[m]
            else:
                if g[m] > g[best] + best.neighbors[m]:
                    g[m] = g[best] + best.neighbors[m]
                    parents[m] = best

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)
        open_list.remove(best)
        closed_list.add(best)

    print("no path")
    return None
