import heapq
import main

# copy pasted https://stackabuse.com/basic-ai-concepts-a-search-algorithm/


def a_star(start: main.Cell, destination: main.Cell):
    open_list = {start}
    closed_list = set([])
    g = {start: 0}

    parents = {start: start}

    while len(open_list) > 0:
        best = None

        for v in open_list:
            if best is None or g[v] + main.distance(start, v) < g[best] + main.distance(start, best):
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
            return path

        for m in best.neighbors:
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = best
                g[m] = g[best] + 1
            else:
                if g[m] > g[best] + 1:
                    g[m] = g[best] + 1
                    parents[m] = best

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)
        open_list.remove(best)
        closed_list.add(best)

    print("no path")
    return None
