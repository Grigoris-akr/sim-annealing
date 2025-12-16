#!/home/golis/.venvs/venv1/bin/python3
import time
import copy
from routes import *
from near_neigh import *
from sim_anneal import *
from vns import *
from utils import *
from local_search import *


def run(func, *args, **kwargs):
    """ wrap timer and plotting around functions """

    startTime = time.perf_counter()
    routes = func(*args, **kwargs)
    print(f"{func.__name__} > cost: {routes.get_best_cost():0.2f} time: {(time.perf_counter() - startTime):0.5f} sec")
    save_plot_from_edges(routes.best, data["node_coords"], filename = f"{func.__name__}_{routes.get_best_cost():0.2f}")
    for r in routes.best.keys():
        #print(routes.best[r].values())
        print(f"route {r+1}: ", end = '')
        for n in list(routes.best[r].keys()):
            print(f"{str(n).ljust(2, ' ')} -> ", end ='')
        print("0")

    return routes

if __name__ == '__main__':
    # Data reading and formatting
    file = 'prov6.txt'
    data = read_data(file)
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create the routes object
    routes = AbstractRoutes(distance_matrix, data["node_dem"])
    ls = localSearch(distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Nearest Neighbor
    routes = run(near_neigh, routes, distance_matrix, data["node_dem"], data["veh_cap"])

    # simulated annealing
    #routes = run(sim_anneal, routes, ls, temp_upd_method = 'linear', init_T = 50, final_T = 1, alpha = 0.10, max_iter=2000)
    routes = run(sim_anneal, routes, ls, temp_upd_method = 'exponential', init_T = 50, final_T = 1, alpha = 0.0005, max_iter=100)

    #for i in range(len(routes)):
    #    print(routes.edges[i])

    #startTime = time.perf_counter()
    # vns_routes = vns(data, sa_routes.best)
    # print(f"cost: {routes.best_cost()} time: {time.perf_counter() - startTime}")
    # save_plot(sa_routes, data["node_coords"], filename = "nn")

    print('finish')
