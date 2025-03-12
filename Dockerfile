FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Gerekli Python bağımlılıklarını yükle
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .  

# Çalışma dizinini /app/src olarak değiştir
WORKDIR /app/src  

# Uygulamayı çalıştır
CMD ["python", "main.py"]