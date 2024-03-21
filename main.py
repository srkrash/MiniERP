import PySimpleGUI as sg
import sqlite3
import os
from datetime import datetime

class main:
    def __init__(self) -> None:
        self.conn = None
        self.tamanho_letra=24
        self.esquema_referencia = {
            'vendas': [(0, 'id_venda', 'INTEGER', 1, None, 1), (1, 'id_produto', 'INTEGER', 1, None, 0), (2, 'dt_hr_venda', 'TEXT', 1, None, 0), (3, 'quantidade', 'NUMERIC', 1, '0', 0), (4, 'vr_venda', 'NUMERIC', 1, '0', 0), (5, 'vr_total', 'NUMERIC', 1, '0', 0), (6, 'vr_pago', 'NUMERIC', 1, '0', 0), (7, 'vr_custo', 'NUMERIC', 1, '0', 0), (8, 'vr_troco', 'NUMERIC', 1, '0', 0)],
            'produtos': [(0, 'id_produto', 'INTEGER', 1, None, 1), (1, 'descricao', 'TEXT(100)', 1, None, 0), (2, 'unidade', 'TEXT(20)', 0, None, 0), (3, 'quantidade', 'NUMERIC', 1, '0', 0), (4, 'vr_venda', 'NUMERIC', 1, '0', 0), (5, 'vr_custo', 'NUMERIC', 1, '0', 0)],
            'entradas': [(0, 'id_entrada', 'INTEGER', 1, None, 1), (1, 'id_produto', 'INTEGER', 1, None, 0), (2, 'dt_hr_entrada', 'TEXT', 1, None, 0), (3, 'quantidade', 'NUMERIC', 1, '0', 0), (4, 'vr_venda', 'NUMERIC', 1, '0', 0), (5, 'vr_custo', 'NUMERIC', 1, '0', 0)],
        }
        
    def fazer_conexao(self):
        self.conn = sqlite3.connect('database.db')

    def fechar_conexao(self):
        self.conn.close()

    def obter_esquema_tabela(self, cursor, nome_tabela):
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        return colunas
    
    def verificar_integridade_bd(self):
        cursor = self.conn.cursor()

        # Obter o esquema de todas as tabelas no banco de dados
        esquema_atual = {}
        tabelas = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence'").fetchall()
        for tabela in tabelas:
            nome_tabela = tabela[0]
            esquema_atual[nome_tabela] = self.obter_esquema_tabela(cursor, nome_tabela)

        # Comparar o esquema atual com o esquema de referência
        for tabela, colunas_referencia in self.esquema_referencia.items():
            if tabela not in esquema_atual:
                self.fechar_conexao()
                novo_nome = 'database'+self.tempo_atual_nome_arquivo()+'.db'
                os.rename('database.db', novo_nome)
                self.fazer_conexao()
                self.criar_bd_sqlite()
                return 1
            
            colunas_atual = esquema_atual[tabela]
            if colunas_atual != colunas_referencia:
                self.fechar_conexao()
                novo_nome = 'database'+self.tempo_atual_nome_arquivo()+'.db'
                os.rename('database.db', novo_nome)
                self.fazer_conexao()
                self.criar_bd_sqlite()
                return 1
        return 0

    def criar_bd_sqlite(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE vendas (
            id_venda INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            dt_hr_venda TEXT NOT NULL,
            quantidade NUMERIC DEFAULT (0) NOT NULL,
            vr_venda NUMERIC DEFAULT (0) NOT NULL,
            vr_total NUMERIC DEFAULT (0) NOT NULL,
            vr_pago NUMERIC DEFAULT (0) NOT NULL,
            vr_custo NUMERIC DEFAULT (0) NOT NULL,
            vr_troco NUMERIC DEFAULT (0) NOT NULL,
            CONSTRAINT vendas_produtos_FK FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE ON UPDATE CASCADE
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
            quantidade NUMERIC DEFAULT (0) NOT NULL, 
            vr_venda NUMERIC DEFAULT (0) NOT NULL, 
            vr_custo NUMERIC DEFAULT (0) NOT NULL,
            CONSTRAINT entradas_produtos_FK FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE ON UPDATE CASCADE
        );
               """)
        self.conn.commit()

    def fetch_data_from_db(self, table):
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT id_produto,
                            descricao,
                            unidade,
                            cast(round(quantidade, 3) as numeric(5,3)) quantidade,
                            cast(round(vr_venda, 2) as numeric(5,2)) vr_venda,
                            cast(round(vr_custo, 2) as numeric(5,2)) vr_custo
                        FROM {table}""")
        data = cursor.fetchall()
        return data
    
    def get_nome_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("select descricao from produtos")
        data = cursor.fetchall()
        return data

    def colunas(self, tabela):
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabela})")
        nomes_colunas = [row[1] for row in cursor.fetchall()]
        return nomes_colunas
    
    def adquirir_produto(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute(f"select * from produtos where id_produto = {id_produto};")
        r = cursor.fetchall()
        return r[0]
    
    def tempo_atual(self):
        # Obter o tempo atual
        tempo_agora = datetime.now()
        # Formatar o tempo no formato desejado
        tempo_formatado = tempo_agora.strftime("%Y-%m-%d %H:%M:%S")
        return tempo_formatado
    
    def tempo_atual_nome_arquivo(self):
        # Obter o tempo atual
        tempo_agora = datetime.now()
        # Formatar o tempo no formato desejado
        tempo_formatado = tempo_agora.strftime("%Y%m%d%H%M%S")
        return tempo_formatado

    def telaconsulta(self, produtos):
        headings = ["id_produto", "descricao", "quantidade"]
        layout_tela = [
            [sg.Button('Confirmar', font=self.tamanho_letra), sg.Button('Cancelar', font=self.tamanho_letra)],
            [sg.HorizontalSeparator()],
            [sg.Table(values=produtos, headings=headings, expand_x=True, expand_y=True, enable_events=True, key='tabela', font=self.tamanho_letra)],
        ]
        window = sg.Window("Seleção de produtos", layout_tela ,size=(600,600))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                window.close()
                return 0
            elif event == 'tabela' and values['tabela']:
                indice = values['tabela'][0]
                window.close()
                return produtos[indice][0]

    def window(self):
        produto_atual = None
        self.fazer_conexao()
        if self.verificar_integridade_bd():
            sg.Popup("Banco de dados novo criado por problemas na estrutura. Se for a primeira vez abrindo, ignore esse erro")
        cursor = self.conn.cursor()
        headings_produtos = self.colunas('produtos')
        data_produtos = self.fetch_data_from_db('produtos')
        # Definindo os layouts de cada aba
        layout_estoque = [
            [sg.Text('Estoque', font=self.tamanho_letra)],
            [sg.Table(values=data_produtos, headings=headings_produtos, key='tabela_estoque',
                    expand_x=True, expand_y=True, vertical_scroll_only=False, auto_size_columns=True, font=self.tamanho_letra, justification='left') ],
            [sg.Button('Atualizar', font=self.tamanho_letra)]]
        
        layout_entrada_l = [
            [sg.Text('Quantidade: ', font=self.tamanho_letra)],
            [sg.Text('Valor de custo: ', font=self.tamanho_letra)],
            [sg.Text('Margem bruta (%): ', font=self.tamanho_letra)],
            [sg.Text('Valor de venda calculado: ', font=self.tamanho_letra)],
            [sg.Text('Valor de venda a aplicar: ', font=self.tamanho_letra)],
        ]

        layout_entrada_r = [
            [sg.Input(key='quantidade_entrada_produtos', default_text=1, font=self.tamanho_letra)],
            [sg.Input(key='vr_custo_entrada_produtos', font=self.tamanho_letra)],
            [sg.Input(key='margem_entrada_produtos', default_text=0, enable_events=True, font=self.tamanho_letra)],
            [sg.Text('R$ 0,00', key='vr_calculado_entrada_produtos', font=self.tamanho_letra)],
            [sg.Input(key='vr_venda_entrada_produtos', font=self.tamanho_letra)],
        ]
        
        layout_entrada = [
            [sg.Text('Entrada no estoque dos produtos', font=self.tamanho_letra)],
            [sg.HorizontalSeparator()],
            [sg.Text("Produto: ", font=self.tamanho_letra), sg.Input(size=(50,1), key='input_entrada_produtos', font=self.tamanho_letra), sg.Button("...", key='consulta_entrada_produtos', font=self.tamanho_letra)],
            [sg.HorizontalSeparator()],
            [sg.Col(layout_entrada_l), sg.Col(layout_entrada_r)],
            [sg.Button('Salvar', key='salvar_entrada_produtos', font=self.tamanho_letra)]
        ]

        layout_venda = [
            [sg.Text('Venda (saída) de produtos', font=self.tamanho_letra)],
            [sg.HorizontalSeparator()],
            [sg.Text("Produto: ", font=self.tamanho_letra), sg.Input(size=(50,1), key='input_venda_produtos', font=self.tamanho_letra), sg.Button("...", key='consulta_venda_produtos', font=self.tamanho_letra)],
            [sg.Text("Quantidade: ", font=self.tamanho_letra), sg.Input(key='quantidade_venda_produtos', default_text=1, enable_events=True, font=self.tamanho_letra)],
            [sg.HorizontalSeparator()],
            [sg.Text("Valor total: ", font=self.tamanho_letra), sg.Text("R$ 0,00", key='vr_total_venda', font=self.tamanho_letra)],
            [sg.Text("Valor pago: ", font=self.tamanho_letra), sg.Input(key='vr_pago', enable_events=True, font=self.tamanho_letra)],
            [sg.Text("Troco: ", font=self.tamanho_letra), sg.Text("R$ 0,00", key='troco', font=self.tamanho_letra)],
            [sg.Button('Salvar', key='salvar_venda_produtos', font=self.tamanho_letra)]]

        layout_cadastro_l = [
            [sg.Text('Descrição: ', font=self.tamanho_letra)],
            [sg.Text('Unidade', font=self.tamanho_letra)],
            [sg.Text('Quantidade inicial', font=self.tamanho_letra)],
            [sg.Text('Valor de venda:', font=self.tamanho_letra)],
            [sg.Text('Valor de custo', font=self.tamanho_letra)],
        ]
        layout_cadastro_r = [
            [sg.Input(key='descricao', font=self.tamanho_letra)],
            [sg.Input(key='unidade', font=self.tamanho_letra)],
            [sg.Input(default_text='0', key='quantidade', font=self.tamanho_letra)],
            [sg.Input(key='vr_venda', font=self.tamanho_letra)],
            [sg.Input(key='vr_custo', font=self.tamanho_letra)],
        ]
        layout_cadastro = [
            [sg.Text('Cadastro de produtos', font=self.tamanho_letra)],
            [sg.Col(layout_cadastro_l), sg.Col(layout_cadastro_r)],
            [sg.Button("Salvar", key='salvar_cadastro', font=self.tamanho_letra)],
        ]
        layout_sobre = [
            [sg.Text("Desenvolvido por Fay Klagenberg", font=self.tamanho_letra)],
            [sg.Text("Versão 1.0 Alpha - 20/03/2024", font=self.tamanho_letra)],
            [sg.Text("Contato: (64) 99213-9766", font=self.tamanho_letra)],
        ]

        # Definindo a estrutura da janela com as abas
        layout = [[sg.TabGroup([[sg.Tab('Estoque', layout_estoque),
                                sg.Tab('Entrada de produtos', layout_entrada),
                                sg.Tab('Realizar Venda', layout_venda),
                                sg.Tab('Cadastro de produtos', layout_cadastro),
                                sg.Tab('Sobre', layout_sobre),
        ]], expand_x=True, expand_y=True, font=self.tamanho_letra)
                   ]]

        # Criando a janela
        window = sg.Window('Controle de estoque', layout, size=(1000, 600), finalize=True, resizable=True)
        window.maximize()

        # Loop de eventos
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                self.fechar_conexao()
                break
            elif event == 'Atualizar':
                data = self.fetch_data_from_db('produtos')
                window['tabela_estoque'].update(values=data)
            elif event == 'salvar_cadastro':
                cursor.execute(f"""insert into produtos(descricao, unidade, quantidade, vr_venda, vr_custo) values('{values['descricao']}',
                               '{values['unidade']}', {float(values['quantidade'])}, {float(values['vr_venda'])}, {float(values['vr_custo'])});""")
                self.conn.commit()
                window['descricao'].update(value='')
                window['unidade'].update(value='')
                window['quantidade'].update(value='')
                window['vr_venda'].update(value='')
                window['vr_custo'].update(value='')
                data = self.fetch_data_from_db('produtos')
                window['tabela_estoque'].update(values=data)
                data = self.fetch_data_from_db('produtos')
                window['tabela_estoque'].update(values=data)
                sg.popup("Cadastro realizado com sucesso!")
            elif event == 'consulta_entrada_produtos':
                cursor.execute(f"select id_produto, descricao, quantidade from produtos where descricao like '%{values['input_entrada_produtos']}%';")
                selecionado = self.telaconsulta(cursor.fetchall())
                if selecionado==0:
                    continue
                produto_atual = self.adquirir_produto(selecionado)
                window['input_entrada_produtos'].update(value=produto_atual[1])
                window['vr_custo_entrada_produtos'].update(value = produto_atual[5])
                window['vr_venda_entrada_produtos'].update(value = produto_atual[4])
                calculo_com_margem = produto_atual[5] + (produto_atual[5] * (float(values['margem_entrada_produtos'])/100))
                window['vr_calculado_entrada_produtos'].update(value = f'R$ {calculo_com_margem}')
            elif event == 'margem_entrada_produtos':
                if produto_atual:
                    if values['margem_entrada_produtos']:
                        calculo_com_margem = produto_atual[5] + (produto_atual[5] * (float(values['margem_entrada_produtos'])/100))
                        window['vr_calculado_entrada_produtos'].update(value = f'R$ {calculo_com_margem}')
            elif event == 'salvar_entrada_produtos':
                cursor.execute(f'''update produtos set 
                               quantidade={produto_atual[3]+float(values['quantidade_entrada_produtos'])}, 
                               vr_venda={float(values['vr_venda_entrada_produtos'])}, 
                               vr_custo={float(values['vr_custo_entrada_produtos'])} 
                               where id_produto={produto_atual[0]};''')
                cursor.execute(f"""insert into entradas (id_produto, dt_hr_entrada, quantidade, vr_venda, vr_custo)
                               values ({produto_atual[0]}, '{self.tempo_atual()}', {float(values['quantidade_entrada_produtos'])}, 
                               {float(values['vr_venda_entrada_produtos'])}, {float(values['vr_custo_entrada_produtos'])})""")
                window['quantidade_entrada_produtos'].update(value = 1)
                window['vr_custo_entrada_produtos'].update(value = '')
                window['margem_entrada_produtos'].update(value = 0)
                window['vr_venda_entrada_produtos'].update(value = '')
                window['vr_calculado_entrada_produtos'].update(value = 'R$ 0.00')
                self.conn.commit()
                data = self.fetch_data_from_db('produtos')
                window['tabela_estoque'].update(values=data)
                sg.Popup("Entrada realizada com sucesso!")
            elif event == 'consulta_venda_produtos':
                cursor.execute(f"select id_produto, descricao, quantidade from produtos where descricao like '%{values['input_venda_produtos']}%';")
                selecionado = self.telaconsulta(cursor.fetchall())
                if selecionado==0:
                    continue
                produto_atual = self.adquirir_produto(selecionado)
                window['input_venda_produtos'].update(value=produto_atual[1])
                if values['quantidade_venda_produtos']:
                    valor_total = produto_atual[4] * int(values['quantidade_venda_produtos'])
                    window['vr_total_venda'].update(value = f'R$ {float(valor_total)}')
            elif event == 'quantidade_venda_produtos':
                if values['quantidade_venda_produtos']:
                    valor_total = produto_atual[4] * int(values['quantidade_venda_produtos'])
                    window['vr_total_venda'].update(value = f'R$ {float(valor_total)}')
                    if values['vr_pago']:
                        valor_troco = float(values['vr_pago']) - valor_total
                        window['troco'].update(value = f'R$ {valor_troco}')
            elif event == 'vr_pago':
                if values['quantidade_venda_produtos']:
                    valor_total = produto_atual[4] * int(values['quantidade_venda_produtos'])
                    window['vr_total_venda'].update(value = f'R$ {float(valor_total)}')
                    if values['vr_pago']:
                        valor_troco = float(values['vr_pago']) - valor_total
                        window['troco'].update(value = f'R$ {valor_troco}')
            elif event == 'salvar_venda_produtos':
                cursor.execute(f'''update produtos set 
                               quantidade={produto_atual[3]-float(values['quantidade_venda_produtos'])}
                               where id_produto={produto_atual[0]};''')
                cursor.execute(f"""insert into vendas (id_produto, dt_hr_venda, quantidade, vr_venda, vr_pago, vr_total, vr_custo, vr_troco)
                               values ({produto_atual[0]}, '{self.tempo_atual()}', {float(values['quantidade_venda_produtos'])}, {produto_atual[4]}, {float(values['vr_pago'])}, {valor_total}, {produto_atual[5]}, {valor_troco})""")
                window['input_venda_produtos'].update(value = '')
                window['quantidade_venda_produtos'].update(value = 1)
                window['vr_total_venda'].update(value = 'R$ 0,00')
                window['vr_pago'].update(value = 0)
                self.conn.commit()
                data = self.fetch_data_from_db('produtos')
                window['tabela_estoque'].update(values=data)
                sg.Popup("Venda realizada com sucesso!")
        window.close()

main().window()
