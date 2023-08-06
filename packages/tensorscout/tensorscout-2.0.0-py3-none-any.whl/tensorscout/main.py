import numpy as np
import pathos.multiprocessing as pathosmp
from pathos.multiprocessing import ProcessPool

from functools import wraps

import matplotlib.pyplot as plt
import math


def multicarlo(num_iters, num_cores):
    '''
    This decorator performs a non-dynamic operation or task for a specified number of iterations num_iters and distributes the tasks across a requested number of available processors num_cores.
    
    Parameters
    ------------
    num_cores: int
        Number of processors to use 
    num_iters : int
        The number of iterations to perform for a specific model / Monte Carlo simulation. 
    '''
    def decorator_monte_carlo(monte_carlo_func):
        @wraps(monte_carlo_func)
        def wrapper_monte_carlo(data, *args, **kwargs):
            def simulate_data(data, num_iters):
                results = []
                for i in range(num_iters):
                    simulated_data = monte_carlo_func(data, *args, **kwargs)
                    results.append(simulated_data)
                return results
            
            pool = pathosmp.ProcessingPool(num_cores)
            iterations_per_process = num_iters // num_cores
            partial_simulate_data = lambda i: simulate_data(data, iterations_per_process)
            results = pool.map(partial_simulate_data, range(num_cores))
            flattened_results = [item for sublist in results for item in sublist]
            return flattened_results
        return wrapper_monte_carlo
    return decorator_monte_carlo


def cakerun(num_cores, L_sectors):
    '''
    This decorator partitions an array into sectors and applies a given function to each sector in parallel. The result of each computation is merged into a final output array.

    Parameters
    ------------
    num_cores: int
        Number of processors to use
    L_sectors : int
        The length scale for the number of sectors [per column]. For non-square arrays, the number of sectors per row gets adjusted as a function of this value 
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(matrix, *args, **kwargs):
            'for non-square arrays, this treatment '
            sector_size = math.ceil(matrix.shape[0] / (L_sectors))
            num_sectors_per_row = math.ceil(matrix.shape[1] / (sector_size))
            # num_sectors = num_sectors_per_row * L_sectors

            'partition the matrix into sectors'
            sectors = [
                matrix[i:i+sector_size, j:j+sector_size]
                for i in range(0, matrix.shape[0], sector_size)
                for j in range(0, matrix.shape[1], sector_size)
            ]

            'ProcessPool performs computations in parallel'
            with ProcessPool(num_cores) as pool:
                results = pool.map(lambda sector: func(sector, *args, **kwargs), sectors)

            '''Merging of processed sectors back to single, merged matrix'''
            merged_matrix = np.hstack(results[:num_sectors_per_row])
            for i in range(1, L_sectors):
                row = np.hstack(results[i*num_sectors_per_row:(i+1)*num_sectors_per_row])
                merged_matrix = np.vstack([merged_matrix, row])

            'check merged matrix dims'
            # print("Merged matrix shape:", merged_matrix.shape)
            # print("New number of sectors:", num_sectors)

            return merged_matrix

        return wrapper
    return decorator


