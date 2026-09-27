"""Base de conocimiento: hechos sobre la red de TransMilenio.

Cada hecho es una tupla cuyo primer elemento es el nombre del predicado,
igual que en Prolog: ("estacion", "heroes", 4.666, -74.059) equivale a
estacion(heroes, 4.666, -74.059).

Simplificacion: se modelan las troncales y no los servicios (B74, G12...).
Suponemos que en cada troncal hay un bus que la recorre completa y para en
todas las estaciones. Las coordenadas y los minutos son aproximados.
"""

# estacion(Nombre, Latitud, Longitud).
ESTACIONES = {
    ("estacion", "portal_norte", 4.7545, -74.0461),
    ("estacion", "toberin", 4.7465, -74.0475),
    ("estacion", "calle_146", 4.7267, -74.0474),
    ("estacion", "calle_100", 4.6863, -74.0566),
    ("estacion", "heroes", 4.6664, -74.0593),
    ("estacion", "calle_76", 4.6606, -74.0631),
    ("estacion", "calle_72", 4.6558, -74.0642),
    ("estacion", "calle_57", 4.6443, -74.0674),
    ("estacion", "calle_45", 4.6326, -74.0692),
    ("estacion", "av_jimenez", 4.6025, -74.0768),
    ("estacion", "tercer_milenio", 4.5973, -74.0813),
    ("estacion", "puente_aranda", 4.6195, -74.1080),
    ("estacion", "marsella", 4.6275, -74.1355),
    ("estacion", "banderas", 4.6305, -74.1510),
    ("estacion", "portal_americas", 4.6295, -74.1720),
}

# en_troncal(Estacion, Troncal).
# heroes y av_jimenez aparecen en dos troncales: son las de intercambio.
EN_TRONCAL = {
    ("en_troncal", e, "autonorte")
    for e in ["portal_norte", "toberin", "calle_146", "calle_100", "heroes"]
} | {
    ("en_troncal", e, "caracas")
    for e in ["heroes", "calle_76", "calle_72", "calle_57", "calle_45", "av_jimenez", "tercer_milenio"]
} | {
    ("en_troncal", e, "americas")
    for e in ["av_jimenez", "puente_aranda", "marsella", "banderas", "portal_americas"]
}

# siguiente(Troncal, EstacionA, EstacionB, Minutos).
# Solo se escribe un sentido; el motor de inferencia deduce el regreso.
SIGUIENTE = {
    ("siguiente", "autonorte", "portal_norte", "toberin", 2),
    ("siguiente", "autonorte", "toberin", "calle_146", 4),
    ("siguiente", "autonorte", "calle_146", "calle_100", 8),
    ("siguiente", "autonorte", "calle_100", "heroes", 4),
    ("siguiente", "caracas", "heroes", "calle_76", 2),
    ("siguiente", "caracas", "calle_76", "calle_72", 2),
    ("siguiente", "caracas", "calle_72", "calle_57", 3),
    ("siguiente", "caracas", "calle_57", "calle_45", 3),
    ("siguiente", "caracas", "calle_45", "av_jimenez", 7),
    ("siguiente", "caracas", "av_jimenez", "tercer_milenio", 2),
    ("siguiente", "americas", "av_jimenez", "puente_aranda", 8),
    ("siguiente", "americas", "puente_aranda", "marsella", 6),
    ("siguiente", "americas", "marsella", "banderas", 4),
    ("siguiente", "americas", "banderas", "portal_americas", 4),
}

# El motor de inferencia recibe todos los hechos en un solo conjunto.
HECHOS = ESTACIONES | EN_TRONCAL | SIGUIENTE
