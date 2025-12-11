#!/home/golis/.venvs/venv1/bin/python3
import time
from routes import *
from near_neigh import *
from sim_anneal import *
from vns import *
from utils import *
from local_search import *

if __name__ == '__main__':
    # Data reading and formatting
    file = 'prov6.txt'
    data = read_data(file)
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create the routes object
    routes = AbstractRoutes(distance_matrix)
    ls = localSearch(distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Nearest Neighbor
    startTime = time.perf_counter()
    routes = near_neigh(routes, distance_matrix, data["node_dem"], data["veh_cap"])
    print(f"cost: {routes.get_best_cost()} time: {time.perf_counter() - startTime}")
    print(f"cost2: {routes.get_cost()} time: {time.perf_counter() - startTime}")

    save_plot_from_edges(routes.edges, data["node_coords"], filename = "nn2")


    startTime = time.perf_counter()
    for i in range(100000):
        routes = ls.reloc_1_0(routes)
    
    print(f"cost_oz: {routes.get_cost()} time: {time.perf_counter() - startTime}")
    save_plot_from_edges(routes.edges, data["node_coords"], filename = "nn_oz")
    
    #for i in range(len(routes)):
    #    print(routes.edges[i])

    #startTime = time.perf_counter()
    # sa_routes = simAnneal(data, nn_routes.best)
    # print(f"cost: {routes.best_cost()} time: {time.perf_counter() - startTime}")
    # save_plot(nn_routes.best, data["node_coords"], filename = "nn")

    #startTime = time.perf_counter()
    # vns_routes = vns(data, sa_routes.best)
    # print(f"cost: {routes.best_cost()} time: {time.perf_counter() - startTime}")
    # save_plot(sa_routes, data["node_coords"], filename = "nn")

    print('finish')
