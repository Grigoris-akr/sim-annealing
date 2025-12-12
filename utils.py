#!/home/golis/.venvs/venv1/bin/python3
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def save_plot_from_adj_mat(adj_mat, coords, filename = "fig"):
    adj_mat = np.array(adj_mat)
    pos = np.array(list(coords.values()))

    colors = ['blue', 'red', 'gray', 'green', 'yellow', 'orange']

    for i in range(np.size(adj_mat, axis=0)): 
        G = nx.from_numpy_array(adj_mat[i,:,:], create_using=nx.DiGraph)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=colors[i % len(colors)])

    plt.savefig(f"{filename}.png")
    G.clear()
    return None

def save_plot_from_edges(edges, coords, filename = "fig"):
    """ from edge dict """
    pos = np.array(list(coords.values()))

    colors = ['blue', 'red', 'gray', 'green', 'yellow', 'orange']
    plt.figure()
    G = nx.DiGraph()
    for route in list(edges.keys()):
        for i, j in edges[route].items():
            G.add_edge(i, j, color=colors[route % len(colors)])

    edge_colors = nx.get_edge_attributes(G,'color').values()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors)

    plt.savefig(f"{filename}.png")
    G.clear()
    plt.close()
    return None


def read_data(filename):
    raw_data = []
    with open(filename, 'r') as f:
        for line in f:
            raw_data.append(line.split())#.split(' '))
    data = {}

    data["N"]           = int(raw_data[0][0])
    data["veh_cap"]     = int(raw_data[1][0])
    data["time_limit"]  = int(raw_data[2][0])
    data["serv_time"]   = int(raw_data[3][0])
    data["node_coords"] = {}
    for (idx, x, y) in raw_data[4:4+data["N"]]:
        data["node_coords"][idx] = [int(x), int(y)]
    data["node_dem"]    = [int(cap) for (idx, cap) in raw_data[4+data["N"]:]]

    return data


def get_distance_matrix(coords):
    coords_arr = np.array(list(coords.values()))
    dist = lambda p1, p2: np.sqrt(((p1-p2)**2).sum())

    dm = np.asarray([[dist(p1, p2) for p2 in coords_arr] for p1 in coords_arr])
    dm[np.diag_indices_from(dm)] = np.inf
    return dm



if __name__ == '__main__':
    data = read_data('prov6.txt')
    print(data)
