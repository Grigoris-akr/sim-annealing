import numpy as np

class AbstractRoutes:
    def __init__(self, distance_matrix):
        self.N = np.size(distance_matrix, axis=0)
        self.dist_mat_zero_diag = np.array(distance_matrix)
        self.dist_mat_zero_diag[np.diag_indices_from(distance_matrix)] = 0 # set diag to zero

        # initiate route objects
        self.am   = np.zeros([1, self.N, self.N])   # adjacency matrix form

        self.edges     = {0: {}} # key -> value
        self.edges_inc = {0: {}} # key <- value

        self.best_am = self.am.copy()
        #self.best_edges  = 

        self.best_cost = np.zeros(1) # best cost per route
        self.load = np.zeros(1)      # load per route

        # TODO: maybe keep track of edge costs

    def __len__(self,):
        return len(self.edges)

    def new_route(self,):
        self.am = np.append(self.am, np.zeros([1, self.N, self.N]), axis=0)
        self.best_cost = np.append(self.best_cost, np.zeros(1))
        self.load = np.append(self.load, np.zeros(1))

        self.edges[len(self.edges)] = {}
        self.edges_inc[len(self.edges_inc)] = {}

    def get_best_cost(self, route_idx = None):
        if route_idx is None:
            return self.best_cost.sum()
        else:
            return self.best_cost[route_idx]

    def get_cost(self, route_idx = None):
        # TODO - fix this shit
        # if None get cost of all routes
        #return (self.dist_mat_zero_diag * self.am[route_idx]).sum()
        #return self.am[route_idx].sum()
        x = []
        y = []
        if route_idx is None:
            #indices = [[i][j] for r in list(self.edges.keys()) for i, j in self.edges[r].items()]
            for r in list(self.edges.keys()):
                for i, j in self.edges[r].items():
                    x.append(i)
                    y.append(j)

            return self.dist_mat_zero_diag[x,y].sum()
        else:
            indices = [[i,j] for i, j in self.edges[route_idx].items()]
            return self.dist_mat_zero_diag[indices].sum()


    def get_delta_from_best(self, route_idx = None):
        return self.am[route_idx].sum() - self.get_best_cost(route_idx)

    def reset_to_best(self,):
        self.am = self.best_am.copy()
        self.list = self.best_l.copy()

    def update_best(self,):
        #self.update_list_view()
        self.best_am = self.am.copy()
        #self.best_l  = self.list.copy()
        self.best_cost = np.einsum('kij -> k', self.am)
        # self.best_cost = np.einsum('ij, kij -> k', self.dist_map..., self.am)


    def commit(self,):
        # commit the perturabation
        pass

    def revert(self,):
        # revert the perturbation
        pass
    
    def add_node(self, route, node, preceding_node):
        # preceding_node --> x || preceding_node -> node -> z
        node_z = self.edges[route][preceding_node]

        self.edges[route][preceding_node] = node
        self.edges_inc[route][node] = preceding_node
        self.edges[route][node] = node_z
        self.edges_inc[route][node_z] = node
        return None

    def remove_node(self, route, node):
        # x -> i -> y || x --> y

        x = self.edges_inc[route][node]
        y = self.edges[route][node]
        
        # remove node
        self.edges[route].pop(node)
        self.edges_inc[route].pop(node)

        # reconnect route
        self.edges[route][x] = y
        self.edges_inc[route][y] = x
        return None

    def exchange_nodes(self, route1, node1, route2, node2):
        preceding_1 = self.edges_inc[route1][node1]
        preceding_2 = self.edges_inc[route2][node2]

        self.remove_node(route1, node1)
        self.remove_node(route2, node2)
        self.add_node(route2, node1, preceding_node = preceding_2)
        self.add_node(route1, node2, preceding_node = preceding_1)
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
