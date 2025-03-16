# FUP-backend

### Requisitos
- Python 3.12
- Pipenv (entorno virtual)
- docker
- postman (Opcional para probar la api y el websocket)

### Get started
Una vez clonado el repositorio ubiquese en la raíz del proyecto y ejecute los siguientes comandos para correr localmente el proyecto.
- ``` docker-compose build``` Para construir la imagen del proyecto.
- ``` docker-compose up``` Para levantar todos los servicios de la plantilla (DB, servidor local Django)
- Para aplicar las migraciones utilize el siguiente comando ```docker-compose run --rm <nombre_contenedor(app)> python manage.py migrate --settings=fup.settings.develop```
- Para crear un superusuario ```docker-compose run --rm <nombre_contenedor(app)> python manage.py createsuperuser --settings=fup.settings.develop```
