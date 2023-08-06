import time
import typing

import networkx
import numpy as np


def get_graph(bin_region: np.ndarray) -> networkx.Graph:
    start = time.time()
    yy, xx = np.nonzero(bin_region)

    G = networkx.Graph()
    start2 = time.time()
    for py, px in zip(yy, xx):
        G.add_node((px, py))
    start3 = time.time()
    for py, px in zip(yy, xx):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if (px + j, py + i) not in G:
                    continue
                if abs(i) + abs(j) == 2:
                    G.add_edge((px, py), (px + j, py + i), weight=1.41)
                else:
                    G.add_edge((px, py), (px + j, py + i), weight=1)
    return G


GeodesicPathPixels = np.ndarray

def get_node_with_longest_shortest_path(shortest_lengths: typing.Dict[typing.Tuple[int, int], float]) -> typing.Tuple[int, int]:
    return max(shortest_lengths.items(), key=lambda t: t[1])[0]


def compute_longest_geodesic_perf(region: np.ndarray) -> float:
    G = get_graph(region)

    yy, xx = np.nonzero(region)

    if len(yy) == 0:
        return -1.0

    min_idx = np.argmin(xx)
    out_pixel = (yy[min_idx], xx[min_idx])
    out_pixel = (xx[min_idx], yy[min_idx])

    shortest_lengths = networkx.shortest_path_length(G, source=out_pixel, weight='weight')
    dst_pix = get_node_with_longest_shortest_path(shortest_lengths)

    shortest_lengths2 = networkx.shortest_path_length(G, source=dst_pix, weight='weight')
    dst_pix2 = get_node_with_longest_shortest_path(shortest_lengths2)

    shortest_lengths3 = networkx.shortest_path_length(G, source=dst_pix2, weight='weight')
    dst_pix3 = get_node_with_longest_shortest_path(shortest_lengths3)

    return shortest_lengths3[dst_pix3]
