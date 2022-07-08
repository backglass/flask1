import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

def get_db_connection():
    """
    Esta función get_db_connection() abra una conexión con el archivo de base de datos database.db,
    y luego establece el atributo row_factory a sqlite3. Row para poder tener acceso basado en nombre a las columnas.
    Esto significa que la conexión con la base de datos devolverá filas que se comportan como diccionarios Python regulares.
    Por último, la función devuelve el objeto de conexión conn que usará para acceder a la base de datos.
    """

                 # Función que crea una conexión con la base de datos "database.db" y devuelve el objeto de conexión
    conn = sqlite3.connect("database.db")   # Crea el objeto conn con la conexión a la base de datos "database.db"
    conn.row_factory = sqlite3.Row   # establece el modo de devolución de filas de la base de datos
    return conn                      # Devuelve el objeto conn con la conexión a la base de datos "database.db"


if __name__ == "__main__":  ## Activar Flask  con modo depurador
    app.run(debug=True)
    