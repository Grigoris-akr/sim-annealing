import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt


def plot(edges, coords, filename = "fig"):
    """ plot graph from edge dict """
    pos = np.array(list(coords.values()))

    colors = ['blue', 'orange', 'red', 'gray', 'green', 'yellow', 'black', 'purple']
    plt.figure()
    G = nx.DiGraph()
    for route in list(edges.keys()):
        for i, j in edges[route].items():
            G.add_edge(i, j, color=colors[route % len(colors)])

    edge_colors = nx.get_edge_attributes(G,'color').values()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, node_size=100, font_size=6)

    plt.savefig(f"{filename}.png")
    plt.close()
    return None


def read_data(file):
    raw_data = []
    with open(file, 'r') as f:
        for line in f:
            raw_data.append(line.split())
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

def ls_random_select(reloc_perc, exch_perc, opt_perc):
    """ Returns a local search method based on the percantages provided"""
    rand = random.random()
    if rand > (1 - reloc_perc):
        ls_method = 'relocation'
    elif rand > (1 - reloc_perc - opt_perc):
        ls_method = '2opt'
    else:
        ls_method = 'exchange'
    return ls_method

class temperature:
    """ Temperature helper class for Simulated Annealing """

    def __init__(self, update_method, init_T, final_T, alpha):
        self.now = init_T
        self.init_T = init_T
        self.final_T = final_T
        self.alpha = alpha
        self.iter = 0

        if update_method == 'linear':
            self.update = self.update_linear
        elif update_method == 'exponential':
            self.update = self.update_exp
        else:
            raise Exception()

    def update_exp(self,):
        self.now = self.init_T * np.exp(-self.iter * self.alpha)
        self.iter += 1

    def update_linear(self,):
        self.now = self.init_T - (self.iter * self.alpha)
        self.iter += 1

