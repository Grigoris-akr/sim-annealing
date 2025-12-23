import numpy as np
import copy

class AbstractRoutes:
    """
    Routes class implementing basic route functions

        self.edges holds info on which node follows the key node (key -> value)
        self.edges_inv holds info on which node precedes the key (key <- value)
        self.node_route holds on which route each node belongs to

            Example
            -------
            route 0: 0 -> 1 -> 4 -> 6 -> 3 -> 0
            route 1: 0 -> 2 -> 5 -> 0

            edges = {0: {0:1, 1:4, 4:6, 6:3, 3:0},
                     1: {0:2, 2:5, 5:0}}

            edges_inv = {0: {0:3, 1:0, 3:6, 4:1, 6:4},
                         1: {0:5, 2:0, 5:2}}

                          0  1  2  3  4  5  6
            node_route = [-, 0, 1, 0, 0, 1, 0]
    """
  
    def __init__(self, distance_matrix, node_dem_l):
        self.N = np.size(distance_matrix, axis=0)
        self.node_dem_l = node_dem_l
        self.dist_mat = np.array(distance_matrix)
        self.dist_mat[np.diag_indices_from(distance_matrix)] = 0 # set diag to zero

        # initiate route attributes
        self.edges     = {0: {}} # key node -> value node
        self.edges_inv = {0: {}} # key node <- value node
        self.cost = np.zeros(1)  # cost per route

        self.best = {}      # edges with best cost
        self.best_inv = {}
        self.best_cost = np.zeros(1) # best cost per route

        self.load = np.zeros(1) # load per route
        self.node_route = np.zeros(self.N, dtype = int) # route id for each node

    def __len__(self,):
        return len(self.edges)

    def new_route(self,):
        self.load = np.append(self.load, np.zeros(1))
        self.cost = np.append(self.cost, np.zeros(1))
        self.best_cost = np.append(self.best_cost, np.zeros(1))

        self.edges[len(self.edges)] = {}
        self.edges_inv[len(self.edges_inv)] = {}
        return None

    def get_best_cost(self, route_idx = None):
        if route_idx is None:
            return np.sum(self.best_cost)
        else:
            return self.best_cost[route_idx]

    def get_cost(self, route_idx = None):
        if route_idx is None:
            return np.sum(self.cost)
        else:
            return self.cost[route_idx]

    def calc_cost(self, route_idx = None):
        # Calculate cost of a route. For all routes if None 
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

    def rollback(self,):
        "reset routes to best"
        self.edges = copy.deepcopy(self.best)
        self.edges_inv = copy.deepcopy(self.best_inv)

        # reset cost
        self.cost = copy.deepcopy(self.best_cost)
        
        # reset load and node routes
        for r in (self.best.keys()):
            self.load[r] = 0
            for n in list(self.best[r].keys()):
                self.load[r] += self.node_dem_l[n]
                self.node_route[n] = r

        return None

    def update_best(self,):
        self.best = copy.deepcopy(self.edges)
        self.best_inv = copy.deepcopy(self.edges_inv)
        self.best_cost = copy.deepcopy(self.cost)
        #self.best_cost = [self.calc_cost(route_idx = route) for route in self.edges.keys()]
        return None

    def add_node(self, route, node, preceding_node):
        # p ==> p -> node

        self.edges[route][preceding_node] = node
        self.edges_inv[route][node] = preceding_node

        # adjust load
        self.load[route] += self.node_dem_l[node]

        # adjust node_route
        self.node_route[node] = route

        # adjust cost
        self.cost[route] += self.dist_mat[preceding_node, node]

        return None

    def _insert_node(self, route, node, preceding_node):
        # p --> a ==> p -> node -> a
        
        #p = preceding_node
        a = self.edges[route][preceding_node]
        
        # edges
        self.edges[route][preceding_node] = node
        self.edges_inv[route][node] = preceding_node
        self.edges[route][node] = a
        self.edges_inv[route][a] = node

        # adjust load
        self.load[route] += self.node_dem_l[node]

        # adjust node_route
        self.node_route[node] = route

        # adjust cost
        self.cost[route] -= self.dist_mat[preceding_node, a]
        self.cost[route] += self.dist_mat[preceding_node, node]
        self.cost[route] += self.dist_mat[node, a]

        return None

    def _remove_node(self, route, node):
        # p -> node -> a ==> p --> a

        p = self.edges_inv[route][node]
        a = self.edges[route][node]
        
        # remove node
        self.edges[route].pop(node)
        self.edges_inv[route].pop(node)

        # reconnect route
        self.edges[route][p] = a
        self.edges_inv[route][a] = p

        # adjust load
        self.load[route] -= self.node_dem_l[node]

        # adjust cost
        self.cost[route] -= self.dist_mat[p, node]
        self.cost[route] -= self.dist_mat[node, a]
        self.cost[route] += self.dist_mat[p, a]

        return None

    def _opt2(self, route, node1, node2):
        # -->p1-->.  .<-n2--<--p2<---    -->p1-------->n2---->p2-->-
        #          \/               ^ =>                           |
        #          /\               | =>                           V
        # <--a2<--'  `--->n1-->a1---^    <--a2<----------n1<--a1<---
        
        # hack to get it work
        if self.edges[route][node2] == node1:
            tmp = node1
            node1 = node2
            node2 = tmp
        
        # preceding and succeeding nodes
        p1 = self.edges_inv[route][node1]
        a2 = self.edges[route][node2]

        # p1 -> n2
        self.edges[route][p1] = node2
        self.edges[route][node2] = self.edges_inv[route][node2]
        self.edges_inv[route][node2] = p1
        
        # n1 -> a2
        self.edges_inv[route][node1] = self.edges[route][node1]
        self.edges[route][node1] = a2
        self.edges_inv[route][a2] = node1
        
        # reverse order from node2 to node1
        p = node2
        n = self.edges[route][node2]
        while n != node1:
            # reverse edge order
            self.edges[route][n] = self.edges_inv[route][n]
            self.edges_inv[route][n] = p 
            
            # next node pair
            p = n
            n = self.edges[route][p]

        # adjust cost
        self.cost[route] -= self.dist_mat[p1, node1]
        self.cost[route] -= self.dist_mat[node2, a2]
        self.cost[route] += self.dist_mat[p1, node2]
        self.cost[route] += self.dist_mat[node1, a2]
            
        return None

    def commit(self, route1, node1, route2, node2, method = None):
        # commit the local search described by these arguments

        if method == 'relocation':
            self._remove_node(route = route1, node = node1)
            self._insert_node(route = route2, node = node1, preceding_node = node2)

        elif method == 'exchange':
            preceding_1 = self.edges_inv[route1][node1]
            preceding_2 = self.edges_inv[route2][node2]
            
            self._remove_node(route1, node1)
            self._remove_node(route2, node2)
            self._insert_node(route1, node2, preceding_node = preceding_1)
            self._insert_node(route2, node1, preceding_node = preceding_2)

        elif method == '2opt':
            self._opt2(route1, node1, node2)

        else:
            raise Exception

        return None

    def print(self, route = None, print_best = True):
        # print routes method

        if print_best:
            routes = self.best.copy()
        else:
            routes = self.edges.copy()
        
        if route is None:
            routes_to_print = routes.keys()
        else:
            routes_to_print = [route]

        print("Routes:")
        for r in routes_to_print:
            print(f"route {r+1}: ", end = '')
            print(f"{"0".ljust(2, ' ')} -> ", end ='')
            n = routes[r][0]
            while n != 0:
                print(f"{str(n).ljust(2, ' ')} -> ", end ='')
                n = routes[r][n]
            print("0")
        print("")

        return None
