import time
import copy
import random
import os
from routes import *
from local_search import *
from near_neigh import *
from sim_anneal import *
from vns import *
from sa_vns import *
from utils import *


def run(func, *args, **kwargs):
    """ wrap timer and graph plotting around functions """

    startTime = time.perf_counter()
    routes = func(*args, **kwargs)
    print(f"{func.__name__} > cost: {routes.get_best_cost():0.2f} time: {(time.perf_counter() - startTime):0.5f} sec")
    plot(routes.best, data["node_coords"], filename = os.path.join("plots", f"{func.__name__}_{routes.get_best_cost():0.2f}"))
    routes.print(print_best = True)
    return routes

if __name__ == '__main__':
    # create directory for plots
    os.makedirs("plots", exist_ok=True)

    # set RNG seed
    random.seed(1) # SA and VNS with seed=1 -> 523.31

    # Data reading and formatting
    data = read_data(file = "prov6.txt")
    distance_matrix = get_distance_matrix(data["node_coords"])

    # Create routes and local search objects
    routes = AbstractRoutes(distance_matrix, data["node_dem"])
    ls = localSearch(distance_matrix, data["node_dem"], data["veh_cap"])
    
    # Nearest Neighbor
    routes = run(near_neigh, routes, distance_matrix, data["node_dem"], data["veh_cap"])


    # == SA and VNS == #
    # Simulated Annealing
    #routes = run(sim_anneal, routes, ls, temp_upd_method = 'linear', init_T = 50, final_T = 1, alpha = 0.10, max_iter = 2000)
    routes = run(sim_anneal, routes, ls, temp_upd_method = 'exponential', init_T = 50, final_T = 1, alpha = 0.0005, max_iter = 10)

    # VNS
    routes = run(vns, routes, ls, max_iter = 1000, ls_iter = 1000)
    
    # == SA-VNS hybrid == #
    # SA-VNS
    #routes = run(sa_vns, routes, ls, temp_upd_method = 'exponential', init_T = 50, final_T = 1, alpha = 0.0005, ls_iter = 1000)
    #routes = run(sa_vns, routes, ls, temp_upd_method = 'linear', init_T = 50, final_T = 1, alpha = 0.10, ls_iter = 2000)
    
    print('finish')
