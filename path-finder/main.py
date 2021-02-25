import argparse
import json
import math
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

FILE_LOCATION = 'path-finder/inputs/input.json'

parser = argparse.ArgumentParser(description='Finds the number of shortest paths between two vertices of an '
                                             'undirected, unweighted graph')
parser.add_argument('-f', action='store', dest='graph_location', help='Relative path to input file',
                    default=FILE_LOCATION)
parser.add_argument('--plot', dest='plot', action='store_true', default=False)


def num_shortest_paths(graph, path_start, path_end):
    num_vertices = len(graph[0])
    paths = [0] * num_vertices
    dists = [math.inf] * num_vertices
    visited_vertices = [False] * num_vertices

    q = deque()
    q.append(path_start)
    dists[path_start] = 0
    paths[path_start] = 1
    visited_vertices[path_start] = True

    while q:
        v = q.popleft()
        # finds indexes of values equal to "1", denoting edges in the adjacency matrix
        nhbrs = [i for i, x in enumerate(graph[v]) if x == 1]
        for nhbr in nhbrs:
            if not visited_vertices[nhbr]:
                q.append(nhbr)
                visited_vertices[nhbr] = True
            if dists[nhbr] > dists[v] + 1:
                # previous nhbrs are not minimal
                dists[nhbr] = dists[v] + 1
                paths[nhbr] = paths[v]
            elif dists[nhbr] == dists[v] + 1:
                # nhbr is minimal wrt to other nhbrs
                paths[nhbr] += paths[v]

    return paths[path_end]


# displays the graph, labelled with respect to index
def print_network(graph, file_path):
    arr = np.array(graph)
    network = nx.convert_matrix.from_numpy_matrix(arr)

    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_title('Graph Generated From: {}'.format(file_path))
    nx.draw(network, with_labels=True, ax=ax)
    _ = ax.axis('off')
    plt.show()


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.graph_location) as f:
        data = json.load(f)
        start = data['path'][0]
        end = data['path'][1]
        adjacency_matrix = data['adjacency_matrix']

        num_paths = num_shortest_paths(adjacency_matrix, start, end)
        print('Number of shortest paths between {} and {}: {}'.format(start, end, num_paths))

    if args.plot:
        print_network(graph=adjacency_matrix, file_path=args.graph_location)
