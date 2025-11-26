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
        
        if nodo_actual == fin:
            break
        
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
    
    return camino, distancias[fin], distancias

def visualizar_resultado(grafo, camino, distancia_total, inicio, fin, todas_distancias):
    """Visualiza el resultado del algoritmo de Dijkstra"""
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Dibujar todas las aristas
    nx.draw_networkx_edges(G, posiciones, edge_color='gray', 
                          width=2, alpha=0.3, ax=ax)
    
    # Resaltar el camino óptimo
    aristas_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
    nx.draw_networkx_edges(G, posiciones, edgelist=aristas_camino,
                          width=6, edge_color='green', ax=ax, alpha=0.8)
    
    # Dibujar etiquetas de peso en las aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels, 
                                font_size=9, ax=ax)
    
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
                          node_size=1000, ax=ax, edgecolors='black', linewidths=2)
    nx.draw_networkx_labels(G, posiciones, font_size=14,
                           font_weight='bold', ax=ax)
    
    # Mostrar distancias desde el origen
    distancias_texto = {nodo: f"{dist:.1f}" if dist != float('inf') else "∞"
                       for nodo, dist in todas_distancias.items()}
    
    pos_distancias = {nodo: (pos[0], pos[1] - 0.5) 
                     for nodo, pos in posiciones.items()}
    
    nx.draw_networkx_labels(G, pos_distancias, distancias_texto,
                           font_size=10, font_color='red', ax=ax)
    
    # Título
    ax.set_title(f'Camino Óptimo de {inicio} a {fin}\n'
               f'Ruta: {" → ".join(camino)}\n'
               f'Distancia Total: {distancia_total:.2f} km',
               fontsize=18, fontweight='bold', color='darkgreen', pad=20)
    
    # Leyenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', 
                  markerfacecolor='lightgreen', markersize=12, 
                  label=f'Nodo Inicio ({inicio})', markeredgecolor='black', markeredgewidth=2),
        plt.Line2D([0], [0], marker='o', color='w',
                  markerfacecolor='lightcoral', markersize=12,
                  label=f'Nodo Destino ({fin})', markeredgecolor='black', markeredgewidth=2),
        plt.Line2D([0], [0], marker='o', color='w',
                  markerfacecolor='gold', markersize=12,
                  label='Nodos en el Camino', markeredgecolor='black', markeredgewidth=2),
        plt.Line2D([0], [0], color='green', linewidth=4,
                  label='Camino Óptimo'),
        plt.Line2D([0], [0], marker='o', color='w',
                  markerfacecolor='lightgray', markersize=12,
                  label='Otros Nodos', markeredgecolor='black', markeredgewidth=2)
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=12, frameon=True, shadow=True)
    
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 7)
    ax.axis('off')
    plt.tight_layout()
    
    return fig

def main():
    print("=" * 70)
    print(" " * 15 + "ALGORITMO DE DIJKSTRA")
    print(" " * 20 + "(Versión Simple)")
    print("=" * 70)
    print("\nGrafo de 15 nodos: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ")
    print("\nIngrese el nodo de inicio: ", end="")
    inicio = input().strip().upper()
    
    print("Ingrese el nodo de destino: ", end="")
    fin = input().strip().upper()
    
    if inicio not in grafo or fin not in grafo:
        print("\n❌ Error: Uno o ambos nodos no existen en el grafo.")
        return
    
    print(f"\n🔍 Calculando ruta más corta de {inicio} a {fin}...\n")
    
    # Ejecutar Dijkstra
    camino, distancia, todas_distancias = dijkstra(grafo, inicio, fin)
    
    if distancia == float('inf'):
        print(f"❌ No existe un camino entre {inicio} y {fin}")
        return
    
    # Mostrar resultado en consola
    print("=" * 70)
    print(" " * 25 + "RESULTADO")
    print("=" * 70)
    print(f"\n📍 Camino óptimo: {' → '.join(camino)}")
    print(f"📏 Distancia total: {distancia:.2f} km")
    print(f"🔢 Número de nodos en el camino: {len(camino)}")
    print(f"🔢 Número de saltos: {len(camino) - 1}")
    
    # Mostrar distancias intermedias
    print("\n📊 Distancias intermedias:")
    distancia_acumulada = 0
    for i in range(len(camino) - 1):
        nodo_actual = camino[i]
        nodo_siguiente = camino[i + 1]
        
        # Buscar el peso de la arista
        peso = None
        for vecino, p in grafo[nodo_actual]:
            if vecino == nodo_siguiente:
                peso = p
                break
        
        distancia_acumulada += peso
        print(f"   {nodo_actual} → {nodo_siguiente}: {peso:.2f} km "
              f"(Acumulado: {distancia_acumulada:.2f} km)")
    
    print("\n" + "=" * 70)
    
    # Mostrar todas las distancias desde el origen
    print(f"\n📏 Distancias desde {inicio} a todos los nodos:")
    distancias_ordenadas = sorted(todas_distancias.items(), key=lambda x: x[1])
    for nodo, dist in distancias_ordenadas:
        if dist != float('inf'):
            print(f"   {inicio} → {nodo}: {dist:.2f} km")
        else:
            print(f"   {inicio} → {nodo}: ∞ (No alcanzable)")
    
    print("\n" + "=" * 70)
    print("\n📊 Generando visualización...")
    
    # Visualizar resultado
    fig = visualizar_resultado(grafo, camino, distancia, inicio, fin, todas_distancias)
    
    print("✅ Visualización lista. Cierra la ventana para terminar.")
    plt.show()

if __name__ == "__main__":
    main()