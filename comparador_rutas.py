import matplotlib.pyplot as plt
import networkx as nx
import heapq

# Definir el grafo con las conexiones y distancias
grafo = {
    'A': [('B', 0.9), ('D', 1.1)],
    'B': [('A', 0.9), ('C', 1.5)],
    'C': [('B', 1.5), ('L', 2.2)],
    'D': [('A', 1.1), ('F', 1.2)],
    'E': [('G', 1.1)],
    'F': [('D', 1.2), ('G', 1.1), ('H', 1.3)],
    'G': [('E', 1.1), ('F', 1.1), ('I', 0.8), ('K', 3.5)],
    'H': [('F', 1.3), ('I', 1.5)],
    'I': [('G', 0.8), ('H', 1.5), ('J', 1.3)],
    'J': [('I', 1.3), ('Ñ', 2.1)],
    'K': [('G', 3.5), ('M', 1.1), ('Ñ', 1.4)],
    'L': [('N', 3.1), ('C', 2.2)],
    'M': [('K', 1.1), ('N', 1.1)],
    'N': [('M', 1.1), ('L', 3.1)],
    'Ñ': [('J', 2.1), ('K', 1.4)]
}

# Posiciones aproximadas de los nodos
posiciones = {
    'A': (0, 5),
    'B': (1.5, 6),
    'C': (3.5, 6),
    'D': (1.5, 4),
    'E': (3.5, 3.5),
    'F': (2, 2.5),
    'G': (3.5, 2.5),
    'H': (1, 1),
    'I': (3.5, 1),
    'J': (5.5, 0.5),
    'K': (8, 2.5),
    'L': (6, 5.5),
    'M': (9, 4.5),
    'N': (10, 6),
    'Ñ': (9, 1)
}

def dijkstra(grafo, inicio, fin):
    """Implementa el algoritmo de Dijkstra"""
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    previos = {nodo: None for nodo in grafo}
    visitados = set()
    
    cola = [(0, inicio)]
    
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        for vecino, peso in grafo[nodo_actual]:
            if vecino not in visitados:
                nueva_distancia = distancia_actual + peso
                
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))
    
    # Construir el camino
    camino = []
    nodo = fin
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = previos[nodo]
    
    return camino, distancias[fin]

def comparar_rutas(rutas_info):
    """Compara múltiples rutas en una sola visualización"""
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)
    
    num_rutas = len(rutas_info)
    fig, axes = plt.subplots(1, num_rutas, figsize=(8 * num_rutas, 8))
    
    if num_rutas == 1:
        axes = [axes]
    
    colores_caminos = ['green', 'blue', 'red', 'purple', 'orange', 'brown']
    
    for idx, (ax, info) in enumerate(zip(axes, rutas_info)):
        inicio, fin, camino, distancia = info
        
        # Dibujar todas las aristas
        nx.draw_networkx_edges(G, posiciones, edge_color='gray', 
                              width=2, alpha=0.3, ax=ax)
        
        # Resaltar el camino
        aristas_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
        color_camino = colores_caminos[idx % len(colores_caminos)]
        nx.draw_networkx_edges(G, posiciones, edgelist=aristas_camino,
                              width=5, edge_color=color_camino, ax=ax, alpha=0.8)
        
        # Dibujar etiquetas de peso
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, posiciones, edge_labels, 
                                    font_size=8, ax=ax)
        
        # Colores de los nodos
        colores = []
        for nodo in G.nodes():
            if nodo in camino:
                if nodo == inicio:
                    colores.append('lightgreen')
                elif nodo == fin:
                    colores.append('lightcoral')
                else:
                    colores.append('gold')
            else:
                colores.append('lightgray')
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, posiciones, node_color=colores,
                              node_size=800, ax=ax, edgecolors='black', linewidths=2)
        nx.draw_networkx_labels(G, posiciones, font_size=12,
                               font_weight='bold', ax=ax)
        
        # Título
        ax.set_title(f'Ruta {idx + 1}: {inicio} → {fin}\n'
                   f'{" → ".join(camino)}\n'
                   f'Distancia: {distancia:.2f} km',
                   fontsize=12, fontweight='bold')
        
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 7)
        ax.axis('off')
    
    plt.tight_layout()
    return fig

def main():
    print("=" * 70)
    print(" " * 15 + "COMPARADOR DE RUTAS - DIJKSTRA")
    print("=" * 70)
    print("\nEste programa permite comparar múltiples rutas simultáneamente")
    print("\nNodos disponibles: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ")
    
    print("\n¿Cuántas rutas deseas comparar? (1-6): ", end="")
    num_rutas = int(input().strip())
    
    if num_rutas < 1 or num_rutas > 6:
        print("❌ Número de rutas inválido. Debe ser entre 1 y 6.")
        return
    
    rutas_info = []
    
    for i in range(num_rutas):
        print(f"\n--- Ruta {i + 1} ---")
        print("Nodo de inicio: ", end="")
        inicio = input().strip().upper()
        
        print("Nodo de destino: ", end="")
        fin = input().strip().upper()
        
        if inicio not in grafo or fin not in grafo:
            print(f"❌ Error: Nodos inválidos para la ruta {i + 1}")
            return
        
        camino, distancia = dijkstra(grafo, inicio, fin)
        
        if distancia == float('inf'):
            print(f"❌ No existe un camino entre {inicio} y {fin}")
            return
        
        rutas_info.append((inicio, fin, camino, distancia))
        print(f"✅ Ruta calculada: {' → '.join(camino)} ({distancia:.2f} km)")
    
    # Mostrar tabla comparativa
    print("\n" + "=" * 70)
    print(" " * 25 + "COMPARACIÓN DE RUTAS")
    print("=" * 70)
    print(f"\n{'Ruta':<8} {'Origen':<8} {'Destino':<10} {'Distancia':<12} {'Nº Saltos':<10}")
    print("-" * 70)
    
    for i, (inicio, fin, camino, distancia) in enumerate(rutas_info, 1):
        print(f"Ruta {i:<3} {inicio:<8} {fin:<10} {distancia:.2f} km{'':<6} {len(camino)-1:<10}")
    
    print("=" * 70)
    
    # Encontrar la ruta más corta
    ruta_mas_corta = min(enumerate(rutas_info, 1), key=lambda x: x[1][3])
    print(f"\n🏆 La ruta más corta es la Ruta {ruta_mas_corta[0]}: "
          f"{ruta_mas_corta[1][0]} → {ruta_mas_corta[1][1]} "
          f"({ruta_mas_corta[1][3]:.2f} km)")
    
    print("\n📊 Generando comparación visual...")
    
    # Visualizar comparación
    fig = comparar_rutas(rutas_info)
    
    print("✅ Visualización lista. Cierra la ventana para terminar.")
    plt.show()

if __name__ == "__main__":
    main()