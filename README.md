# Transporte inteligente IA

Calcula la ruta más rápida entre dos estaciones de TransMilenio con una base de conocimiento de reglas lógicas y búsqueda A\*. Es un trabajo de la materia de Inteligencia Artificial.

## Requisitos

Python 3.10 o superior. El programa solo usa la biblioteca estándar; pytest hace falta únicamente para correr las pruebas.

## Instalación

Todos los comandos de esta guía se ejecutan en una terminal abierta en la raíz del proyecto, que es la carpeta donde están `README.md`, `requirements.txt` y las carpetas `src/` y `tests/`. Ahí se crea el entorno virtual `.venv`, que `.gitignore` ya excluye del repositorio.

1. Clonar el repositorio y entrar a la carpeta:

   ```
   git clone https://github.com/Lichundead/transporte-inteligente-ia.git
   cd transporte-inteligente-ia
   ```

2. Abrir un terminal en la carpeta raíz y crear el entorno virtual. Se hace una sola vez.

   En Linux o macOS:

   ```
   python3 -m venv .venv
   ```

   En Windows:

   ```
   python -m venv .venv
   ```

3. Activar el entorno. Hay que repetirlo cada vez que se abre una terminal nueva (En VScode se hace automáticamente despues de la primera activación manual).

   En Linux o macOS:

   ```
   source .venv/bin/activate
   ```

   En Windows:

   ```
   .venv\Scripts\activate
   ```

   Con el entorno activo, la línea de la terminal empieza con `(.venv)`. Si en PowerShell sale un error de que la ejecución de scripts está deshabilitada, corran una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelvan a activar.

4. Instalar las dependencias. También se hace una sola vez.

   ```
   pip install -r requirements.txt
   ```

Para salir del entorno se usa `deactivate`.

## Ejecución

Con el entorno activado y desde la raíz del proyecto:

```
Para la ejecución del modelo:
python src/main.py

Para pruebas de código:
pytest
```

El programa primero pregunta si se quiere ver qué regla generó cada hecho. Después muestra las estaciones numeradas y pide el número del origen y el del destino.

## Arquitectura

- `src/base_conocimiento.py` guarda los hechos de la red: 15 estaciones con sus coordenadas, la troncal a la que pertenece cada una y el tiempo entre estaciones vecinas. Se modelan troncales y no servicios (B74, G12...).
- `src/motor_inferencia.py` aplica las reglas por encadenamiento hacia adelante. De ahí salen las conexiones en ambos sentidos y las estaciones de transbordo.
- `src/busqueda.py` busca la ruta con A\*, usando como heurística la distancia en línea recta dividida entre la velocidad máxima del bus. Cada cambio de troncal suma 5 minutos. También trae la misma búsqueda sin heurística para comparar cuántos nodos explora cada una.
- `src/main.py` conecta las tres piezas anteriores y muestra la ruta paso a paso, los transbordos, el tiempo total y la comparación de nodos.
