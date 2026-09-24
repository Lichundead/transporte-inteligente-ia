# Transporte inteligente IA

Calcula la ruta más rápida entre dos estaciones de TransMilenio con una base de conocimiento de reglas lógicas y búsqueda A*. Es un trabajo de la materia de Inteligencia Artificial.

## Requisitos

Python 3.10 o superior. El programa solo usa la biblioteca estándar; pytest hace falta únicamente para correr las pruebas.

## Instalación

En Linux o macOS:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Con el entorno activado y desde la raíz del proyecto:

```
python src/main.py
pytest
```

El programa primero pregunta si se quiere ver qué regla generó cada hecho. Después muestra las estaciones numeradas y pide el número del origen y el del destino.

## Arquitectura

- `src/base_conocimiento.py` guarda los hechos de la red: 15 estaciones con sus coordenadas, la troncal a la que pertenece cada una y el tiempo entre estaciones vecinas. Se modelan troncales y no servicios (B74, G12...).
- `src/motor_inferencia.py` aplica las reglas por encadenamiento hacia adelante. De ahí salen las conexiones en ambos sentidos y las estaciones de transbordo.
- `src/busqueda.py` busca la ruta con A*, usando como heurística la distancia en línea recta dividida entre la velocidad máxima del bus. Cada cambio de troncal suma 5 minutos. También trae la misma búsqueda sin heurística para comparar cuántos nodos explora cada una.
- `src/main.py` conecta las tres piezas anteriores y muestra la ruta paso a paso, los transbordos, el tiempo total y la comparación de nodos.
