import matplotlib.pyplot as plt
import time
import random
import threading
import globals as g
import constants
import algo_demo

# Global variables to store results for each thread
algorithm_results = {
    constants.ALGO_BACKTRACKING: [],
    constants.ALGO_BEST_FIRST: [],
    constants.ALGO_HILL_CLIMB: [],
    constants.ALGO_CULTURAL: []
}

# Function to run the algorithm and store results in the global dictionary
def run_algorithm_in_thread(n, strategy):
    """
    Run the selected algorithm in a separate thread and store the results.
    """
    solutions, times = run_algorithm_for_n(n, strategy)
    algorithm_results[strategy] = (solutions, times)  # Store results for this strategy

def run_algorithm_for_n(n, strategy):
    """
    Run the selected algorithm and return the solutions and time consumed for each solution.
    """
    start_time = time.perf_counter()
    
    if strategy == constants.ALGO_BACKTRACKING:
        solutions, solution_times = algo_demo.backtracking(n, record_times=True, start_time=start_time)
        return solutions, solution_times
    
    elif strategy == constants.ALGO_BEST_FIRST:
        solutions = algo_demo.best_first(n)
        end_time = time.perf_counter()
        return solutions, [end_time - start_time]  # Single time for the solution
    
    elif strategy == constants.ALGO_HILL_CLIMB:
        solutions = algo_demo.hill_climbing(n)
        end_time = time.perf_counter()
        return solutions, [end_time - start_time]  # Single time for the solution
    
    elif strategy == constants.ALGO_CULTURAL:
        solutions = algo_demo.cultural(n)
        end_time = time.perf_counter()
        return solutions, [end_time - start_time]  # Single time for the solution
    
    else:
        return [], []  # If unknown strategy


def plot_algorithm_performance_fixed_n(n):
    """
    Plot the performance of different algorithms for a fixed n (e.g., n = 8), treating each solution as a separate point.
    Each algorithm's solutions will be plotted with the same color.
    """
    strategies = [constants.ALGO_BACKTRACKING, constants.ALGO_BEST_FIRST, constants.ALGO_HILL_CLIMB, constants.ALGO_CULTURAL]
    
    # Define color for each strategy
    strategy_colors = {
        constants.ALGO_BACKTRACKING: 'r',  # Red
        constants.ALGO_BEST_FIRST: 'b',    # Blue
        constants.ALGO_HILL_CLIMB: 'y',    # Yellow
        constants.ALGO_CULTURAL: 'm',      # Magenta
    }
    
    # Start each algorithm in a separate thread
    threads = []
    for strategy in strategies:
        thread = threading.Thread(target=run_algorithm_in_thread, args=(n, strategy))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Now plot the results from the global dictionary
    plt.figure(figsize=(10, 6))

    # For each strategy, plot the number of solutions and time consumed for each solution
    for strategy in strategies:
        solutions, times = algorithm_results.get(strategy, ([], []))
        
        if not solutions:
            continue  # Skip if no solutions found
        
        color = strategy_colors.get(strategy, 'k')  # Default color 'k' for unknown strategies
        
        # Plot each solution as a separate point for the strategy
        for idx, time_taken in enumerate(times):
            plt.scatter(time_taken, idx + 1, color=color, alpha=0.7, marker='o')

        # Add label to the legend for this strategy (just once per algorithm)
        plt.scatter([], [], color=color, label=strategy)  # Invisible point for legend only

    # Add labels and title
    plt.title(f'Algorithm Performance: Solutions vs Time for n = {n}', fontsize=14)
    plt.xlabel('Time Consumed (seconds)', fontsize=12)
    plt.ylabel('Solution Count', fontsize=12)
    
    # Add legend
    plt.legend(title="Algorithms", fontsize=10, loc='upper left')
    
    # Show grid and plot
    plt.grid(True)
    plt.show()

# Set the fixed n value (e.g., n = 8)
n = 8
plot_algorithm_performance_fixed_n(n)
