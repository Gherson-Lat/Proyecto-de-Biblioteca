# Imagen base oficial de Python (ligera)
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza salida sin búfer para ver logs en vivo
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de requerimientos e instalarlos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente del proyecto al contenedor
COPY . /app/

# Exponer el puerto predeterminado de FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor de FastAPI con hot-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]