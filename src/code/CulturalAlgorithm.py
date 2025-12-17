import random
import time


# Fitness Score Function -------------------------------

def fitness(board):
    n = len(board)
    score = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] != board[j] and abs(board[i] - board[j]) != abs(i - j):
                score += 1
    return score

# Random Board (gen 0) -------------------------------

def random_board(n):
    board = list(range(1, n+1))
    random.shuffle(board)
    return board

# Crossover (Ordered crossover => to avoid duplicates) ------------------

def crossover(parent1, parent2):
    n = len(parent1)
    a,b = sorted(random.sample(range(n),2))
    child = [None] * n
    child[a:b] = parent1[a:b]
    remaining = [x for x in parent2 if x not in child]
    index = 0
    for i in range(n):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1
    return child

# Mutation (swap two places, to produce new population) ------------------------

def mutate(board):
    n = len(board)
    a,b = random.sample(range(n),2)
    board[a], board[b] = board[b], board[a]
    return board

# Belief Space --------------------------

# initialization

def init_belief_space(n):
    return{
        'min_col' : [1] * n,
        'max_col' : [n] * n,
        'best_solution' : None,
        'best_fitness' : -1
    }

# update space

def update_belief_space(belief, parents):
    n = len(parents[0])
    for board in parents:
        for row in range(n):
            col = board[row]
            belief['min_col'][row] = min(belief['min_col'][row],col)
            belief['max_col'][row] = max(belief['max_col'][row],col)
        f = fitness(board)
        if f > belief['best_fitness']:
            belief['best_fitness'] = f
            belief['best_solution'] = board[:]

# influence (new rules that influences children) -----------------------------------

def influence(board, belief):
    n = len(board)
    new_board = board[:]
    for row in range(n):
        low = belief['min_col'][row]
        high = belief['max_col'][row]
        if not (low <= new_board[row] <= high):
            new_board = random.randint(low,high)
    return new_board

# main function of cultural algorithm -------------------------

def cultural_algorithm(n,time, population_size = 100, time_limit_seconds = 60):
    start_time = time
    population = [random_board(n) for _ in range(population_size)]
    belief = init_belief_space(n)
    perfect_score = n * (n - 1) // 2

    gen = 0

    while True:

        #check time limit
        elapsed = time - start_time
        if elapsed >= time_limit_seconds:
            print("\n Time Limit Reached")
            break

        #calculate and rank fitness score for each board in population (generation)
        score = [(fitness(board),board) for board in population]
        score.sort(reverse=True)
        best_fitness, best_board = score[0]

        #check if best_fitness is the perfect score
        if best_fitness == perfect_score:
            elapsed = time - start_time
            print("\nCultural Algorithm Results(0):")
            print(f"\nPerfect solution found at generation {gen}")
            print(f"Number of Queens : {n}")
            print(f"Total time taken : {elapsed:.6f} seconds")
            return best_board, gen, elapsed

        #create parents for next generation (20% of current generation's best boards)
        parents_counts = max(1, population_size // 5)
        # the tuple is structured like (fitness_score, board) , so this means i only take the board part from the tuple
        parents = [board for _, board in score[:parents_counts]]

        #update belief space
        update_belief_space(belief,parents)

        #create new population (generation) => doing crossover and mutation on parents
        new_population = []
        while len(new_population) < population_size:
            p1,p2 = random.sample(parents,2) # take two of the parents to operate on
            child = crossover(p1,p2)
            if random.random() < 0.3: # use propability for diversity => avoid too little or too much mutation (healthy balance)
                child = mutate(child)
            child = influence(child,belief)
            new_population.append(child)

        population = new_population
        gen += 1

    # finished due to time limit
    elapsed = time - start_time
    print("\nCultural Algorithm Results(1):")
    print(f"\nBest solution found after time limit:")
    print(f"Number of Queens : {n}")
    print(f"Time taken : {elapsed:.6f} seconds")

    return belief['best_solution']

