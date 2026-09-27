"""Pruebas del sistema. Se corren con pytest desde la raiz del proyecto.

Todas usan las conexiones que deduce el motor, igual que main.py.
"""

from base_conocimiento import HECHOS
from busqueda import a_estrella, busqueda_sin_heuristica
from motor_inferencia import REGLAS, inferir

HECHOS_INFERIDOS = inferir(HECHOS, REGLAS)
CONEXIONES = {h for h in HECHOS_INFERIDOS if h[0] == "conecta"}
ESTACIONES = [h[1] for h in HECHOS if h[0] == "estacion"]


def solo_estaciones(camino):
    """Quita la troncal de cada paso para comparar solo los nombres."""
    return [estacion for estacion, _ in camino]


def test_ruta_en_una_sola_troncal():
    """Todo por autonorte, sin transbordo: se suman solo los minutos de cada tramo."""
    camino, minutos, _ = a_estrella("portal_norte", "calle_100", CONEXIONES)
    assert solo_estaciones(camino) == [
        "portal_norte", "toberin", "calle_146", "calle_100"]
    assert minutos == 2 + 4 + 8


def test_ruta_con_transbordo():
    """De autonorte a caracas: hay que cambiar de troncal en heroes."""
    camino, minutos, _ = a_estrella("calle_100", "calle_72", CONEXIONES)
    assert solo_estaciones(camino) == [
        "calle_100", "heroes", "calle_76", "calle_72"]
    assert minutos == 4 + 2 + 2 + 5  # 5 = penalizacion por cambiar a caracas en heroes


def test_origen_igual_a_destino():
    """El camino es solo la estacion de partida y no cuesta nada."""
    camino, minutos, _ = a_estrella("heroes", "heroes", CONEXIONES)
    assert solo_estaciones(camino) == ["heroes"]
    assert minutos == 0


def test_a_estrella_y_sin_heuristica_dan_el_mismo_tiempo():
    """Si la heuristica nunca sobreestima, A* es optimo: debe coincidir con Dijkstra."""
    # Se prueban todas las combinaciones de origen y destino (15 x 15).
    for origen in ESTACIONES:
        for destino in ESTACIONES:
            _, con_h, _ = a_estrella(origen, destino, CONEXIONES)
            _, sin_h, _ = busqueda_sin_heuristica(origen, destino, CONEXIONES)
            assert con_h == sin_h, (origen, destino)


def test_regla_transbordo_detecta_intercambios():
    """Son las unicas estaciones que estan en dos troncales a la vez."""
    transbordos = {h[1] for h in HECHOS_INFERIDOS if h[0] == "transbordo"}
    assert transbordos == {"heroes", "av_jimenez"}
