import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import defaultdict
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

# Posiciones aproximadas de los nodos basadas en la imagen
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

class DijkstraAnimado:
    def __init__(self, grafo, inicio, fin):
        self.grafo = grafo
        self.inicio = inicio
        self.fin = fin
        self.pasos = []
        
        # Ejecutar Dijkstra y guardar los pasos
        self.ejecutar_dijkstra()
        
    def ejecutar_dijkstra(self):
        """Ejecuta el algoritmo de Dijkstra y guarda cada paso para la animación"""
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[self.inicio] = 0
        previos = {nodo: None for nodo in self.grafo}
        visitados = set()
        
        # Cola de prioridad: (distancia, nodo)
        cola = [(0, self.inicio)]
        
        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)
            
            if nodo_actual in visitados:
                continue
            
            visitados.add(nodo_actual)
            
            # Guardar el estado actual
            self.pasos.append({
                'nodo_actual': nodo_actual,
                'visitados': visitados.copy(),
                'distancias': distancias.copy(),
                'previos': previos.copy(),
                'cola': [n for _, n in cola]
            })
            
            # Explorar vecinos
            for vecino, peso in self.grafo[nodo_actual]:
                if vecino not in visitados:
                    nueva_distancia = distancia_actual + peso
                    
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        previos[vecino] = nodo_actual
                        heapq.heappush(cola, (nueva_distancia, vecino))
        
        # Construir el camino óptimo
        self.camino_optimo = []
        nodo = self.fin
        while nodo is not None:
            self.camino_optimo.insert(0, nodo)
            nodo = previos[nodo]
        
        self.distancia_total = distancias[self.fin]
        
    def animar(self):
        """Crea la animación del algoritmo"""
        # Crear el grafo de NetworkX para visualización
        G = nx.Graph()
        for nodo, vecinos in self.grafo.items():
            for vecino, peso in vecinos:
                G.add_edge(nodo, vecino, weight=peso)
        
        fig, ax = plt.subplots(figsize=(16, 10))
        
        def actualizar(frame):
            ax.clear()
            
            if frame < len(self.pasos):
                paso = self.pasos[frame]
                nodo_actual = paso['nodo_actual']
                visitados = paso['visitados']
                distancias = paso['distancias']
                cola = paso['cola']
                
                # Título con información del paso actual
                ax.set_title(f'Algoritmo de Dijkstra - Paso {frame + 1}/{len(self.pasos)}\n'
                           f'Explorando: {nodo_actual} | '
                           f'Distancia desde {self.inicio}: {distancias[nodo_actual]:.1f} km',
                           fontsize=16, fontweight='bold')
            else:
                # Mostrar resultado final
                ax.set_title(f'Camino Óptimo de {self.inicio} a {self.fin}\n'
                           f'Distancia Total: {self.distancia_total:.1f} km\n'
                           f'Ruta: {" → ".join(self.camino_optimo)}',
                           fontsize=16, fontweight='bold', color='darkgreen')
                
                # Resaltar el camino óptimo
                aristas_camino = [(self.camino_optimo[i], self.camino_optimo[i+1]) 
                                 for i in range(len(self.camino_optimo)-1)]
                nx.draw_networkx_edges(G, posiciones, edgelist=aristas_camino,
                                      width=5, edge_color='green', ax=ax)
            
            # Dibujar todas las aristas
            nx.draw_networkx_edges(G, posiciones, edge_color='gray', 
                                  width=2, alpha=0.5, ax=ax)
            
            # Dibujar etiquetas de peso en las aristas
            edge_labels = nx.get_edge_attributes(G, 'weight')
            edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
            nx.draw_networkx_edge_labels(G, posiciones, edge_labels, 
                                        font_size=8, ax=ax)
            
            if frame < len(self.pasos):
                paso = self.pasos[frame]
                nodo_actual = paso['nodo_actual']
                visitados = paso['visitados']
                distancias = paso['distancias']
                cola = paso['cola']
                
                # Colores de los nodos
                colores = []
                for nodo in G.nodes():
                    if nodo == self.inicio:
                        colores.append('lightgreen')
                    elif nodo == self.fin:
                        colores.append('lightcoral')
                    elif nodo == nodo_actual:
                        colores.append('gold')
                    elif nodo in visitados:
                        colores.append('lightblue')
                    elif nodo in cola:
                        colores.append('lightyellow')
                    else:
                        colores.append('lightgray')
                
                # Dibujar nodos
                nx.draw_networkx_nodes(G, posiciones, node_color=colores,
                                      node_size=800, ax=ax)
                nx.draw_networkx_labels(G, posiciones, font_size=12,
                                       font_weight='bold', ax=ax)
                
                # Mostrar distancias calculadas
                distancias_texto = {nodo: f"{dist:.1f}" if dist != float('inf') else "∞"
                                   for nodo, dist in distancias.items()}
                
                # Posiciones para las etiquetas de distancia (ligeramente desplazadas)
                pos_distancias = {nodo: (pos[0], pos[1] - 0.4) 
                                 for nodo, pos in posiciones.items()}
                
                nx.draw_networkx_labels(G, pos_distancias, distancias_texto,
                                       font_size=9, font_color='red', ax=ax)
                
                # Leyenda
                legend_elements = [
                    plt.Line2D([0], [0], marker='o', color='w', 
                              markerfacecolor='lightgreen', markersize=10, 
                              label=f'Inicio ({self.inicio})'),
                    plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='lightcoral', markersize=10,
                              label=f'Destino ({self.fin})'),
                    plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='gold', markersize=10,
                              label='Nodo Actual'),
                    plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='lightblue', markersize=10,
                              label='Visitado'),
                    plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='lightyellow', markersize=10,
                              label='En Cola'),
                    plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='lightgray', markersize=10,
                              label='No Visitado')
                ]
                ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
            else:
                # Resultado final - solo mostrar camino óptimo
                colores = []
                for nodo in G.nodes():
                    if nodo in self.camino_optimo:
                        if nodo == self.inicio:
                            colores.append('lightgreen')
                        elif nodo == self.fin:
                            colores.append('lightcoral')
                        else:
                            colores.append('gold')
                    else:
                        colores.append('lightgray')
                
                nx.draw_networkx_nodes(G, posiciones, node_color=colores,
                                      node_size=800, ax=ax)
                nx.draw_networkx_labels(G, posiciones, font_size=12,
                                       font_weight='bold', ax=ax)
            
            ax.set_xlim(-1, 11)
            ax.set_ylim(-1, 7)
            ax.axis('off')
        
        # Crear animación
        frames_totales = len(self.pasos) + 5  # Pasos + frames extras para mostrar resultado
        anim = animation.FuncAnimation(fig, actualizar, frames=frames_totales,
                                      interval=1000, repeat=True)
        
        plt.tight_layout()
        return anim, fig

# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("ALGORITMO DE DIJKSTRA CON ANIMACIÓN")
    print("=" * 60)
    print("\nGrafo de 15 nodos: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ")
    print("\nIngrese el nodo de inicio (ej: A): ", end="")
    inicio = input().strip().upper()
    
    print("Ingrese el nodo de destino (ej: N): ", end="")
    fin = input().strip().upper()
    
    if inicio not in grafo or fin not in grafo:
        print("\n❌ Error: Uno o ambos nodos no existen en el grafo.")
        exit()
    
    print(f"\n🔍 Calculando ruta más corta de {inicio} a {fin}...\n")
    
    # Crear y ejecutar la animación
    dijkstra = DijkstraAnimado(grafo, inicio, fin)
    
    # Mostrar resultado en consola
    print("=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(f"📍 Camino óptimo: {' → '.join(dijkstra.camino_optimo)}")
    print(f"📏 Distancia total: {dijkstra.distancia_total:.2f} km")
    print(f"🔢 Número de pasos: {len(dijkstra.pasos)}")
    print("=" * 60)
    
    print("\n🎬 Iniciando animación...")
    print("   (Cierra la ventana para terminar)")
    
    anim, fig = dijkstra.animar()
    plt.show()