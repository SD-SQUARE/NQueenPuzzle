import time

def isSafe(mat, row, col):
    n = len(mat)

    # Check this col on upper side
    for i in range(row):
        if mat[i][col]:
            return 0

    # Check upper diagonal on left side
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if mat[i][j]:
            return 0
        i -= 1
        j -= 1

    # Check upper diagonal on right side
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if mat[i][j]:
            return 0
        i -= 1
        j += 1

    return 1


# Recursive function to place queens
def placeQueens(row, mat, result, times, record_times, t0):
    n = len(mat)

    # base case: If all queens are placed
    if row == n:
        # store current solution
        ans = []
        for i in range(n):
            for j in range(n):
                if mat[i][j]:
                    ans.append(j + 1)    # 1-indexed like your old code
        result.append(ans)

        if record_times:
            times.append(time.perf_counter() - t0)

        return

    # Try placing queen in all columns for this row
    for col in range(n):
        # Check if the queen can be placed
        if isSafe(mat, row, col):
            mat[row][col] = 1
            placeQueens(row + 1, mat, result, times, record_times, t0)
            # backtrack
            mat[row][col] = 0


# Function to find all solutions
def backtrackingAlgo(n, record_times=False, start_time=None):
    """
    If record_times == False  -> returns [solutions]
    If record_times == True   -> returns (solutions, times)
        where times[i] is the time (sec) when solution i was found
    """
    # Initialize the board
    mat = [[0] * n for _ in range(n)]
    result = []
    times = []

    t0 = start_time if start_time is not None else time.perf_counter()

    # Place queens
    placeQueens(0, mat, result, times, record_times, t0)

    if record_times:
        return result, times
    return result
