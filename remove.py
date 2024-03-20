import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('delete from produtos;')
cursor.execute('delete from vendas;')
cursor.execute('delete from entradas;')


conn.commit()
conn.close()