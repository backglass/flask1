"""Ahora que tiene un esquema SQL en el archivo schema.sql, ("squema.sql")
lo usará para crear la base de datos usando un archivo Python que generará un archivo base de datos .db de SQLite.
 Abra un archivo llamado init_db.py dentro del directorio flask_blog usando su editor preferido:"""

import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

connection = sqlite3.connect("database.db")  # Se el objeto de conexión a la base de datos "database.db"

with open("schema.sql") as f: # Abre el archivo "schema.sql"
    connection.executescript(f.read()) # Ejecuta el archivo "schema.sql" en el objeto de conexión "connection" y lo guarda en la base de datos "database.db"

cur = connection.cursor() # Crea un objeto de cursor para la base de datos "database.db" y lo guarda en la variable "cur"


##### Inserción directa en la base de datos con cur.execute
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('First Post', 'Content for the first post') 
            ) # Inserta un registro en la tabla posts con los valores "First Post" y "Content for the first post"
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            ) # Inserta un registro en la tabla posts con los valores "Second Post" y "Content for the second post"

connection.commit() # Confirma los cambios en la base de datos
connection.close() # Cierra la conexión con la base de datos
