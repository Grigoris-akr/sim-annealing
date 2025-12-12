#!/home/golis/.venvs/venv1/bin/python3
import numpy as np
import random


def cost_deviation_watchdog():
    pass

class temperature:
    def __init__(self, init_T, final_T, alpha):
        self.now = init_T
        self.init_T = init_T
        self.final_T = init_T
        self.alpha = alpha
        # maybe final_T == 0 -> easy check
    
    def update(self, iteration):
        self.now = max(final_T, (self.init_T * np.exp(-iteration * self.alpha)))
        
    

def acceptance(delta, T):
    return np.exp(-(delta/T)) > random.rand()


deviation_too_much = False

def sim_anneal(routes, node_dem_l, init_T = 1200, final_T = 1, alpha = 0.9, max_iter=1000):
    N = np.size(adj_cube, axis = 1)
    print(f"N: {N}")
    T = temperature(init_t, final_T, alpha)

    i = 0
    while T.now:
        
        for i in range(max_iter):
            # choose perturbation
            if random.rand() > 0.5:
                delta = routes.apply_reloc() 
            else:
                pass
                #delta = routes.apply_exch() 

            if routes.get_delta_from_best() > 0:
                routes.update_best()
                continue
            
            # acceptance probability
            if np.exp(-(delta/T.now)) > random.rand():
                routes.commit()
            else:
                routes.revert()
            
            if deviation_too_much:
                routes.reset_to_best()

        i += 1
        T.update(i, alpha)

    return routes
