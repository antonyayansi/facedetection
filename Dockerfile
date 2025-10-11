FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para dlib y Pillow
RUN apt-get update && apt-get install -y \
    build-essential cmake g++ libopenblas-dev liblapack-dev \
    libx11-dev libjpeg-dev zlib1g-dev libpng-dev && \
    pip install --upgrade pip

# Copiar archivos
WORKDIR /app
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Iniciar el servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
