#!/home/golis/.venvs/venv1/bin/python3
import time
import copy
import random
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
    plot(routes.best, data["node_coords"], filename = f"plots/{func.__name__}_{routes.get_best_cost():0.2f}")
    routes.print(print_best = True)
    return routes

if __name__ == '__main__':
    # set rng seed
    random.seed(1000)

    # Data reading and formatting
    file = 'prov6.txt'
    data = read_data(file)
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create routes and local search objects
    routes = AbstractRoutes(distance_matrix, data["node_dem"])
    ls = localSearch(distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Nearest Neighbor
    routes = run(near_neigh, routes, distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Simulated Annealing
    #routes = run(sim_anneal, routes, ls, temp_upd_method = 'linear', init_T = 50, final_T = 1, alpha = 0.10, max_iter=2000)
    routes = run(sim_anneal, routes, ls, temp_upd_method = 'exponential', init_T = 50, final_T = 1, alpha = 0.0005, max_iter=10)

    #sa_routes = copy.deepcopy(routes)
    
    # VNS
    routes = run(vns, routes, ls, max_iter = 1000, ls_iter = 2000)

    print('finish')
