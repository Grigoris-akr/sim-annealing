#!/home/golis/.venvs/venv1/bin/python3
import numpy as np

def near_neigh(routes, distance_matrix, node_dem_l, veh_cap):
    """ 
    Nearest neighbor function 
    
    Parameters:
    routes:     object of type AbstractRoutes
    etc
    """
    node_dem_l = np.array(node_dem_l)

    N = np.size(distance_matrix, 0)
    unchecked_nodes = np.ones(N) # array containing 1s for every unchecked node
    unchecked_nodes[0] = np.nan

    start_node = 0
    route_idx = 0
    while not np.isnan(unchecked_nodes).all():
        # elimination due to capacity restriction
        eligible_nodes = np.argwhere(node_dem_l * unchecked_nodes + routes.load[route_idx] <= veh_cap).T[0]

        if eligible_nodes.size == 0:
            # no available nodes, returning to depot
            routes.am[route_idx][start_node, 0] = distance_matrix[start_node, 0]
            
            routes.edges[route_idx][start_node] = 0
            routes.edges_inc[route_idx][0] = start_node

            routes.new_route()

            start_node = 0
            route_idx += 1
            continue

        # get nearest node
        nearest_node = eligible_nodes[np.argmin(distance_matrix[start_node, eligible_nodes])]

        # add the node
        routes.am[route_idx][start_node, nearest_node] = distance_matrix[start_node, nearest_node]
        routes.load[route_idx] += node_dem_l[nearest_node]
    
        #print(route_idx)
        #print(start_node)
        #print(nearest_node)
        routes.edges[route_idx][start_node] = nearest_node
        routes.edges_inc[route_idx][nearest_node] = start_node

        # remove node from unchecked_nodes list
        unchecked_nodes[nearest_node] = np.nan

        # setting start as this node
        start_node = nearest_node.copy()
    
    # finilize last route
    routes.am[route_idx][start_node, 0] = distance_matrix[start_node, 0]

    routes.edges[route_idx][start_node] = 0
    routes.edges_inc[route_idx][0] = start_node

    routes.update_best()
    return routes

