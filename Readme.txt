Descripción.
Título: Tienda Online 
Proyecto para la gestión administrativa de las ventas e ingreso de productos de una tienda.


¿Como iniciar este repositorio?
1. iniciar git y clonar el repositorio en tu computador
   $git clone 'https://github.com/persyjr/PRUEBA_TIENDA_ONLINE.git'
   abrir el proyecto en tu IDE

2. Configurar base.
    Crear base de datos en postgress
    crear archivo .env con la siguiente información
    File .env Example. 
    DATABASE_URL=psql://user_base:pwd_user@localhost:5432/NAME_BASE

3. Crear ambiente virtual e instalar Requirements.txt
    $python -m venv venv
    $source venv/bin/activate
    $pip install -r requirements.txt

4. Iniciar Django
    $python TiendaOnline/manage.py runserver

5. correr migraciones.
    $python TiendaOnline/manage.py migrate

6. crear super user para base local
    $python TiendaOnline/manage.py createsuperuser
    user_admin : admin
    pwd : admin
