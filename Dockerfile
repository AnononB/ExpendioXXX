FROM python:3.10-slim

WORKDIR /code

# Copiamos e instalamos las librerías
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos el resto del código
COPY ./app /code/app

# El comando debe ir en una sola línea y usar comillas dobles
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]