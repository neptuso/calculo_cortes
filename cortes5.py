from ortools.sat.python import cp_model

def cutting_stock_optimization(rod_length_mm, piece_lengths_mm, piece_quantities):
    model = cp_model.CpModel()

    # Variables
    num_rods = sum(piece_quantities)  # Número máximo de barras posibles
    x = {}  # x[i, j] = 1 si la barra i contiene la pieza j

    for i in range(num_rods):
        for j in range(len(piece_lengths_mm)):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Restricción: la suma de las longitudes de las piezas en cada barra no puede exceder la longitud de la barra
    for i in range(num_rods):
        model.Add(sum(x[i, j] * piece_lengths_mm[j] for j in range(len(piece_lengths_mm))) <= rod_length_mm)

    # Restricción: cumplir con las cantidades requeridas para cada tipo de pieza
    for j in range(len(piece_lengths_mm)):
        model.Add(sum(x[i, j] for i in range(num_rods)) == piece_quantities[j])

    # Minimizar el número de barras usadas
    rods_used = [model.NewBoolVar(f'rods_used[{i}]') for i in range(num_rods)]
    for i in range(num_rods):
        model.AddMaxEquality(rods_used[i], [x[i, j] for j in range(len(piece_lengths_mm))])

    model.Minimize(sum(rods_used))

    # Resolver el modelo
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    total_waste = 0  # Variable para acumular el desperdicio total
    total_bars_used = 0  # Contador para el número total de barras utilizadas

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Número mínimo de barras utilizadas: {int(solver.ObjectiveValue())}')
        for i in range(num_rods):
            if solver.Value(rods_used[i]) == 1:
                total_bars_used += 1
                print(f'\nBarra {i + 1} contiene las piezas:')
                total_length = 0
                for j in range(len(piece_lengths_mm)):
                    if solver.Value(x[i, j]) == 1:
                        print(f' - {piece_lengths_mm[j] / 1000} metros (cantidad: 1)')
                        total_length += piece_lengths_mm[j]
                waste = rod_length_mm - total_length
                total_waste += waste
                print(f' - Longitud total usada: {total_length / 1000} metros')
                print(f' - Espacio desperdiciado: {waste / 1000} metros')
        
        # Imprimir el resumen final
        print(f'\n--- Resumen final ---')
        print(f'Total de barras utilizadas: {total_bars_used}')
        print(f'Desperdicio total: {total_waste / 1000} metros')
    else:
        print('No se encontró una solución óptima.')

# Datos de entrada (convertidos a milímetros)
rod_length_mm = 6000  # Longitud de las barras de hierro en milímetros
piece_lengths_mm = [3100, 850, 1200, 4200, 3600, 700]  # Longitudes de las piezas en milímetros
piece_quantities = [2, 2, 2, 2, 2, 2]  # Cantidades necesarias para cada longitud

cutting_stock_optimization(rod_length_mm, piece_lengths_mm, piece_quantities)
