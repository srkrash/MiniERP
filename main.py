import PySimpleGUI as sg
import sqlite3


class main:
    def __init__(self) -> None:
        self.conn = None

    def fazer_conexao(self):
        self.conn = sqlite3.connect('database.db')

    def fechar_conexao(self):
        self.conn.close()

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

    def window(self):
        self.fazer_conexao()
        cursor = self.conn.cursor()
        headings_produtos = self.colunas('produtos')
        data_produtos = self.fetch_data_from_db('produtos')
        nome_produtos = self.get_nome_produtos()
        # Definindo os layouts de cada aba
        layout_estoque = [[sg.Text('Estoque')],
                          [sg.Table(values=data_produtos, headings=headings_produtos, key='tabela_estoque',
                                    expand_x=True, expand_y=True, vertical_scroll_only=False, auto_size_columns=True)],
                          [sg.Button('Atualizar')]]

        layout_entrada = [[sg.Text('Entrada no estoque dos produtos')],
                          [sg.Input(size=(25,1)), sg.Button("...")],
                          [sg.Button('Enviar', key='-BUTTON2-')]]

        layout_venda = [[sg.Text('Conteúdo da Aba 3')],
                        [sg.Input(key='-INPUT3-')],
                        [sg.Button('Enviar', key='-BUTTON3-')]]

        layout_cadastro_l = [
            [sg.Text('Descrição: ')],
            [sg.Text('Unidade')],
            [sg.Text('Quantidade inicial')],
            [sg.Text('Valor de venda:')],
            [sg.Text('Valor de custo')],
        ]
        layout_cadastro_r = [
            [sg.Input(key='descricao')],
            [sg.Input(key='unidade')],
            [sg.Input(default_text='0', key='quantidade')],
            [sg.Input(key='vr_venda')],
            [sg.Input(key='vr_custo')],
        ]
        layout_cadastro = [
            [sg.Text('Cadastro de produtos')],
            [sg.Col(layout_cadastro_l), sg.Col(layout_cadastro_r)],
            [sg.Button("Salvar", key='salvar_cadastro')],
        ]

        # Definindo a estrutura da janela com as abas
        layout = [[sg.TabGroup([[sg.Tab('Estoque', layout_estoque),
                                sg.Tab('Entrada de produtos', layout_entrada),
                                sg.Tab('Realizar Venda', layout_venda),
                                sg.Tab('Cadastro de produtos', layout_cadastro)]], expand_x=True, expand_y=True)
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
                sg.popup("Cadastro realizado com sucesso!")
            #elif event ==''

        window.close()


main().window()
