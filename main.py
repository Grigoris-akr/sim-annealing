#!/home/golis/.venvs/venv1/bin/python3
import time
from routes import *
from near_neigh import *
from sim_anneal import *
from vns import *
from utils import *
from local_search import *

import copy

if __name__ == '__main__':
    # Data reading and formatting
    file = 'prov6.txt'
    data = read_data(file)
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create the routes object
    routes = AbstractRoutes(distance_matrix, data["node_dem"])
    ls = localSearch(distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Nearest Neighbor
    startTime = time.perf_counter()
    routes = near_neigh(routes, distance_matrix, data["node_dem"], data["veh_cap"])
    print(f"cost: {routes.get_best_cost()} time: {time.perf_counter() - startTime}")
    save_plot_from_edges(routes.edges, data["node_coords"], filename = "nn2")

    nn_routes = copy.deepcopy(routes)
    # startTime = time.perf_counter()
    # for i in range(100000):
    #     routes = ls.reloc_1_0(routes)
    # print(f"cost_oz: {routes.get_cost()} time: {time.perf_counter() - startTime}")
    # save_plot_from_edges(routes.best, data["node_coords"], filename = "nn_oz")
    
    startTime = time.perf_counter()
    sa_routes = sim_anneal(routes, ls, temp_upd_method = 'linear', init_T = 50, final_T = 1, alpha = 0.10, max_iter=1000)
    print(f"cost: {sa_routes.get_best_cost()} time: {time.perf_counter() - startTime}")
    save_plot_from_edges(routes.best, data["node_coords"], filename = "nn3")
    save_plot_from_edges(sa_routes.best, data["node_coords"], filename = "nn_sa")

    #for i in range(len(routes)):
    #    print(routes.edges[i])

    #startTime = time.perf_counter()
    # vns_routes = vns(data, sa_routes.best)
    # print(f"cost: {routes.best_cost()} time: {time.perf_counter() - startTime}")
    # save_plot(sa_routes, data["node_coords"], filename = "nn")

    print('finish')
