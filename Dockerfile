# Dockerfile para Sistema de Gestión Odontológica
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Crear directorio para la base de datos y backups
RUN mkdir -p instance/backups

# Exponer puerto
EXPOSE 5000

# Variable de entorno para producción
ENV FLASK_ENV=production

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "run:app"]
