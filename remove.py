import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('drop table produtos;')
cursor.execute('drop table vendas;')
cursor.execute('drop table entradas;')
cursor.execute("""
CREATE TABLE vendas (
	id_venda INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_produto INTEGER NOT NULL,
	dt_hr_venda TEXT NOT NULL,
	quantidade NUMERIC DEFAULT (0) NOT NULL
);
               """)

cursor.execute("""
CREATE TABLE produtos (
    id_produto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    descricao TEXT(100) NOT NULL, 
    unidade TEXT(20), 
    quantidade NUMERIC DEFAULT (0) NOT NULL, 
    vr_venda NUMERIC DEFAULT (0) NOT NULL, 
    vr_custo NUMERIC DEFAULT (0) NOT NULL
);
               """)

cursor.execute("""
CREATE TABLE entradas (
	id_entrada INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_produto INTEGER NOT NULL,
	dt_hr_entrada TEXT NOT NULL,
	quantidade NUMERIC DEFAULT (0) NOT NULL
);
               """)


conn.commit()
conn.close()