# Imagen base con Python 3.10 y las herramientas necesarias
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libdlib-dev \
    libgl1 \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
