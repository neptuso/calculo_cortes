from ortools.linear_solver import pywraplp

def cutting_stock_optimization(rod_length, piece_lengths, piece_quantities):
    # Create the solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    if not solver:
        return None

    # Variables: x[i] represents how many full rods are used for the i-th combination of pieces
    piece_count = len(piece_lengths)
    x = [solver.IntVar(0, solver.infinity(), f'x[{i}]') for i in range(piece_count)]
    
    # Constraints: Ensure that we meet the required quantity of each piece.
    for i in range(piece_count):
        solver.Add(sum(x[j] for j in range(piece_count)) >= piece_quantities[i])

    # Objective: Minimize the number of rods used.
    solver.Minimize(solver.Sum(x))

    # Solve the problem.
    status = solver.Solve()

    # Check the results.
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal solution found using {solver.Objective().Value()} rods.')
        for i in range(piece_count):
            print(f'Use {x[i].solution_value()} pieces of {piece_lengths[i]} meters.')
    else:
        print('No optimal solution found.')

# Define the inputs
rod_length = 6.0  # 6 meters long iron rods
piece_lengths = [3.1, 0.85, 1.2, 4.2, 3.6, 0.7, 1.5]  # Lengths of pieces in meters
piece_quantities = [2, 2, 2, 2, 2, 2, 15]  # Quantities needed for each length

cutting_stock_optimization(rod_length, piece_lengths, piece_quantities)
