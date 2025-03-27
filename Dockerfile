# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Crea la carpeta instance y asigna permisos adecuados
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Expón el puerto en el que el servicio de auth estará corriendo
EXPOSE 5001

RUN flask init_db

CMD ["python", "app.py"]
# Ejecuta las migraciones antes de iniciar el servidor
# CMD ["sh", "-c", "flask db upgrade && python app.py"]
