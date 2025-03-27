# 🛡️ Python & Flask: Autenticación con JWT (JSON Web Tokens)

Este proyecto implementa un sistema de autenticación de usuarios utilizando JSON Web Tokens (JWT) con Python y Flask.
---

lo clonamos, instalamos.
docker-compose up --build (levanta server postgress y pgadmin)

pgadmin
server: postgres-auth-dev
port 5432

usuario y clave las del yml, con eso estamos ahi.

corremos el app.py

y luego pdremos iniciar las migraciones

estas variables asi:
AUTH_POSTGRES_HOST=localhost
AUTH_POSTGRES_PORT=5464

flask db init
flask db migrate -m "inicial"
flask db upgrade
---




## 🚀 Características

- Registro y autenticación de usuarios
- Protección de rutas con JWT
- Manejo de roles de usuario
- Migraciones de base de datos con Alembic
- Manejo de errores personalizados

## 📋 Requisitos

- Python 3.9+
- pip (Python package installer)

## 🛠️ Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual:
    ```sh
    python -m venv env
    ```

3. Activa el entorno virtual:
    - En Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - En Unix o MacOS:
        ```sh
        source env/bin/activate
        ```

4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1. Crea un archivo [.env](http://_vscodecontentref_/1) en la raíz del proyecto y configura las variables de entorno necesarias. Puedes usar los archivos [.TEMPLATE_env](http://_vscodecontentref_/2), [.TEMPLATE_env.prod](http://_vscodecontentref_/3) y [.TEMPLATE_env.test](http://_vscodecontentref_/4) como referencia.

## 📦 Migraciones de Base de Datos

Para aplicar las migraciones de la base de datos, ejecuta:
```sh
flask db upgrade


Recopilando información del área de trabajo

Claro, aquí tienes un ejemplo de un 

README.md

 con algunos iconos para tu proyecto:

```md
# 🛡️ Python & Flask: Autenticación con JWT (JSON Web Tokens)

Este proyecto implementa un sistema de autenticación de usuarios utilizando JSON Web Tokens (JWT) con Python y Flask.

## 🚀 Características

- Registro y autenticación de usuarios
- Protección de rutas con JWT
- Manejo de roles de usuario
- Migraciones de base de datos con Alembic
- Manejo de errores personalizados

## 📋 Requisitos

- Python 3.9+
- pip (Python package installer)

## 🛠️ Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual:
    ```sh
    python -m venv env
    ```

3. Activa el entorno virtual:
    - En Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - En Unix o MacOS:
        ```sh
        source env/bin/activate
        ```

4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1. Crea un archivo 

.env

 en la raíz del proyecto y configura las variables de entorno necesarias. Puedes usar los archivos 

.TEMPLATE_env

, 

.TEMPLATE_env.prod

 y 

.TEMPLATE_env.test

 como referencia.

## 📦 Migraciones de Base de Datos

Para aplicar las migraciones de la base de datos, ejecuta:
```sh
flask db upgrade
```

## 🚀 Ejecución

Para iniciar la aplicación, ejecuta:
```sh
flask run
```

La aplicación estará disponible en `http://127.0.0.1:5001`.

## 📄 Endpoints

- `POST /auth/register`: Registro de un nuevo usuario.
- `POST /auth/login`: Autenticación de usuario.
- `GET /auth/protected`: Ruta protegida con JWT.
- `PUT /users/update/<int:user_id>`: Actualización de usuario.
- `GET /users/list`: Listado de usuarios.

## 🐳 Docker

También puedes ejecutar la aplicación usando Docker:

1. Construye la imagen de Docker:
    ```sh
    docker build -t flask-jwt-auth .
    ```

2. Ejecuta el contenedor:
    ```sh
    docker run -p 5001:5001 flask-jwt-auth
    ```

## 📚 Documentación

Para más detalles sobre el uso de JWT en Flask, consulta la [documentación oficial de Flask](https://flask.palletsprojects.com/).

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---

Desarrollado con ❤️ por [Fernando Masino](https://github.com/fom78)
```

Este README incluye secciones para la instalación, configuración, ejecución, endpoints y más, con algunos iconos para hacerlo más atractivo. Puedes personalizarlo según tus necesidades.
Este README incluye secciones para la instalación, configuración, ejecución, endpoints y más, con algunos iconos para hacerlo más atractivo. Puedes personalizarlo según tus necesidades.