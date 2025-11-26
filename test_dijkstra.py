"""
Script de pruebas para el algoritmo de Dijkstra
Ejecuta varios casos de prueba predefinidos
"""

import heapq

# Definir el grafo
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

def probar_ruta(inicio, fin, distancia_esperada=None):
    """Prueba una ruta específica"""
    camino, distancia = dijkstra(grafo, inicio, fin)
    
    print(f"\n{'='*60}")
    print(f"Ruta: {inicio} → {fin}")
    print(f"{'='*60}")
    print(f"Camino: {' → '.join(camino)}")
    print(f"Distancia: {distancia:.2f} km")
    print(f"Número de saltos: {len(camino) - 1}")
    
    if distancia_esperada is not None:
        diferencia = abs(distancia - distancia_esperada)
        if diferencia < 0.01:
            print(f"✅ CORRECTO: Distancia coincide con la esperada ({distancia_esperada:.2f} km)")
        else:
            print(f"❌ ERROR: Distancia esperada {distancia_esperada:.2f} km, obtenida {distancia:.2f} km")
    
    return camino, distancia

def verificar_conectividad():
    """Verifica que todos los nodos sean alcanzables desde A"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CONECTIVIDAD DEL GRAFO")
    print("="*60)
    
    # Calcular distancias desde A a todos los nodos
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias['A'] = 0
    previos = {nodo: None for nodo in grafo}
    visitados = set()
    
    cola = [(0, 'A')]
    
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
    
    print("\nDistancias desde A a todos los nodos:")
    nodos_alcanzables = 0
    nodos_no_alcanzables = []
    
    for nodo in sorted(grafo.keys()):
        if distancias[nodo] != float('inf'):
            print(f"  A → {nodo}: {distancias[nodo]:.2f} km")
            nodos_alcanzables += 1
        else:
            print(f"  A → {nodo}: ∞ (NO ALCANZABLE)")
            nodos_no_alcanzables.append(nodo)
    
    print(f"\nResumen:")
    print(f"  Total de nodos: {len(grafo)}")
    print(f"  Nodos alcanzables desde A: {nodos_alcanzables}")
    print(f"  Nodos NO alcanzables: {len(nodos_no_alcanzables)}")
    
    if nodos_no_alcanzables:
        print(f"  ⚠️  ADVERTENCIA: Los siguientes nodos no son alcanzables desde A:")
        for nodo in nodos_no_alcanzables:
            print(f"     - {nodo}")
        print(f"  El grafo NO está completamente conectado.")
    else:
        print(f"  ✅ El grafo está completamente conectado.")

def ejecutar_pruebas():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print(" " * 15 + "PRUEBAS DEL ALGORITMO DE DIJKSTRA")
    print("="*60)
    
    # Verificar conectividad
    verificar_conectividad()
    
    # Casos de prueba
    print("\n" + "="*60)
    print(" " * 20 + "CASOS DE PRUEBA")
    print("="*60)
    
    casos_prueba = [
        ('A', 'B', 0.9),    # Camino directo muy corto
        ('A', 'N', 7.7),    # Camino largo
        ('A', 'Ñ', 7.6),    # Camino mediano (CORREGIDO)
        ('E', 'H', 3.4),    # Desde un nodo aislado (CORREGIDO)
        ('H', 'E', 3.4),    # Camino inverso (CORREGIDO)
        ('G', 'I', 0.8),    # Camino más corto posible
        ('A', 'A', 0.0),    # Mismo nodo
        ('L', 'C', 2.2),    # Camino directo
        ('M', 'N', 1.1),    # Camino directo corto
        ('B', 'Ñ', 8.5),    # Camino largo desde B (CORREGIDO)
    ]
    
    resultados = []
    
    for inicio, fin, distancia_esperada in casos_prueba:
        camino, distancia = probar_ruta(inicio, fin, distancia_esperada)
        resultados.append({
            'inicio': inicio,
            'fin': fin,
            'camino': camino,
            'distancia': distancia,
            'esperada': distancia_esperada,
            'correcto': abs(distancia - distancia_esperada) < 0.01
        })
    
    # Resumen de pruebas
    print("\n" + "="*60)
    print(" " * 22 + "RESUMEN DE PRUEBAS")
    print("="*60)
    
    correctas = sum(1 for r in resultados if r['correcto'])
    total = len(resultados)
    
    print(f"\nPruebas ejecutadas: {total}")
    print(f"Pruebas correctas: {correctas}")
    print(f"Pruebas fallidas: {total - correctas}")
    print(f"Porcentaje de éxito: {(correctas/total)*100:.1f}%")
    
    if correctas == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON:")
        for r in resultados:
            if not r['correcto']:
                print(f"   {r['inicio']} → {r['fin']}: "
                      f"Esperado {r['esperada']:.2f} km, Obtenido {r['distancia']:.2f} km")
    
    print("\n" + "="*60)

def estadisticas_grafo():
    """Muestra estadísticas del grafo"""
    print("\n" + "="*60)
    print(" " * 18 + "ESTADÍSTICAS DEL GRAFO")
    print("="*60)
    
    # Contar nodos y aristas
    num_nodos = len(grafo)
    num_aristas = sum(len(vecinos) for vecinos in grafo.values()) // 2
    
    # Calcular grados de nodos
    grados = {nodo: len(vecinos) for nodo, vecinos in grafo.items()}
    grado_max = max(grados.values())
    grado_min = min(grados.values())
    grado_promedio = sum(grados.values()) / len(grados)
    
    # Encontrar nodos con grado máximo y mínimo
    nodos_max_grado = [nodo for nodo, grado in grados.items() if grado == grado_max]
    nodos_min_grado = [nodo for nodo, grado in grados.items() if grado == grado_min]
    
    # Calcular distancia total de todas las aristas
    distancia_total = sum(peso for vecinos in grafo.values() for _, peso in vecinos) / 2
    
    print(f"\nNúmero de nodos: {num_nodos}")
    print(f"Número de aristas: {num_aristas}")
    print(f"Distancia total de aristas: {distancia_total:.2f} km")
    print(f"\nGrado de nodos:")
    print(f"  Grado máximo: {grado_max} (Nodos: {', '.join(nodos_max_grado)})")
    print(f"  Grado mínimo: {grado_min} (Nodos: {', '.join(nodos_min_grado)})")
    print(f"  Grado promedio: {grado_promedio:.2f}")
    
    print(f"\nGrados de todos los nodos:")
    for nodo in sorted(grafo.keys()):
        print(f"  {nodo}: {grados[nodo]} conexiones")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("\n" + "🔬" * 30)
    print(" " * 15 + "SUITE DE PRUEBAS - ALGORITMO DE DIJKSTRA")
    print("🔬" * 30)
    
    # Ejecutar todas las pruebas
    estadisticas_grafo()
    ejecutar_pruebas()
    
    print("\n✅ Todas las pruebas han finalizado.")
    print("=" * 60)