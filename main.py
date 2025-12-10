#!/home/golis/.venvs/venv1/bin/python3
import time
from near_neigh import *
from sim_anneal import *
from vns import *
from utils import *

if __name__ == '__main__':
    # Data reading and formatting
    file = 'prov6.txt'
    data = read_data(file)
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create the routes object
    routes = AbstractRoutes(distance_matrix)
    
    # Nearest Neighbor
    startTime = time.perf_counter()
    routes = near_neigh(routes, distance_matrix, data["node_dem"], data["veh_cap"])
    print(f"cost: {routes.get_best_cost()} time: {time.perf_counter() - startTime}")
    save_plot(routes.best_am, data["node_coords"], filename = "nn")
    
    startTime = time.perf_counter()
    # sa_routes = simAnneal(data, nn_routes.best)
    # print(f"cost: {routes.best_cost()}")
    # save_plot(nn_routes.best, data["node_coords"], filename = "nn")

    # vns_routes = vns(data, sa_routes.best)
    # print(f"cost: {routes.best_cost()}")
    # save_plot(sa_routes, data["node_coords"], filename = "nn")

    print('finish')
