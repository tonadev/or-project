import numpy as np

class Heuristic:
    def __init__(self, dimension, n_iterations):
        self.dimension = dimension
        self.n_iterations = n_iterations

    def run(self, objective_fn, neighborhood_fn, initial_sol, params):
        pass

class TabuSearch(Heuristic):
    def __init__(self, dimension, n_iterations):
        super().__init__(dimension, n_iterations)

        # Initialize tabu matrix
        self.tabu_matrix = dict()

    def run(self, objective_fn, neighborhood_fn, initial_sol, params):
        [p_time, times] = params

        # Generate an initial solution
        best = initial_sol
        # Evaluate the initial solution
        best_eval = objective_fn(best, times)
        # Current working solution
        curr, curr_eval = best, best_eval

        self.tabu_matrix[np.array_repr(best)] = {
                        "short_memory": 0,
                        "long_memory": 0
                    }
        
        # Run the algorithm
        for i in range(self.n_iterations):
            neighbors = neighborhood_fn(curr)

            best_neighbor, best_neigbor_eval = curr, curr_eval
            for neighbor in neighbors:
                neighbor_name = np.array_repr(neighbor)

                if neighbor_name not in self.tabu_matrix:
                    self.tabu_matrix[neighbor_name] = {
                        "short_memory": 0,
                        "long_memory": 0
                    }

                neighbor_eval = objective_fn(neighbor, times)
                neighbor_penalized_eval = neighbor_eval + self.tabu_matrix[neighbor_name]["long_memory"]

                best_neighbor_name = np.array_repr(best_neighbor)
                best_neighbor_penalized_eval = best_neigbor_eval + self.tabu_matrix[best_neighbor_name]["long_memory"]

                # Check aspiration level
                if neighbor_eval < best_eval:
                    best = neighbor
                    best_eval = neighbor_eval
                    best_neighbor = neighbor
                    best_neigbor_eval = neighbor_eval
                elif neighbor_penalized_eval < best_neighbor_penalized_eval and self.tabu_matrix[neighbor_name]["short_memory"] == 0:
                    best_neighbor = neighbor
                    best_neigbor_eval = neighbor_eval

            # Choose best feasible solution
            curr, curr_eval = best_neighbor, best_neigbor_eval

            # Check for new best solution
            if curr_eval <= best_eval:
                # Store new best solution
                best, best_eval = curr, curr_eval
                # Report progress
                print('[INFO] >%d f(%s) = %.5f' % (i, best, best_eval))

            # Update tabu matrix
            for key in self.tabu_matrix.keys():
                if self.tabu_matrix[key]["short_memory"] > 0:
                    self.tabu_matrix[key]["short_memory"] -= 1
            
            best_neighbor_name = np.array_repr(best_neighbor)
            # Update short term memory
            self.tabu_matrix[best_neighbor_name]["short_memory"] = p_time
            # Update large term memory with frequency
            self.tabu_matrix[best_neighbor_name]["long_memory"] += 1

        return [best, best_eval]
    
class SimulatedAnnealing(Heuristic):
    def run(self, objective_fn, neighborhood_fn, initial_sol, params):
        [L, initial_temp, times] = params

        # Generate an intial solution
        best = initial_sol
        # Evaluate the initial solution
        best_eval = objective_fn(best, times)
        # Current working solution
        curr, curr_eval = best, best_eval

        # Run the algorithm
        for i in range(self.n_iterations):
            for _ in range(L):
                neighbors = neighborhood_fn(curr)

                for neighbor in neighbors:
                    # Evaluate candidate point
                    neighbor_eval = objective_fn(neighbor, times)

                    # Check for new best solution
                    if neighbor_eval < best_eval:
                        # Store new best point 
                        best, best_eval = neighbor, neighbor_eval
                        # Report progress
                        print('[INFO] >%d f(%s) = %.5f' % (i, best, best_eval))

                    # Difference between candidate and current point evaluation
                    diff = neighbor_eval - curr_eval

                    # Calculate temperature for current epoch (using Cauchy)
                    t = initial_temp / float(i + 1)

                    # Calculate metropolis acceptance criterion
                    metropolis = np.exp(-diff / t)

                    # Check if we should keep the new point
                    if diff < 0 or np.random.rand() < metropolis:
                        # Store the new current point
                        curr, curr_eval = neighbor, neighbor_eval
                        
        return [best, best_eval]