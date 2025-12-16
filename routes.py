import numpy as np

class AbstractRoutes:
    def __init__(self, distance_matrix, node_dem_l):
        self.N = np.size(distance_matrix, axis=0)
        self.dist_mat = np.array(distance_matrix)
        self.dist_mat[np.diag_indices_from(distance_matrix)] = 0 # set diag to zero
        self.node_dem_l = node_dem_l

        # initiate route objects
        self.edges     = {0: {}} # key node -> value node
        self.edges_inc = {0: {}} # key node <- value node

        self.best = {}
        self.best_inc = {}

        self.best_cost = []     # best cost per route
        self.load = np.zeros(1) # load per route

        self.node_route = np.zeros(self.N, dtype = int)

        # TODO: maybe keep track of edge costs

    def __len__(self,):
        return len(self.edges)

    def new_route(self,):
        self.best_cost = np.append(self.best_cost, np.zeros(1))
        self.load = np.append(self.load, np.zeros(1))

        self.edges[len(self.edges)] = {}
        self.edges_inc[len(self.edges_inc)] = {}
        return None

    def get_best_cost(self, route_idx = None):
        if route_idx is None:
            return sum(self.best_cost)
        else:
            return self.best_cost[route_idx]

    def get_cost(self, route_idx = None):
        # TODO - fix this shit
        # if None get cost of all routes
        x = []
        y = []
        if route_idx is None:
            #indices = [[i][j] for r in list(self.edges.keys()) for i, j in self.edges[r].items()]
            for r in list(self.edges.keys()):
                for i, j in self.edges[r].items():
                    x.append(i)
                    y.append(j)

            return self.dist_mat[x,y].sum()
        else:
            # indices = [[i,j] for i, j in self.edges[route_idx].items()]
            # return self.dist_mat[indices].sum()
            s = 0
            for i, j in self.edges[route_idx].items():
                s += self.dist_mat[i,j]
            return s

    def get_delta_from_best(self, route_idx = None):
        return self.get_cost(route_idx) - self.get_best_cost(route_idx)

    def reset_to_best(self,):
        self.edges = self.best.copy()
        self.edges_inc = self.best_inc.copy()
        
        # reset load and node routes
        for r in (self.best.keys()):
            self.load[r] = 0
            for n in list(self.best[r].keys()):
                self.load[r] += self.node_dem_l[n]
                self.node_route[n] = r

        return None

    def update_best(self,):
        self.best = self.edges.copy()
        self.best_inc = self.edges_inc.copy()
        self.best_cost = [self.get_cost(route_idx = route) for route in self.edges.keys()]
        return None

    def rollback(self,):
        pass

    def add_node(self, route, node, preceding_node):
        # preceding_node --> x ==> preceding_node -> node -> z
        node_z = self.edges[route][preceding_node]

        self.edges[route][preceding_node] = node
        self.edges_inc[route][node] = preceding_node
        self.edges[route][node] = node_z
        self.edges_inc[route][node_z] = node

        # adjust load
        self.load[route] += self.node_dem_l[node]

        # adjust node_route
        self.node_route[node] = int(route)

        return None

    def remove_node(self, route, node):
        # x -> node -> y ==> x --> y

        x = self.edges_inc[route][node]
        y = self.edges[route][node]
        
        # remove node
        self.edges[route].pop(node)
        self.edges_inc[route].pop(node)

        # reconnect route
        self.edges[route][x] = y
        self.edges_inc[route][y] = x

        # adjust load
        self.load[route] -= self.node_dem_l[node]
        return None

    def untangle(self, route, node1, node2):
        # 2-opt
        # --p1  n2--   --p1--n2--
        #     \/   | =>         |
        #     /\   | =>         |
        # --a2  n1--   --p2--n1--

        # This is wrong, it breaks the chain.
        # Considering changing between edges and edges_inc
        p1 = self.edges_inc[route][node1]
        a2 = self.edges[route][node2]

        self.edges[route][p1] = node2
        self.edges[route][p2] = node1
       
        self.edges_inc[route][node1] = p2
        self.edges_inc[route][node2] = p1
        return None

    def commit(self, route1, node1, route2, node2, method = None):
        if method == 'reloc':
            self.remove_node(route = route1, node = node1)
            self.add_node(route = route2, node = node1, preceding_node = node2)

        elif method == 'exchange':
            preceding_1 = self.edges_inc[route1][node1]
            preceding_2 = self.edges_inc[route2][node2]

            self.remove_node(route1, node1)
            self.remove_node(route2, node2)
            self.add_node(route2, node1, preceding_node = preceding_2)
            self.add_node(route1, node2, preceding_node = preceding_1)

        return None
