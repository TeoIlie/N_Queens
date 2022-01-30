"""
CISC 352
Assignment 1
Code by: 
    Jean Charle Yaacoub, 20094416
    Zack Urbaniak, 20124496
    Renee Tibando, 20113399
    Teodor Ilie, 20100698
    Alice Petrov 20111076

Problem: Placing n-queens on a n x n chessboard such that no two queens threaten each other.

Heuristic method:
    Minimum-conflicts - focuses on the piece with the most conflicts and moves it to a place in that same column where
    conflicts are the smallest.

Search method:
    Iterative repair - starts with all queens on the board and then counts the conflicts then uses heuristics to
    determine how to improve placement of queens.

States:
    Start- Greedy algorithm.
    Goal - No two queens share the same row, column or diagonal
"""

import random
import math
import time

def queens_conflicts(row, indexPos, state):
    """
    Returns how many conflicts does a queens has with the other queens on the board.

    :param row: is the queen's row value
    :param indexpos: column value -1
    :param state: remaining board setup
    :return: number of conflicts
    """
    total_conflicts = 0

    for i in range(len(state)):
        if indexPos != i: # checks cols -> if same -> skip (impossible by definition of the state)
            row_2 = state[i]

            # the following two are mutually exclusive (can't be both row and diagonal conflict)
            if row == row_2: # checks row
                total_conflicts += 1
            elif abs(row - row_2) == abs(indexPos - i): # checks diagonal 
                total_conflicts += 1

    return total_conflicts

def initial_board(n):
    """
    :param n: initial board size
    """
    start_board = [random.randint(1, n)]

    # for each column, generate a list of all the conflict values
    for col in range(1, n):
        conflicts = [None for x in range(n)]

        for row in range(1, n+1):
            conflicts[row-1] = queens_conflicts(row, col, start_board)

        # the new position will be the spot with the least conflicts
        minval = min(conflicts)
        mincols = [i for i, x in enumerate(conflicts) if x == minval] # the cols for those values

        # choosing one of the cols to be the pos
        start_board.append(random.choice(mincols)+1)
    return start_board

def new_board(n):
    """
    :param n: initial board size
    """

    board = list(range(1, n+1)) 

    if (n%2 == 0 and n%6 != 0):
        for i in range(1, int(n/2) + 1):
            y = n - (2*i + n/2 - 3%n) - 1
            if (y < 0):
                y += n
            board[i-1] = (2*i + n/2 - 3%n) % n
            board[n-i] = y   
        return board

    elif (n%2 == 0 and (n-2)%6 != 0):
        for i in range(1, int(n/2) + 1):
            board[i-1] =  2*i-1
            board[int(n/2) + i - 1] =  2*i - 2
        return board 

    else:
        for i in range(1, int((n-1)/2) + 1):
            board[i-1] =  2*i-1
            board[int(n/2) + i - 1] =  2*i - 2
        board[n-1] = n-1

        for i in range(1, int(n/2) + 1):
            y = n - (2*i + n/2 - 3%n)-1
            if (y < 0):
                y += n
            board[i-1] = (2*i + n/2 - 3%n) % n
            board[n-i] = y
        return board

def is_solution(state):
    """
    checks a solution for correctness.
    :param lst: list representing row position of the queens.
    :return: boolean True if it is correct, false otherwise
    """

    # ensure lst is within allowed bounds
    if len(state) <= 3 or len(state) > 10000000:
        return False

    for i in range(len(state)):  # loop through q_index
        # item is alone in its column, so check it is alone in its row and on its diagonals
        row = state[i]

        for j in range(i+1, len(state)-1): # Dont need to check elements behind it (that would just be a repeated check)
            row_2 = state[j]

            # checks rows, and diagonal:
            if (row_2 == row or 
                abs(row - row_2) == abs(i - j)):
                return False
    return True

def solve(n):
    """
    This function takes in a number and solves the N-Queens problem for that number of queens on an nxn chessboard.
    :param n: the number of queens
    :return: List of integers where each entry corresponds to the row of a queen (starting at 1 not zero)
            Note: The index position of the queen represents their column.
    """
    row_opt = list(range(1, n+1)) # possible row options for a queen

    # Starting state has no two queens sharing same row or col.
    if n <= 128:
        current = initial_board(n)
    else:
        current = random.sample(row_opt, n)

    num_steps = 0
    max_steps = (2.2*n*math.log(n,10)) / 4

    # N-Queens always has a solution (it is NP-COMPLETE)
    while True:
        # Randomly Selecting a queen:
        randomQ_i = random.randint(0, n-1)

        # Finding all conflicts for possible new row positions for that queen.
        min_value = n   # Max possible value is n-1
        new_row = -1    # ^egro this is Garenteed to be overwritten

        for row in range(1, n+1):
            conflicts = queens_conflicts(row, randomQ_i, current)
            if conflicts < min_value:
                min_value = conflicts
                new_row = row
        
        current[randomQ_i] = new_row
        num_steps += 1

        # Checks for solution iff the move resulted in a 0 conflict score for that queen
        if min_value == 0 and is_solution(current):
            return current
        
        # Restarting if exceeded max steps:
        if num_steps > max_steps:
            num_steps = 0
            current = new_board(n) # restarting

if __name__ == "__main__":
    num_exe = 1
    test_range = [1000] #list(range(128, 129, 50)) # list of n values to test

    print('Testing n =', test_range)
    print(num_exe, 'executions per n')

    print('{:^10} | {:^15}'.format('N', 'AVG EXE TIME'))
    print('-'*10, '|', '-'*15)
    
    for n in test_range:
        average_exe = 0
        total_steps = 0
        max_steps = 0

        # print('\n{} for {} exe:'.format(n, num_exe))
        for i in range(num_exe):
            start = time.time()

            state = solve(n)
            exe_time = time.time() - start

            average_exe += exe_time

        print('{:^10} | {:^15.3}'.format(n, average_exe/num_exe))
