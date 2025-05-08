import sqlite3 

conn = sqlite3.connect('poemas.db')
c = conn.cursor() #Cursor para ejecutar 

c.execute('''
CREATE TABLE IF NOT EXISTS poemas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    etiquetas TEXT,
    fecha TEXT
    )
''')

conn.commit()
conn.close()
print("Base de datos creada con éxito.")