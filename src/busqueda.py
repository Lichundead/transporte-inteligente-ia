"""Busqueda A* sobre los hechos conecta(T, A, B, M) que dedujo el motor."""

import heapq
import math

from base_conocimiento import ESTACIONES

VELOCIDAD_MAXIMA_KMH = 60  # ningun bus de la red va mas rapido que esto
PENALIZACION_TRANSBORDO = 5  # minutos extra por bajarse y cambiar de troncal
# Diccionario nombre -> (latitud, longitud) para buscar coordenadas rapido.
COORDENADAS = {nombre: (lat, lon) for (_, nombre, lat, lon) in ESTACIONES}


def heuristica(a, b):
    """Minutos que tardaria un bus yendo en linea recta a velocidad maxima.

    Nunca sobreestima el tiempo real: la linea recta es el camino mas corto
    posible y la velocidad maxima es la mas alta posible, asi que ningun
    recorrido real puede ser mas rapido. Por eso A* encuentra la ruta optima.
    """
    (lat1, lon1), (lat2, lon2) = COORDENADAS[a], COORDENADAS[b]
    # Formula de haversine: distancia sobre la superficie de la Tierra.
    # Las funciones trigonometricas de math trabajan en radianes.
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    s = math.sin(dp / 2) ** 2 + math.cos(p1) * \
        math.cos(p2) * math.sin(dl / 2) ** 2
    km = 2 * 6371 * math.asin(math.sqrt(s))  # 6371 km = radio de la Tierra
    return km / VELOCIDAD_MAXIMA_KMH * 60  # horas -> minutos


def a_estrella(origen, destino, conexiones, h=heuristica):
    """Devuelve (camino, minutos_totales, nodos_expandidos).

    camino es una lista de (estacion, troncal por la que se llego). El estado
    guarda la troncal porque de ella depende el transbordo: quien llega a
    heroes por autonorte y sigue por caracas paga la penalizacion.
    """
    # Lista de adyacencia: para cada estacion, a donde se puede ir,
    # cuantos minutos tarda y por que troncal.
    vecinos = {}
    for _, t, a, b, m in conexiones:
        vecinos.setdefault(a, []).append((b, m, t))

    # La frontera es una cola de prioridad (heapq): siempre saca el
    # elemento con menor f. Cada elemento es:
    # (f = g + h, g = minutos hasta aqui, estacion, troncal, camino)
    # En el origen la troncal es "" porque todavia no se ha subido a ningun bus.
    frontera = [(h(origen, destino), 0, origen, "", [(origen, "")])]
    visitados = set()
    expandidos = 0
    while frontera:
        _, g, estacion, troncal, camino = heapq.heappop(
            frontera)  # el de menor f
        # Se revisa la meta al sacar de la cola (no al meter): en ese momento
        # ya no puede existir un camino mas barato hasta el destino.
        if estacion == destino:
            return camino, g, expandidos
        # Un mismo estado puede quedar varias veces en la cola con costos
        # distintos. Solo se expande la primera vez, que es la mas barata.
        if (estacion, troncal) in visitados:
            continue
        visitados.add((estacion, troncal))
        expandidos += 1
        for vecino, minutos, t in vecinos.get(estacion, []):
            costo = g + minutos
            if troncal and t != troncal:  # cambio de troncal = transbordo
                costo += PENALIZACION_TRANSBORDO
            heapq.heappush(frontera, (costo + h(vecino, destino),
                           costo, vecino, t, camino + [(vecino, t)]))
    # Se vacio la frontera sin llegar: no hay ruta entre las dos estaciones.
    return None, math.inf, expandidos


def busqueda_sin_heuristica(origen, destino, conexiones):
    """A* con h = 0, que es Dijkstra: expande por costo sin saber donde queda el destino."""
    return a_estrella(origen, destino, conexiones, h=lambda a, b: 0)
