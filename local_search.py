import numpy as np
import random

class localSearch:
    def __init__(self, distance_matrix, node_dem_l, veh_cap):
        self.dist_mat = np.array(distance_matrix)
        self.node_dem = np.array(node_dem_l)
        self.N = self.dist_mat.shape[0] 
        self.veh_cap = veh_cap
         
    def reloc_1_0(self, edges, edges_inc, load):
        # route_i: x -> i -> y | x ------> y 
        # route_j: j ------> z | j -> i -> z

        # get random route
        route_i = random.randint(0, len(edges)-1)
        # get random node
        i = random.choice(list(edges[route_i].keys())) 

        # fix this as well
        while i == 0:
            i = random.choice(list(edges[route_i].keys())) 

        # skip origin route # TODO - fix this
        routes_loads = load.copy()
        routes_loads[route_i] = 1000

        eligible_routes = np.argwhere(routes_loads + self.node_dem[i] <= self.veh_cap).T[0] # maybe no zero
        
        if eligible_routes.size == 0:
            return None, None, None, None, None
        
        # get random position to insert
        route_j = random.choice(eligible_routes)
        j  = random.choice(list(edges[route_j].keys()))
        
        # nodes
        x = edges_inc[route_i][i]
        y = edges[route_i][i]
        z = edges[route_j][j]
        
        # edge distances
        x_i = self.dist_mat[x, i]
        i_y = self.dist_mat[i, y]
        x_y = self.dist_mat[x, y]

        j_z = self.dist_mat[j, z] 
        j_i = self.dist_mat[j, i]
        i_z = self.dist_mat[i, z]
        
        # delta = new edges - old edges
        delta = (x_y + j_i + i_z) - (x_i + i_y + j_z) 

        return route_i, i, route_j, j, delta

    def exch_1_1(self, edges, edges_inc, load):
        # route1: x1 -> n1 -> y1 | x1 -> n2 -> y1 
        # route2: x2 -> n2 -> y2 | x2 -> n1 -> y2 

        # get random route
        route1 = random.randint(0, len(edges)-1)
        # get random node
        node1 = random.choice(list(edges[route1].keys())) 

        # fix this as well
        while i == 0:
            i = random.choice(list(edges[route1].keys())) 

        # skip origin route # TODO - fix this
        routes_loads = load.copy()
        routes_loads[route1] = 1000

        eligible_routes = np.argwhere(routes_loads + self.node_dem[i] <= self.veh_cap).T[0]
        

        if eligible_routes.size == 0:
            return None, None, None, None, None
        
        
        # nodes
        x = edges_inc[route1][node1]
        y = edges[route1][node1]
        z = edges[route2][node2]
        
        # edge distances
        x1_n1 = self.dist_mat[x, i]
        n1_y1 = self.dist_mat[i, y]
        x1_y1 = self.dist_mat[x, y]

        n2_y2 = self.dist_mat[j, z] 
        j_i = self.dist_mat[j, i]
        i_z = self.dist_mat[i, z]
        
        # delta = new edges - old edges
        delta = (x_y + j_i + i_z) - (x_i + i_y + j_z) 

        return route_i, i, route_j, j, delta

    def opt2(self,):
        pass

