# Nombre del proyecto: A book for you

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
- wtforms
- wtforms.validators
- sys
- pickle
- pytest
- jinja

## Frameworks
No se utilizaron frameworks

## Plugins
No se utilizaron plugins

## Endpoints
- '/': Index
- '/home': Muestra la pagina principal de la aplicación con los botones Log in, Sign up y Settings.
- '/register': Pagina para registrarse
- '/register/newUser': Se envia la informacion mediante un fetch de un nuevo usuario.
- '/login': Iniciar sesión
- '/logout': Cerrar sesión
- '/settings': Configuracion para cambiar nombre de usuario y password.
- 'settings/newPassword': Se envia la informacion mediante un fetch de una nueva password.
- 'settings/deleteUser':  Se envia la informacion de la eliminacion de un usuario.

## Forma de autenticacion
Usamos Flask-Login para poder manejar y authenticar la sesion actual del usuario. Con Flask-WTForms mandamos un formulario para que el backend se comunique con la base de datos.

## Host
localhost:5432

## Manejo de errores
500: Errores en el Servidor

## Ejecutar el archivo `app.py`
