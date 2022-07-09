from os import abort
import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort      # Se usará para crear paginas 404

app = Flask(__name__)


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

    
if __name__ == "__main__":  ## Activar Flask  con modo depurador
    app.run(debug=True)
    