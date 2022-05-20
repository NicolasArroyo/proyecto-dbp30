# A book for you

## Integrantes

- Nicolas Mateo Arroyo Chavez
- Josue Mauricio Arriaga Colchado
- Francisco Escalante Farje
- Matias Jose Castro Mendoza

## Descripcion
El presente proyecto del curso de Desarrollo basado en plataformas, es la página web de una biblioteca virtual (A book for you) en la cual se puede almacenar, rentar y distribuir libros de diferentes categorias para cualquier tipo de usuario. Se puede tener una cuenta personal que te brindara un entorno más personalizado y único.

## Objetivos principales
El principal objetivo de esta entorno es poder adquirir un libro que te guste de las diferentes categorias que contamos y poder nutrirte con su información.

## Mision
Satisfacer íntegramente las necesidades de nuestros clientes, ofreciendo el mayor surtido de libros de texto, lectura e innovación digital.  Satisfaciendo las necesidades de la comunidad educativa con una amplia gama de editoriales para garantizar el aprendizaje y fomentar el amor a la lectura en el público en general.

## Vision
Ser la librería líder en el Perú en la venta y distribución de libros de textos, libros de lectura en general, tanto de editoriales nacionales como extranjeras, reconocida por la calidad de nuestro servicio y la contribución a la comunidad educativa.

## Librerias
- flask
- flask_sqlalchemy
- flask_migrate
- flask_login
- flask_wtf
- flask_bcrypt
- wtforms
- wtforms.validators
- sys
- pickle
- pytest
- jinja
- datetime

## Frameworks
No se utilizaron frameworks

## Plugins
No se utilizaron plugins

## Endpoints
- '/': Index
- '/home': Muestra la pagina principal de la aplicación con los botones Log in, Sign up y Settings.
- '/home/search': Endpoint en el que se obtiene los ids de cada libro para buscarlos.
- '/home/rent': Se hace un POST de los libros por rentar de un usuario.
- '/register': Pagina para registrarse
- '/register/newUser': Se envia la informacion mediante un fetch de un nuevo usuario.
- '/login': Iniciar sesión
- '/logout': Cerrar sesión
- '/settings': Configuracion para cambiar nombre de usuario y borrar tu usuario.
- 'settings/newPassword': Se envia la nueva password del usuario logeado a la base de datos.
- 'settings/deleteUser':  Se envia la informacion de la eliminacion de un usuario a la base de datos.
- '/add_book': Renderiza el template add_book.html
- '/add_book/new': Endpoint al que se postea un nuevo libro agregado por un administrador.
- '/add_author': Renderiza el template add_author.html
- '/add_author/new': Endpoint al que se postea un nuevo autor agregado por un administrador.

## Forma de autenticacion
Usamos Flask-Login para poder manejar y authenticar la sesion actual del usuario. Con Flask-WTForms mandamos un formulario para que el backend se comunique con la base de datos.

## Host
http://127.0.0.1:5001/
localhost: 5432
port: 5001

## Manejo de errores
- 401: Unauthorized (informacion entregada invalida)
- 403: Forbidden (falta de permisos para acceder a la pagina)
- 404: Not found (pagina no encontrada)
- 500: Internal server error (Error de servidor)

## Ejecutar el archivo `app.py`
