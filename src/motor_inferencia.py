"""Motor de inferencia con encadenamiento hacia adelante.

Cada regla es una funcion que recibe el conjunto de hechos y devuelve
los hechos que se pueden deducir de ellos. Las reglas no modifican el
conjunto; de eso se encarga inferir().
"""


def regla_conecta(hechos):
    """conecta(T, A, B, M) :- siguiente(T, A, B, M).

    Guardamos la troncal T en conecta porque la busqueda la necesita
    para saber cuando hay transbordo.
    """
    # Mismos argumentos que siguiente, solo cambia el nombre del predicado.
    # hecho[1:] toma todo menos el nombre: (troncal, a, b, minutos).
    return {("conecta",) + hecho[1:] for hecho in hechos if hecho[0] == "siguiente"}


def regla_simetrica(hechos):
    """conecta(T, B, A, M) :- conecta(T, A, B, M).

    Los buses van en ambos sentidos. Esta regla usa hechos que produjo
    otra regla: por eso inferir() repite hasta que no salga nada nuevo.
    """
    nuevos = set()
    for hecho in hechos:
        if hecho[0] == "conecta":
            _, t, a, b, m = hecho
            nuevos.add(("conecta", t, b, a, m))  # mismo tramo, al reves
    return nuevos


def regla_transbordo(hechos):
    """transbordo(E) :- en_troncal(E, T1), en_troncal(E, T2), T1 != T2."""
    en_troncal = [hecho for hecho in hechos if hecho[0] == "en_troncal"]
    nuevos = set()
    # Compara cada hecho en_troncal con todos los demas. Si la misma
    # estacion aparece con dos troncales distintas, es de transbordo.
    for _, e1, t1 in en_troncal:
        for _, e2, t2 in en_troncal:
            if e1 == e2 and t1 != t2:
                nuevos.add(("transbordo", e1))
    return nuevos


REGLAS = [regla_conecta, regla_simetrica, regla_transbordo]


def como_texto(hecho):
    """("transbordo", "heroes") -> "transbordo(heroes)", para leerlo como logica."""
    return f"{hecho[0]}({', '.join(str(x) for x in hecho[1:])})"


def inferir(hechos, reglas, mostrar=False):
    """Aplica las reglas una y otra vez hasta que ninguna produzca un hecho nuevo.

    Devuelve los hechos originales mas todos los deducidos. Con mostrar=True
    imprime cada hecho nuevo junto con la regla que lo genero.
    """
    hechos = set(hechos)  # copia: no tocamos la base de conocimiento original
    hubo_nuevos = True
    # Cada vuelta del while recorre todas las reglas. Si en una vuelta
    # completa ninguna regla aporta algo nuevo, ya se dedujo todo.
    while hubo_nuevos:
        hubo_nuevos = False
        for regla in reglas:
            nuevos = regla(hechos) - hechos  # solo lo que aun no sabiamos
            for hecho in sorted(nuevos):  # ordenados para que la salida sea legible
                if mostrar:
                    print(f"  {regla.__name__} => {como_texto(hecho)}")
                hechos.add(hecho)
                hubo_nuevos = True
    return hechos
