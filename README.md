# EP3 - Hola Mundo Flask

**Ciberseguridad en Desarrollo_004V_OLS**

App mínima para la evaluación de CI/CD. Sirve como base para que Jenkins
la construya, prueba y despliegue.

## Archivos

- `app.py` — la app Flask (`/` devuelve "Hola Mundo", `/health` para checks del pipeline)
- `test_app.py` — test automatizado que verifica que `/` responde bien
- `requirements.txt` — dependencias con versión fijada

## Cómo correrla localmente

```bash
# 1. Crear entorno virtual (recomendado, evita ensuciar el Python del sistema)
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Levantar el servidor
python app.py
```

Abrir en el navegador: http://127.0.0.1:5000

Debería mostrar `Hola Mundo`.

## Cómo correr el test

```bash
pytest test_app.py -v
```

Debería salir `1 passed`.

## Notas para el pipeline (Jenkins/Docker)

- Puerto por defecto: **5000**
- El test no necesita servidor corriendo aparte: usa el test client interno de Flask.
- `requirements.txt` tiene versiones fijas a propósito, para que el build sea
  reproducible y para que las herramientas de gestión de dependencias (Dependabot,
  etc.) puedan detectar actualizaciones disponibles.
