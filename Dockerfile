# Gunakan image Python versi stabil
FROM python:3.10-slim

# Set working directory di container
WORKDIR /app

RUN apt-get update

# Salin requirements.txt ke container
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh isi project ke container
COPY . .

# Expose port Flask (default 5000)
EXPOSE 5000

# Jalankan API
CMD ["python", "app.py"]