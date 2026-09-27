"""Programa principal: el usuario elige origen y destino y se muestra la ruta.

Orden de trabajo: 1) el motor deduce hechos nuevos a partir de la base de
conocimiento, 2) el usuario elige estaciones, 3) A* busca la ruta con los
hechos conecta que dedujo el motor.
"""

from base_conocimiento import HECHOS
from busqueda import PENALIZACION_TRANSBORDO, a_estrella, busqueda_sin_heuristica
from motor_inferencia import REGLAS, inferir


def elegir(estaciones, mensaje):
    """Pide un numero hasta que sea valido y devuelve la estacion elegida."""
    while True:
        opcion = input(mensaje).strip()
        if opcion.isdigit() and 1 <= int(opcion) <= len(estaciones):
            return estaciones[int(opcion) - 1]  # la lista empieza en 0
        print("Opcion no valida, intente de nuevo.")


def main():
    mostrar = input(
        "Mostrar que regla genero cada hecho? (s/n): ").strip().lower() == "s"
    hechos = inferir(HECHOS, REGLAS, mostrar)

    # Separamos lo que dedujo el motor segun el predicado.
    conexiones = {h for h in hechos if h[0] == "conecta"}
    transbordos = {h[1] for h in hechos if h[0] == "transbordo"}
    estaciones = sorted(h[1] for h in hechos if h[0] == "estacion")

    print("\nEstaciones:")
    for i, estacion in enumerate(estaciones, 1):
        marca = "  (transbordo)" if estacion in transbordos else ""
        print(f"  {i:2}. {estacion}{marca}")
    origen = elegir(estaciones, "\nNumero de la estacion de origen: ")
    destino = elegir(estaciones, "Numero de la estacion de destino: ")

    camino, minutos, nodos_a = a_estrella(origen, destino, conexiones)
    # De la busqueda sin heuristica solo interesan los minutos y los nodos,
    # para compararlos con A*. [1:] descarta el camino.
    minutos_sin_h, nodos_sin_h = busqueda_sin_heuristica(
        origen, destino, conexiones)[1:]

    print(f"\nRuta de {origen} a {destino}:")
    if len(camino) == 1:
        print("  Ya esta en su destino.")
    # zip(camino, camino[1:]) recorre el camino de a pares de pasos seguidos:
    # (paso 1, paso 2), (paso 2, paso 3)... Asi cada tramo tiene su inicio y
    # su fin, y se nota cuando cambia la troncal entre un tramo y el siguiente.
    for (anterior, troncal_anterior), (estacion, troncal) in zip(camino, camino[1:]):
        if troncal_anterior and troncal != troncal_anterior:
            print(f"  ** Transbordo en {anterior}: de {troncal_anterior} a {troncal} "
                  f"(+{PENALIZACION_TRANSBORDO} min)")
        print(f"  {anterior} -> {estacion}  [{troncal}]")
    print(f"\nTiempo total: {minutos} minutos")

    # Los minutos deben coincidir; los nodos muestran cuanto trabajo
    # se ahorra A* gracias a la heuristica.
    print("\nComparacion de busquedas:")
    print(f"  A*               : {minutos} min, {nodos_a} nodos explorados")
    print(
        f"  Sin heuristica   : {minutos_sin_h} min, {nodos_sin_h} nodos explorados")


if __name__ == "__main__":
    main()
