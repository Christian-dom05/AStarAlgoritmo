from typing import List

all_solutions = []
N_QUEENS = 8

# ---------------- Visualización 3D Adaptada ----------------

def visualizar_3d(board_matrix: List[List[int]]):
    """
    Toma una matriz 2D (donde 1 representa una reina) y la grafica en 3D.
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    except ImportError:
        print("No se pudo abrir la vista 3D. Asegúrate de tener matplotlib instalado.")
        return

    n = len(board_matrix)
    fig = plt.figure(figsize=(8, 8))
    # Creamos el entorno 3D que permite rotación con el ratón
    ax = fig.add_subplot(111, projection='3d')

    dx = dy = 0.95
    xs, ys, zs, dxs, dys, dzs, colors = [], [], [], [], [], [], []

    # 1. Dibujar el Tablero (damero)
    for i in range(n):
        for j in range(n):
            xs.append(j)
            ys.append(n - 1 - i)   # Invertimos Y para que la fila 0 quede abajo
            zs.append(0.0)
            dxs.append(dx)
            dys.append(dy)
            dzs.append(0.1)
            # Alternar colores para las casillas
            shade = 0.85 if (i + j) % 2 == 0 else 0.35
            colors.append((shade, shade, shade))

    ax.bar3d(xs, ys, zs, dxs, dys, dzs, shade=True, color=colors, edgecolor="k", linewidth=0.2)

    # 2. Dibujar las Reinas como rectángulos 3D (torres)
    qxs, qys, qzs, qdxs, qdys, qdzs = [], [], [], [], [], []
    
    # Recorremos la matriz 2D buscando los '1'
    for fila in range(n):
        for col in range(n):
            if board_matrix[fila][col] == 1:
                qxs.append(col + 0.1)
                qys.append(n - 1 - fila + 0.1)
                qzs.append(0.1)
                qdxs.append(0.75)
                qdys.append(0.75)
                qdzs.append(1.2) # Altura de la reina

    # Color dorado para distinguir fácilmente a las reinas
    ax.bar3d(qxs, qys, qzs, qdxs, qdys, qdzs, shade=True, color="gold", edgecolor="k", linewidth=0.6)

    # Configuraciones de la cámara y límites
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_zlim(0, 1.5)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_zticks([])
    ax.set_xlabel("Columnas")
    ax.set_ylabel("Filas")
    ax.set_title(f"Primera Solución 3D - Problema de {n} Reinas")
    
    # Ángulo de vista inicial
    ax.view_init(elev=25, azim=45)

    print("\nMostrando la primera solución en 3D...")
    print("Puedes hacer clic y arrastrar para mover el tablero en todas las coordenadas.")
    print("(Cierra la ventana gráfica para finalizar el programa).")
    plt.tight_layout()
    plt.show()

# ---------------- Algoritmo Backtracking ----------------

def solve_8_queens():
    # Inicializar tablero vacío como una matriz de 8x8
    board = [[0 for _ in range(N_QUEENS)] for _ in range(N_QUEENS)]
    place_queen(board, 0)
    return all_solutions

def place_queen(board, row):
    # Si la fila es igual a 8, se ha colocado la reina en la fila 8.
    if row == N_QUEENS:
        # Guardar la solución completa.
        # Copiamos el tablero actual para no alterarlo en futuras llamadas.
        solution = [row[:] for row in board]
        all_solutions.append(solution)
        return

    # Para cada columna en 0 a n-1
    for col in range(N_QUEENS):
        # Si es seguro colocar la reina en (fila, columna)
        if is_safe(board, row, col):
            # Colocar reina
            board[row][col] = 1
            # Llamar recursivamente colocarReina(fila + 1)
            place_queen(board, row + 1)
            # Quitar reina (backtrack)
            board[row][col] = 0

def is_safe(board, row, col):
    # Verificar misma columna en filas anteriores.
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Verificar diagonal principal (arriba-izquierda).
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if board[i][j] == 1:
            return False

    # Verificar diagonal secundaria (arriba-derecha).
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, N_QUEENS)):
        if board[i][j] == 1:
            return False

    # Si no hay conflictos, retornar verdadero.
    return True

# ---------------- Ejecución ----------------

if __name__ == "__main__":
    solutions = solve_8_queens()

    print(f"Total de soluciones encontradas: {len(solutions)}")
    
    if len(solutions) > 0:
        print("\nPrimera solución encontrada (matriz):")
        for row in solutions[0]:
            print(row)
            
        # Llamamos a la función gráfica pasando la primera solución (que es una matriz 2D)
        visualizar_3d(solutions[0])
    else:
        print("No se encontraron soluciones.")