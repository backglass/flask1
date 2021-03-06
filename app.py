import sqlite3
from webbrowser import get
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort      # Se usará para crear paginas 404

app = Flask(__name__)
app.config['SECRET_KEY'] = 'plisados123' # Configurando clave secreta para el cifrado de cookies


@app.route("/")
def index():

    """
    En esta nueva versión de la función index(), primero abre una conexión de base de datos usando la función get_db_connection()
    que definió antes. A continuación, ejecuta una consulta SQL para seleccionar todas las entradas de la tabla post.
    Implementa el método fetchall() para recuperar todas las filas del resultado de la consulta.
    Esto devolverá una lista de las entradas que insertó en la base de datos en el paso anterior.
    Cierra la conexión con la base de datos usando el método close() y devuelve el resultado de representar la plantilla index.html.
    También pasará el objeto posts como argumento, que contiene los resultados que obtuvo de la base de datos;
    esto le permitirá acceder a las entradas del blog en la plantilla index.html.
    Con estas modificaciones implementadas, guarde y cierre el archivo app.py. """

    conn = get_db_connection()                              # Abre una conexión con la base de datos y devuelve el objeto conn con la conexión a la base de datos "database.db"
    posts = conn.execute("SELECT * FROM posts").fetchall()  # Ejecuta una consulta SQL para seleccionar todas las entradas de la tabla post
    conn.close()                                            # Cierra la conexión con la base de datos
    return render_template("index.html",posts = posts)      # Devuelve el resultado de representar la plantilla index.html y le pasa el objeto posts como argumento


def get_db_connection():
    """
    Esta función get_db_connection() abra una conexión con el archivo de base de datos database.db,
    y luego establece el atributo row_factory a sqlite3. Row para poder tener acceso basado en nombre a las columnas.
    Esto significa que la conexión con la base de datos devolverá filas que se comportan como diccionarios Python regulares.
    Por último, la función devuelve el objeto de conexión conn que usará para acceder a la base de datos.
    """

                                            # Función que crea una conexión con la base de datos "database.db" y devuelve el objeto de conexión
    conn = sqlite3.connect("database.db")   # Crea el objeto conn con la conexión a la base de datos "database.db"
    conn.row_factory = sqlite3.Row          # establece el modo de devolución de filas de la base de datos
    return conn                             # Devuelve el objeto conn con la conexión a la base de datos "database.db"


def get_post(post_id):
    """
    Esta nueva función tiene el argumento post_id que determina qué entrada de blog recuperar.
    Dentro de la función, utiliza la función get_db_connection() para abrir una conexión de base de datos
    y ejecutar una consulta SQL para obtener la entada de blog asociada con el valor post_id dado.
    Añade el método fetchone() para obtener el resultado y almacenarlo en la variable post.
    Luego, cierre la conexión. Si la variable post tiene el valor None, lo que significa
    que no se ha encontrado ningún resultado en la base de datos, utiliza la función abort()
    que importó anteriormente para responder con un código de error 404 y la función terminará la ejecución.
    Si, sin embargo, se encuentra una entrada, devuelve el valor de la variable post.
    """
    conn = get_db_connection()              # Abre una conexión con la base de datos y devuelve el objeto conn con la conexión a la base de datos "database.db"
    post = conn.execute("SELECT * FROM posts WHERE id = ?",(post_id,)).fetchone() # Ejecuta una consulta SQL para seleccionar una entrada por id de la tabla post
    conn.close()                            # Cierra la conexión con la base de datos
    
    if post is None:                        # Si no existe una entrada con el id indicado, abortará la ejecución de la aplicación
        abort(404)
    return post


@app.route("/<int:post_id>")                        # Ruta para recuperar una entrada de blog por id
def post(post_id):

    post = get_post(post_id)                        # Obtiene la entrada de blog asociada con el id indicado
    return render_template("post.html",post = post)


@app.route("/create",methods = ["GET","POST"])      # Ruta para crear una entrada de blog nueva y guardarla en la base de datos
def create():
    """
    En la instrucción if asegura que el código que le sigue solo se ejecuta cuando la solicitud es una solicitud POST
    a través de la comparativa request.method == 'POST'.
    A continuación, extrae el título enviado y el contenido desde el objeto request.form que le proporciona acceso a 
    los datos del formulario en la solicitud. Si no se proporciona el título, la condición if not title se cumplirá,
    mostrando un mensaje al usuario informándole de que el título es obligatorio. Si, por otro lado, se proporciona el título, abrirá una conexión con la función get_db_connection() e insertará el título y el contenido que recibió en la tabla posts.
    Luego confirma los cambios en la base de datos y cierra la conexión. Tras añadir la entrada de blog a la base de datos,
    redirige al cliente a la página de índice usando la función redirect() pasándole la URL generada por la función url_for() con el valor 'index' como argumento.
    Guarde y cierre el archivo.
    """


    if request.method == "POST":                    # Si el método de solicitud es POST, seguirá el flujo de ejecución
        
        title = request.form["title"]               # Obtiene el valor del campo title del formulario de solicitud
        content = request.form["content"]           # Obtiene el valor del campo content del formulario de solicitud
        
        if not title or not content:                # Si no se ha introducido un título mostrara un mensaje al usuario
            flash("Todos los campos son obligatorios")
        else:
            conn = get_db_connection()
            conn.execute ("INSERT INTO posts (title,content) VALUES (?,?)",(title,content)) # Ejecuta una consulta SQL para insertar una nueva entrada de blog
            conn.commit()                           # Guarda los cambios en la base de datos
            conn.close()                            # Cierra la conexión con la base de datos
            return redirect(url_for("index"))       # Redirige a la página de inicio
 
    return render_template("create.html")



@app.route("/<int:id>/edit", methods=["GET","POST"])
def edit(id):
    """
    La entrada que edita viene determinada por la URL y Flask pasará el número de ID a la función edit() a través del argumento id. Añade este valor
    a la función get_post() para recuperar la entrada asociada con el ID proporcionado desde la base de datos. Los nuevos datos vendrán en una solicitud POST,
    que se gestiona dentro de la condición if request.method == 'POST'.
    Igual que cuando creó una nueva entrada, primero extrae los datos del objeto request.form,
    luego muestra un mensaje si el título tiene un valor vacío, de lo contrario, abre una conexión con la base de datos. Luego actualiza la tabla posts estableciendo un nuevo título y nuevo contenido donde el ID de la entrada en la base de datos es igual al ID que estaba en la URL.
    En el caso de una solicitud GET, representa una plantilla edit.html
    pasando la variable post que alberga el valor devuelto de la función get_post(). Usará esto para mostrar el título existente y el contenido en la página de edición."""
    
    post = get_post(id)                         # Obtiene la entrada de blog asociada con el id indicado

    if request.method == "POST":                # Si el método de solicitud es POST, seguirá el flujo de ejecución
        title = request.form["title"]           # Obtiene el valor del campo title del formulario de solicitud
        content = request.form["content"]       # Obtiene el valor del campo content del formulario de solicitud

        if not title:                           # Si no se ha introducido un título mostrara un mensaje al usuario
           flash("Ambos campos requeridos")
    
        else:                                   # Si se ha introducido un título, abrirá una conexión con la función get_db_connection() 
                                                # e insertará el título y el contenido que recibió en la tabla posts.
            conn = get_db_connection()
            conn.execute("UPDATE posts SET title = ?, content = ?" " WHERE id = ?", (title, content, id))
            conn.commit()
            conn.close()
        return redirect(url_for("index"))       # Redirige a la página de inicio cuando se ha actualiza una entrada de blog

    return render_template("edit.html", post = post)    # Muestra la plantilla edit.html pasándole el valor de la variable post


@app.route("/<int:id>/delete", methods = ("POST",))   # Ruta para eliminar una entrada de blog por id
def delete(id):
    post = get_post(id)                                     # Obtiene la entrada de blog asociada con el id indicado y la guarda en la variable post
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?",(id,))    # Elimina la entrada de blog de la base de datos con el id indicado
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))   # Muestra un mensaje al usuario informándole de que la entrada de blog ha sido eliminada
    return redirect(url_for("index"))                               # Redirige a la página de inicio


if __name__ == "__main__":                           ## Activar Flask  con modo depurador
    app.run(debug=True)
    