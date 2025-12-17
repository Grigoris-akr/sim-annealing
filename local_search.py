import numpy as np
import random

class localSearch:
    def __init__(self, distance_matrix, node_dem_l, veh_cap):
        self.dist_mat = np.array(distance_matrix)
        self.node_dem = np.array(node_dem_l)
        self.node_num = self.dist_mat.shape[0] 
        self.veh_cap = veh_cap

    def apply_local_search(self, edges, edges_inc, load, node_route = None, method = ''):
        if method == 'relocation':
            return self.reloc_1_0(edges, edges_inc, load)
        elif method == 'exchange':
            return self.exch_1_1(edges, edges_inc, load, node_route)
        elif method == '2opt':
            return self.opt2(edges, edges_inc)
        else:
            raise Exception()
         
    def reloc_1_0(self, edges, edges_inc, load):
        # route1: p1 -> n1 -> a1 | p1 -------> a1 
        # route2: n2 -------> a2 | n2 -> n1 -> a2

        # get random route
        route1 = random.randint(0, len(edges)-1)
        # get random node
        node1 = random.choice(list(edges[route1].keys())) 

        # fix this as well
        while node1 == 0:
            node1 = random.choice(list(edges[route1].keys())) 

        # skip origin route # TODO - fix this
        routes_loads = load.copy()
        routes_loads[route1] = 1000

        eligible_routes = np.argwhere(routes_loads + self.node_dem[node1] <= self.veh_cap).T[0] # maybe no zero
        
        if eligible_routes.size == 0:
            return None, None, None, None, None
        
        # get random position to insert
        route2 = random.choice(eligible_routes)
        node2  = random.choice(list(edges[route2].keys()))
        
        # nodes
        p1 = edges_inc[route1][node1]
        a1 = edges[route1][node1]
        a2 = edges[route2][node2]
        
        # edge distances
        p1_n1 = self.dist_mat[p1, node1]
        n1_a1 = self.dist_mat[node1, a1]
        n2_a2 = self.dist_mat[node2, a2] 

        p1_a1 = self.dist_mat[p1, a1]
        n2_n1 = self.dist_mat[node2, node1]
        n1_a2 = self.dist_mat[node1, a2]
        
        # delta = new edges - old edges
        delta = (p1_a1 + n2_n1 + n1_a2) - (p1_n1 + n1_a1 + n2_a2) 

        return route1, node1, route2, node2, delta

    def exch_1_1(self, edges, edges_inc, load, node_route):
        # route1: p1 -> n1 -> a1 | p1 -> n2 -> a1 
        # route2: p2 -> n2 -> a2 | p2 -> n1 -> a2 
        
        # get random route
        route1 = random.randint(0, len(edges)-1)
        # get random node
        node1 = random.choice(list(edges[route1].keys()))

        # fix this as well
        while node1 == 0:
            node1 = random.choice(list(edges[route1].keys()))
        
        # remove route1 from the search # TODO fix it
        load_cpy = load.copy()
        load_cpy[route1] = 10000

        # route load per node
        node_route_load = load_cpy[node_route]

        # remove depot from the eligible routes
        node_route_load[0] = 10000

        # route load per node - node demand + node1 demand
        eligible_nodes = np.argwhere(node_route_load - self.node_dem + self.node_dem[node1] <= self.veh_cap).T[0] # maybe no zero

        if eligible_nodes.size == 0:
            return None, None, None, None, None

        # get random position to insert
        node2 = random.choice(eligible_nodes)
        route2 = node_route[node2]

        # nodes
        p1 = edges_inc[route1][node1]
        a1 = edges[route1][node1]
        p2 = edges_inc[route2][node2]
        a2 = edges[route2][node2]

        # edge distances
        p1_n1 = self.dist_mat[p1, node1]
        n1_a1 = self.dist_mat[node1, a1]
        p2_n2 = self.dist_mat[p2, node2]
        n2_a2 = self.dist_mat[node2, a2]

        p1_n2 = self.dist_mat[p1, node2]
        n2_a1 = self.dist_mat[node2, a1]
        p2_n1 = self.dist_mat[p2, node1]
        n1_a2 = self.dist_mat[node1, a2]

        # delta = new edges - old edges
        delta = (p1_n2 + n2_a1 + p2_n1 + n1_a2) - (p1_n1 + n1_a1 + p2_n2 + n2_a2)

        return route1, node1, route2, node2, delta


    def opt2(self, edges, edges_inc):
        # -->p1-->.  .<-n2--<--p2<---    -->p1 ------> n2 --> p2-->-
        #          \/               ^ =>                           |
        #          /\               | =>                           V
        # <--a2<--'  `--> n1-->a1---^    <--a2 <-------- n1 <-a1 <--

        # get random route
        route = random.randint(0, len(edges)-1)
        
        # node list
        node_list = list(edges[route].keys())

        # get random node1
        node1 = random.choice(node_list)
        
        # remove node1, its preceding and succeeding nodes
        node_list.remove(node1)
        node_list.remove(edges[route][node1])
        node_list.remove(edges_inc[route][node1])
        
        if node_list == []:
            return None, None, None, None

        # get random node2
        node2 = random.choice(node_list)
        
        # preceding/succeeding nodes
        p1 = edges_inc[route][node1]
        a2 = edges[route][node2]
        
        # edge costs
        # old
        p1_n1 = self.dist_mat[p1, node1]
        n2_a2 = self.dist_mat[node2, a2]
        # new
        p1_n2 = self.dist_mat[p1, node2]
        n1_a2 = self.dist_mat[node1, a2]

        delta = (p1_n2 + n1_a2) - (p1_n1 + n2_a2)

        return route, node1, None, node2, delta
