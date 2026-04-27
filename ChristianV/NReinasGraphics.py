from typing import List, Set

# ---------------- Utilidades de impresión ----------------

def pausa():
    try:
        input("[ENTER] para continuar...")
    except EOFError:
        pass

def imprimir_tablero_marcado(tablero: List[int], analizadas_por_fila: List[Set[int]], n: int, titulo: str = ""):
    """
    Imprime el tablero con:
      - '♛' = reina colocada
      - '×' = casilla analizada (probada)
      - '.' = sin analizar
    """
    if titulo:
        print("\n" + titulo)

    for fila in range(n):
        linea = []
        for col in range(n):
            if tablero[fila] == col:
                linea.append("♛")
            elif col in analizadas_por_fila[fila]:
                linea.append("×")
            else:
                linea.append(".")
        print(" ".join(linea))
    pausa()

def imprimir_tablero_simple(solucion: List[int]):
    n = len(solucion)
    print("\nPrimera solución (vista 2D):")
    for fila in range(n):
        linea = []
        for col in range(n):
            linea.append("♛" if solucion[fila] == col else ".")
        print(" ".join(linea))

# ---------------- Chequeo de seguridad ----------------

def es_seguro(tablero: List[int], fila: int, col: int) -> bool:
    for i in range(fila):
        if tablero[i] == col:                      # misma columna
            return False
        if tablero[i] - i == col - fila:           # diagonal principal
            return False
        if tablero[i] + i == col + fila:           # diagonal secundaria
            return False
    return True

# ---------------- Visualización 3D de la primera solución ----------------

def visualizar_3d(solucion: List[int]):
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    except Exception as e:
        print("No se pudo abrir la vista 3D (matplotlib no disponible).", e)
        return

    n = len(solucion)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    dx = dy = 0.95
    xs, ys, zs, dxs, dys, dzs, colors = [], [], [], [], [], [], []

    # Tablero (damero) como barras bajitas
    for i in range(n):
        for j in range(n):
            xs.append(j)
            ys.append(n - 1 - i)   # invertir Y para ver fila 0 abajo
            zs.append(0.0)
            dxs.append(dx)
            dys.append(dy)
            dzs.append(0.1)
            shade = 0.85 if (i + j) % 2 == 0 else 0.35
            colors.append((shade, shade, shade))

    ax.bar3d(xs, ys, zs, dxs, dys, dzs, shade=True, color=colors, edgecolor="k", linewidth=0.2)

    # Reinas como torres
    qxs, qys, qzs, qdxs, qdys, qdzs = [], [], [], [], [], []
    for fila, col in enumerate(solucion):
        qxs.append(col + 0.1)
        qys.append(n - 1 - fila + 0.1)
        qzs.append(0.1)
        qdxs.append(0.75)
        qdys.append(0.75)
        qdzs.append(1.2)

    ax.bar3d(qxs, qys, qzs, qdxs, qdys, qdzs, shade=True, edgecolor="k", linewidth=0.6)

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_zlim(0, 1.5)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_zticks([])
    ax.set_xlabel("Columnas")
    ax.set_ylabel("Filas")
    ax.set_title(f"Primera solución 3D para N = {n}")
    ax.view_init(elev=25, azim=45)

    print("Mostrando la primera solución en 3D (cierra la ventana para continuar).")
    plt.tight_layout()
    plt.show()

# ---------------- Backtracking instrumentado ----------------

def resolver_n_reinas(tablero: List[int],
                       fila: int,
                       n: int,
                       soluciones: List[List[int]],
                       analizadas_por_fila: List[Set[int]],
                       retrocesos_impresos: List[int],     # mutable contador [k]
                       primera_3d_mostrada: List[bool]):    # flag [bool]
    """
    - Imprime exactamente 3 instantáneas 'ANTES DEL RETROCESO' (si hay al menos 3).
    - No imprime cada intento; solo esos 3 y la primera solución.
    """
    if fila == n:
        # Solución completa
        soluciones.append(tablero[:])

        # Solo mostrar la PRIMERA solución (2D + 3D)
        if len(soluciones) == 1:
            imprimir_tablero_simple(tablero)
            visualizar_3d(tablero[:])
        return

    for col in range(n):
        # Registrar que esta casilla (fila, col) fue ANALIZADA en esta rama
        analizadas_por_fila[fila].add(col)

        if es_seguro(tablero, fila, col):
            # Colocar reina
            tablero[fila] = col

            # Limpiar marcas de filas más profundas antes de descender (que no “hereden” análisis viejos)
            for f in range(fila + 1, n):
                analizadas_por_fila[f].clear()

            # Avanzar
            resolver_n_reinas(tablero, fila + 1, n, soluciones,
                              analizadas_por_fila, retrocesos_impresos, primera_3d_mostrada)

            # ---- Aquí se activa el RETROCESO sobre (fila, col) ----
            if retrocesos_impresos[0] < 3:
                titulo = f"ANTES DEL RETROCESO #{retrocesos_impresos[0] + 1}: deshacer fila {fila}, col {col}"
                imprimir_tablero_marcado(tablero, analizadas_por_fila, n, titulo)
                retrocesos_impresos[0] += 1

            # Deshacer reina (retroceso)
            tablero[fila] = -1

    # Si ninguna columna sirve, el retroceso real sucederá en la fila anterior.

def n_reinas_8():
    n = 8
    tablero = [-1] * n
    soluciones: List[List[int]] = []
    analizadas_por_fila: List[Set[int]] = [set() for _ in range(n)]
    retrocesos_impresos = [0]
    primera_3d_mostrada = [False]

    print("Ejecutando 8-Reinas.\nSe mostrarán 3 estados 'ANTES DEL RETROCESO' con ENTER para continuar.")
    pausa()

    resolver_n_reinas(tablero, 0, n, soluciones, analizadas_por_fila,
                      retrocesos_impresos, primera_3d_mostrada)

    print(f"\nTotal de soluciones encontradas: {len(soluciones)}")

if __name__ == "__main__":
    n_reinas_8()