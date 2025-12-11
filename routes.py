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
        self.update_list_view()
        self.best_am = self.am.copy()
        self.best_l  = self.list.copy()
        self.best_cost = np.einsum('kij -> k', self.am)
        # self.best_cost = np.einsum('ij, kij -> k', self.dist_map..., self.am)


    def commit(self,):
        # commit the perturabation
        pass

    def revert(self,):
        # revert the perturbation
        pass

