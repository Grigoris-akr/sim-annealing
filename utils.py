#!/home/golis/.venvs/venv1/bin/python3
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def save_plot(adj_mat, coords, filename = "fig"):
    adj_mat = np.array(adj_mat)
    pos = np.array(list(coords.values()))

    colors = ['blue', 'red', 'gray', 'green', 'yellow', 'orange']

    for i in range(np.size(adj_mat, axis=0)): 
        # For a directed graph (treat A as adjacency from i->j):
        G = nx.from_numpy_array(adj_mat[i,:,:], create_using=nx.DiGraph)

        # If A contains weights, they become edge attribute 'weight'.
        # Quick draw
        #pos = nx.spring_layout(G)    # layout; alternatives: circular_layout, kamada_kawai
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=colors[i % len(colors)])

    plt.savefig(f"{filename}.png")


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
    #data["node_coords"] = [[int(x), int(y)] for (idx, x, y) in raw_data[4:4+data["N"]]]
    data["node_dem"]    = [int(cap) for (idx, cap) in raw_data[4+data["N"]:]]

    return data


def get_distance_matrix(coords):
    coords_arr = np.array(list(coords.values()))
    dist = lambda p1, p2: np.sqrt(((p1-p2)**2).sum())

    dm = np.asarray([[dist(p1, p2) for p2 in coords_arr] for p1 in coords_arr])
    dm[np.diag_indices_from(dm)] = np.inf
    return dm


class AbstractRoutes:
    def __init__(self, distance_matrix):
        self.N = np.size(distance_matrix, axis=0)
        self.dist_mat_zero_diag = np.array(distance_matrix)
        self.dist_mat_zero_diag[np.diag_indices_from(distance_matrix)] = 0 # set diag to zero

        # initiate route objects
        self.am   = np.zeros([1, self.N, self.N])   # adjacency matrix form
        self.list = list()                          # list form
        self.best_am = self.am.copy()               
        self.best_l  = self.list.copy()

        self.best_cost = np.zeros(1) # best cost per route
        self.load = np.zeros(1)      # load per route

    #def __call__(self,):
    #    return self.routesx

    def __len__(self,):
        return self.am.shape[0]

    def new_route(self,):
        self.am = np.append(self.am, np.zeros([1, self.N, self.N]), axis=0)
        self.best_cost = np.append(self.best_cost, np.zeros(1))
        self.load = np.append(self.load, np.zeros(1))

    def get_best_cost(self, route_idx = None):
        if route_idx is None:
            return self.best_cost.sum()
        else:
            return self.best_cost[route_idx]

    def get_cost(self, route_idx = None):
        # if None get cost of all routes
        return (self.dist_mat_zero_diag * self.am[route_idx]).sum()

    def update_list_view(self,):
        pass

    def get_delta(self, route_idx = None):
        return self.get_cost(self.am[route_idx]) - self.best_cost(route_idx)

    def reset_to_best(self,):
        self.am = self.best_am.copy()
        self.list = self.best_l.copy()

    def update_best(self,):
        self.update_list_view()
        self.best_am = self.am.copy()
        self.best_l  = self.list.copy()
        self.best_cost = np.einsum('ij, kij -> k', self.dist_mat_zero_diag, self.am)

if __name__ == '__main__':
    data = read_data('prov6.txt')
    print(data)
