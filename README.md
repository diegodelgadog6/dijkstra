# Algoritmo de Dijkstra con Animación

LINK DEL VIDEO DE EXPLICACION: 

## 📋 Descripción
Implementación del algoritmo de Dijkstra para encontrar la ruta más corta en un grafo de 15 nodos con visualización animada paso a paso.

## 🎯 Características
- ✅ Implementación completa del algoritmo de Dijkstra
- ✅ Animación paso a paso del proceso
- ✅ Visualización de:
  - Nodos visitados
  - Distancias calculadas
  - Nodo actual en exploración
  - Cola de prioridad
  - Camino óptimo final
- ✅ Interfaz interactiva para seleccionar nodo origen y destino

## 📦 Requisitos
- Python 3.7+
- matplotlib
- networkx

## 🚀 Instalación

### Opción 1: Usando pip
```bash
pip install matplotlib networkx
```

### Opción 2: Usando el archivo requirements.txt
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecución básica
```bash
python dijkstra_animado.py
```

El programa te pedirá:
1. **Nodo de inicio** (ej: A, B, C, etc.)
2. **Nodo de destino** (ej: N, M, K, etc.)

### Ejemplo de ejecución
```
ALGORITMO DE DIJKSTRA CON ANIMACIÓN
============================================================

Grafo de 15 nodos: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ

Ingrese el nodo de inicio (ej: A): A
Ingrese el nodo de destino (ej: N): N

🔍 Calculando ruta más corta de A a N...

============================================================
RESULTADO:
============================================================
📍 Camino óptimo: A → B → C → L → N
📏 Distancia total: 7.70 km
🔢 Número de pasos: 12
============================================================

🎬 Iniciando animación...
```

## 🎨 Leyenda de Colores

| Color | Significado |
|-------|-------------|
| 🟢 Verde claro | Nodo de inicio |
| 🔴 Rojo claro | Nodo de destino |
| 🟡 Amarillo | Nodo actual en exploración |
| 🔵 Azul claro | Nodo ya visitado |
| 💛 Amarillo claro | Nodo en cola de prioridad |
| ⚪ Gris claro | Nodo no visitado |
| 🟢 Verde (arista) | Camino óptimo final |

## 📊 Estructura del Grafo

El grafo contiene 15 nodos con las siguientes conexiones:

```
A: B(0.9 km), D(1.1 km)
B: A(0.9 km), C(1.5 km)
C: B(1.5 km), L(2.2 km)
D: A(1.1 km), F(1.2 km)
E: G(1.1 km)
F: D(1.2 km), G(1.1 km), H(1.3 km)
G: E(1.1 km), F(1.1 km), I(0.8 km), K(3.5 km)
H: F(1.3 km), I(1.5 km)
I: G(0.8 km), H(1.5 km), J(1.3 km)
J: I(1.3 km), Ñ(2.1 km)
K: G(3.5 km), M(1.1 km), Ñ(1.4 km)
L: N(3.1 km), C(2.2 km)
M: K(1.1 km), N(1.1 km)
N: M(1.1 km), L(3.1 km)
Ñ: J(2.1 km), K(1.4 km)
```

## 🔍 ¿Cómo funciona?

### Algoritmo de Dijkstra
1. **Inicialización**: Se establece la distancia del nodo origen como 0 y todas las demás como infinito
2. **Exploración**: Se selecciona el nodo no visitado con menor distancia
3. **Actualización**: Se actualizan las distancias de los vecinos si se encuentra un camino más corto
4. **Repetición**: Se repite hasta visitar todos los nodos o alcanzar el destino

### Animación
- Cada frame muestra un paso del algoritmo
- Las distancias se actualizan en rojo debajo de cada nodo
- El nodo actual se resalta en amarillo
- Los nodos visitados se muestran en azul
- Al final, el camino óptimo se resalta en verde

## 📝 Ejemplos de Rutas Interesantes

| Origen | Destino | Distancia | Camino |
|--------|---------|-----------|--------|
| A | N | 7.70 km | A → B → C → L → N |
| A | Ñ | 7.60 km | A → D → F → G → I → J → Ñ |
| E | M | 6.90 km | E → G → K → M |
| H | N | 7.60 km | H → I → J → Ñ → K → M → N |
| G | I | 0.80 km | G → I (ruta más corta) |

## 🛠️ Personalización

### Modificar el grafo
Puedes editar el diccionario `grafo` en el archivo `dijkstra_animado.py`:

```python
grafo = {
    'A': [('B', 0.9), ('D', 1.1)],
    # Agrega o modifica conexiones aquí
}
```

### Cambiar posiciones de nodos
Modifica el diccionario `posiciones` para ajustar la visualización:

```python
posiciones = {
    'A': (0, 5),
    # Cambia las coordenadas (x, y)
}
```

### Ajustar velocidad de animación
Modifica el parámetro `interval` en la función `FuncAnimation`:

```python
anim = animation.FuncAnimation(fig, actualizar, frames=frames_totales,
                              interval=1000,  # milisegundos (1000 = 1 segundo)
                              repeat=True)
```

## 📚 Recursos Adicionales
- [Algoritmo de Dijkstra - Wikipedia](https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Matplotlib Animation](https://matplotlib.org/stable/api/animation_api.html)

## 👥 Autor
Proyecto educativo para el Módulo 1: Algoritmo de Dijkstra con Animación

## 📄 Licencia
Este proyecto es de código abierto y está disponible para fines educativos.