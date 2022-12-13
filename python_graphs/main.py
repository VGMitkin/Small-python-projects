class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links

class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value

class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if all({i.v1, i.v2} != {link.v1, link.v2} for i in self._links):
            self._links.append(link)
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)
            link.v1.links.append(link)
            link.v2.links.append(link)

    def find_path(self, start_v, stop_v):
        plan_to_visit = []
        d = {}
        n = float('inf')
        for i in self._vertex:
            d[i] = 0 if i == stop_v else n, None, None  # dist, vertex, link
            plan_to_visit.append(i)

        while plan_to_visit:
            min_vertex = None
            for i in plan_to_visit:
                if min_vertex is None or d[i][0] < d[min_vertex][0]:
                    min_vertex = i
            plan_to_visit.remove(min_vertex)

            for link in min_vertex.links:
                next_vertex = link.v1 if link.v1 != min_vertex else link.v2
                if next_vertex not in plan_to_visit:
                    continue
                dist = d[min_vertex][0] + link.dist
                if dist < d[next_vertex][0]:
                    d[next_vertex] = dist, link, min_vertex

        vertexs = [start_v]
        links = []
        last = d[start_v]
        while last[0]:
            links.append(last[1])
            vertexs.append(last[2])
            last = d[last[2]]

        return vertexs, links

class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self.dist = dist


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7