import numpy as np

class AbstractRoutes:
    def __init__(self, distance_matrix, node_dem_l):
        self.N = np.size(distance_matrix, axis=0)
        self.dist_mat = np.array(distance_matrix)
        self.dist_mat[np.diag_indices_from(distance_matrix)] = 0 # set diag to zero
        self.node_dem_l = node_dem_l

        # initiate route attributes
        self.edges     = {0: {}} # key node -> value node
        self.edges_inc = {0: {}} # key node <- value node
        self.cost = np.zeros(1)  # cost per route

        self.best = {}
        self.best_inc = {}
        self.best_cost = []     # best cost per route

        self.load = np.zeros(1) # load per route
        self.node_route = np.zeros(self.N, dtype = int) # route id for each node

    def __len__(self,):
        return len(self.edges)

    def new_route(self,):
        self.load = np.append(self.load, np.zeros(1))
        self.cost = np.append(self.cost, np.zeros(1))
        self.best_cost = np.append(self.best_cost, np.zeros(1))

        self.edges[len(self.edges)] = {}
        self.edges_inc[len(self.edges_inc)] = {}
        return None

    def get_best_cost(self, route_idx = None):
        if route_idx is None:
            return np.sum(self.best_cost)
        else:
            return self.best_cost[route_idx]

    # def get_cost(self, route_idx = None):
    #     if route_idx is None:
    #         return np.sum(self.cost)
    #     else:
    #         return self.cost[route_idx]

    #def calc_cost(self, route_idx = None):
    def get_cost(self, route_idx = None):
        # Calculate cost of a route. If None for all routes
        if route_idx is None:
            x = []
            y = []
            for r in list(self.edges.keys()):
                for i, j in self.edges[r].items():
                    x.append(i)
                    y.append(j)

            return self.dist_mat[x,y].sum()
        else:
            s = 0
            for i, j in self.edges[route_idx].items():
                s += self.dist_mat[i,j]
            return s

    def get_delta_from_best(self, route_idx = None):
        return self.get_cost(route_idx) - self.get_best_cost(route_idx)

    def reset_to_best(self,):
        self.edges = self.best.copy()
        self.edges_inc = self.best_inc.copy()

        # reset cost
        self.cost = self.best_cost.copy()
        
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
        #self.best_cost = [self.calc_cost(route_idx = route) for route in self.edges.keys()]
        #self.best_cost = self.cost.copy()
        return None

    def rollback(self,):
        pass

    def add_node(self, route, node, preceding_node):
        # p ==> p -> node

        self.edges[route][preceding_node] = node
        self.edges_inc[route][node] = preceding_node

        # adjust load
        self.load[route] += self.node_dem_l[node]

        # adjust node_route
        self.node_route[node] = route

        return None

    def insert_node(self, route, node, preceding_node):
        # p --> a ==> p -> node -> a
        
        #p = preceding_node
        a = self.edges[route][preceding_node]

        self.edges[route][preceding_node] = node
        self.edges_inc[route][node] = preceding_node
        self.edges[route][node] = a
        self.edges_inc[route][a] = node

        # adjust load
        self.load[route] += self.node_dem_l[node]

        # adjust node_route
        self.node_route[node] = route

        # # adjust cost
        # self.cost[route] -= self.dist_mat[preceding_node, a]
        # self.cost[route] += self.dist_mat[preceding_node, node]
        # self.cost[route] += self.dist_mat[node, a]

        return None

    def remove_node(self, route, node):
        # p -> node -> a ==> p --> a

        p = self.edges_inc[route][node]
        a = self.edges[route][node]
        
        # remove node
        self.edges[route].pop(node)
        self.edges_inc[route].pop(node)

        # reconnect route
        self.edges[route][p] = a
        self.edges_inc[route][a] = p

        # adjust load
        self.load[route] -= self.node_dem_l[node]

        # # adjust cost
        # self.cost[route] -= self.dist_mat[p, node]
        # self.cost[route] -= self.dist_mat[node, a]
        # self.cost[route] += self.dist_mat[p, a]

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
            self.insert_node(route = route2, node = node1, preceding_node = node2)

        elif method == 'exchange':
            preceding_1 = self.edges_inc[route1][node1]
            preceding_2 = self.edges_inc[route2][node2]

            self.remove_node(route1, node1)
            self.remove_node(route2, node2)
            self.insert_node(route2, node1, preceding_node = preceding_2)
            self.insert_node(route1, node2, preceding_node = preceding_1)

        return None
