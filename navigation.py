# Navigation module for ThatsJustTheWazeItIs
from collections import defaultdict
import json
import threading

class Navigation:
    """docstring for ."""

    def __init__(self, filename):
        self.graph = Graph(filename)
        self.__roomEmpty = threading.Lock()
        self.__turnstile = threading.Lock()

    def requestMapUpdate(body):
        self.__turnstile.acquire()
        self.__turnstile.release()

        with self.__roomEmpty:
            path, wait, total_wait = self.dijkstra(body["curr"], body["dest"])

        if len(path) == 1:
            road = ""
        else:
            road = graph.edges[path[0]][path[1]].road_name

            self.__turnstile.acquire()
            self.__roomEmpty.acquire()
            self.updateMap(body["prev"], path[0], path[1])
            self.__turnstile.release():
            self.__roomEmpty.release()

        return json.dumps({"next": path[1], "road": road, "wait" : wait, "total_wait" = total_wait})

    def dijkstra(curr, dest):
        visited = {curr: 0}
        path = {curr: [curr]}

        nodes = self.graph.nodes

        while nodes:
            min_node = None
            for node in nodes:
              if node in visited:
                if min_node is None:
                  min_node = node
                elif visited[node] < visited[min_node]:
                  min_node = node

            if min_node is None:
              break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for to_node in self.graph.edges[min_node]:
                weight = current_weight + self.graph.getWeight(min_node, to_node)
                if to_node not in visited or weight < visited[to_node]:
                    visited[to_node] = weight
                    path[to_node] = path[min_node] + [to_node]

        return path[dest][1], visited[path[dest][1]], visited[dest]


    def updateMap(prev, curr, next):
        if prev:
            self.graph[prev][curr].num_cars -= 1
        self.graph[curr][next].num_cars += 1
