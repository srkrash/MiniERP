-- vendas definition

CREATE TABLE vendas (
	id_venda INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_produto INTEGER NOT NULL,
	dt_hr_venda TEXT NOT NULL,
	quantidade NUMERIC DEFAULT (0) NOT NULL
);

-- produtos definition

CREATE TABLE produtos (
    id_produto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    descricao TEXT(100) NOT NULL, 
    unidade TEXT(20), 
    quantidade NUMERIC DEFAULT (0) NOT NULL, 
    vr_venda NUMERIC DEFAULT (0) NOT NULL, 
    vr_custo NUMERIC DEFAULT (0) NOT NULL
);

-- entradas definition

CREATE TABLE entradas (
	id_entrada INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_produto INTEGER NOT NULL,
	dt_hr_entrada TEXT NOT NULL,
	quantidade NUMERIC DEFAULT (0) NOT NULL
);