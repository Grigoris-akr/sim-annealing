import numpy as np
import random


def two_opt():
    pass

def exch_1_1(routes):
    pass



class localSearch:
    def __init__(self, distance_matrix, node_dem_l, veh_cap):
        self.dist_mat = np.array(distance_matrix)
        self.node_dem = np.array(node_dem_l)
        self.N = self.dist_mat.shape[0] 
        self.veh_cap = veh_cap
         
    def reloc_1_0(self, routes):

        # get random route
        route_i = random.randint(0, len(routes)-1)
        # get random node
        i = random.choice(list(routes.edges[route_i].keys())) 

        # fix this as well
        while i == 0:
            i = random.choice(list(routes.edges[route_i].keys())) 

        # skip origin route
        routes_loads = routes.load.copy()
        routes_loads[route_i] = 1000

        eligible_routes = np.argwhere(routes_loads + self.node_dem[i] <= self.veh_cap).T[0] # maybe no zero
        
        if eligible_routes.size == 0:
            #print("no eligible routes")
            return routes
        
        # get random position to insert
        route_j = random.choice(eligible_routes)
        j  = random.choice(list(routes.edges[route_j].keys()))
        
        # route_i: x -> i -> y | x ------> y 
        # route_j: j ------> z | j -> i -> z
        
        # nodes
        x = routes.edges_inc[route_i][i]
        y = routes.edges[route_i][i]
        z = routes.edges[route_j][j]
        
        # edge distances
        x_i = self.dist_mat[x, i]
        i_y = self.dist_mat[i, y]
        x_y = self.dist_mat[x, y]

        j_z = self.dist_mat[j, z] 
        j_i = self.dist_mat[j, i]
        i_z = self.dist_mat[i, z]
        
        # cost check
        if (x_i + i_y + x_y) > (i_z + j_i + i_z):
            print("better route")
            # delete node i from route_i
            routes.edges[route_i].pop(i)
            routes.edges_inc[route_i].pop(i)
            
            # reconnect route_i
            routes.edges[route_i][x] = y
            routes.edges_inc[route_i][y] = x
            
            # add node i to route_j
            routes.edges[route_j][j] = i
            routes.edges_inc[route_j][i] = j
            routes.edges[route_j][i] = z
            routes.edges_inc[route_j][z] = i


        return routes

    def exch_1_1(self,):
        pass

