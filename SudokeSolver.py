import time
start_time = time.perf_counter()

from collections import deque

def get_related_cells():
    related = {}
    for row in range(9):
        for col in range(9):
            related_cells = set()
            # Same row
            for c in range(9):
                if c != col:
                    related_cells.add((row, c))
            # Same column
            for r in range(9):
                if r != row:
                    related_cells.add((r, col))
            # Same 3x3 box
            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    if r != row or c != col:
                        related_cells.add((r, c))
            related[(row, col)] = list(related_cells)
    return related

def is_valid(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False
    # Check column
    for r in range(9):
        if grid[r][col] == num:
            return False
    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False
    return True

def ac3(grid, possible_values, related):
    queue = deque(possible_values.keys())
    while queue:
        cell = queue.popleft()
        if cell not in possible_values:
            continue
        row, col = cell
        for rc in related[cell]:
            if rc not in possible_values:
                rc_val = grid[rc[0]][rc[1]]
                if cell not in possible_values:
                    break  
                if rc_val in possible_values[cell]:
                    possible_values[cell].remove(rc_val)
                    if not possible_values[cell]:
                        return False
                    
                    if len(possible_values[cell]) == 1:
                        val = possible_values[cell].pop()
                        if not is_valid(grid, row, col, val):
                            return False
                        grid[row][col] = val
                        del possible_values[cell]
                        for adj in related[cell]:
                            if adj in possible_values and adj not in queue:
                                queue.append(adj)
                        break 
    return True

def backtrack(grid, possible_values, related):
    if not possible_values:
        return grid

    # MRV heuristic
    cell = min(possible_values.keys(), key=lambda k: len(possible_values[k]))
    row, col = cell

    for value in list(possible_values[cell]):
        if not is_valid(grid, row, col, value):
            continue  # Skip invalid assignments immediately

        new_grid = [row_copy.copy() for row_copy in grid]
        new_possible = {k: v.copy() for k, v in possible_values.items()}

        new_grid[row][col] = value
        del new_possible[cell]

        # Propagate constraints with AC-3
        ac3_success = ac3(new_grid, new_possible, related)
        if not ac3_success:
            continue

        # Recursive backtracking
        result = backtrack(new_grid, new_possible, related)
        if result is not None:
            return result

    return None

def solve_sudoku(grid):
    related = get_related_cells()
    possible_values = {}
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                possible_values[(row, col)] = set(range(1, 10))


    if not ac3(grid, possible_values, related):
        return None

    return backtrack(grid, possible_values, related)

if __name__ == "__main__":
    puzzle = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,3,0,8,5],
    [0,0,1,0,2,0,0,0,0],
    [0,0,0,5,0,7,0,0,0],
    [0,0,4,0,0,0,1,0,0],
    [0,9,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,0,7,3],
    [0,0,2,0,1,0,0,0,0],
    [0,0,0,0,4,0,0,0,9]
]
    solution = solve_sudoku(puzzle)
    if solution:
        for row in solution:
            print(row)
    else:
        print("No solution exists")

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")