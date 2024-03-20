import PySimpleGUI as sg
import sqlite3
from datetime import datetime


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

    def telaconsulta(self, produtos):
        headings = ["id_produto", "descricao", "quantidade"]
        layout_tela = [
            [sg.Button('Confirmar'), sg.Button('Cancelar')],
            [sg.HorizontalSeparator()],
            [sg.Table(values=produtos, headings=headings, expand_x=True, expand_y=True, enable_events=True, key='tabela')],
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
        cursor = self.conn.cursor()
        headings_produtos = self.colunas('produtos')
        data_produtos = self.fetch_data_from_db('produtos')
        # Definindo os layouts de cada aba
        layout_estoque = [
            [sg.Text('Estoque')],
            [sg.Table(values=data_produtos, headings=headings_produtos, key='tabela_estoque',
                    expand_x=True, expand_y=True, vertical_scroll_only=False, auto_size_columns=True)],
            [sg.Button('Atualizar')]]
        
        layout_entrada_l = [
            [sg.Text('Quantidade: ')],
            [sg.Text('Valor de custo: ')],
            [sg.Text('Margem bruta (%): ')],
            [sg.Text('Valor de venda calculado: ')],
            [sg.Text('Valor de venda a aplicar: ')],
        ]

        layout_entrada_r = [
            [sg.Input(key='quantidade_entrada_produtos', default_text=1)],
            [sg.Input(key='vr_custo_entrada_produtos')],
            [sg.Input(key='margem_entrada_produtos', default_text=0, enable_events=True)],
            [sg.Text('R$ 0,00', key='vr_calculado_entrada_produtos')],
            [sg.Input(key='vr_venda_entrada_produtos')],
        ]
        
        layout_entrada = [
            [sg.Text('Entrada no estoque dos produtos', font=(36))],
            [sg.HorizontalSeparator()],
            [sg.Text("Produto: "), sg.Input(size=(50,1), key='input_entrada_produtos'), sg.Button("...", key='consulta_entrada_produtos')],
            [sg.HorizontalSeparator()],
            [sg.Col(layout_entrada_l), sg.Col(layout_entrada_r)],
            [sg.Button('Salvar', key='salvar_entrada_produtos')]
        ]

        layout_venda = [
            [sg.Text('Venda (saída) de produtos', font=(36))],
            [sg.HorizontalSeparator()],
            [sg.Text("Produto: "), sg.Input(size=(50,1), key='input_venda_produtos'), sg.Button("...", key='consulta_venda_produtos')],
            [sg.Text("Quantidade: "), sg.Input(key='quantidade_venda_produtos', default_text=1, enable_events=True)],
            [sg.HorizontalSeparator()],
            [sg.Text("Valor total: "), sg.Text("R$ 0,00", key='vr_total_venda')],
            [sg.Text("Valor pago: "), sg.Input(key='vr_pago')],
            [sg.Text("Troco: "), sg.Text("R$ 0,00", key='troco')],
            [sg.Button('Salvar', key='salvar_venda_produtos')]]

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
        layout_sobre = [
            [sg.Text("Desenvolvido por Fay Klagenberg")],
            [sg.Text("Versão 1.0 Alpha - 20/03/2024")],
            [sg.Text("Contato: (64) 99213-9766")],
        ]

        # Definindo a estrutura da janela com as abas
        layout = [[sg.TabGroup([[sg.Tab('Estoque', layout_estoque),
                                sg.Tab('Entrada de produtos', layout_entrada),
                                sg.Tab('Realizar Venda', layout_venda),
                                sg.Tab('Cadastro de produtos', layout_cadastro),
                                sg.Tab('Sobre', layout_sobre),
        ]], expand_x=True, expand_y=True)
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
                tempo_atual = self.tempo_atual()
                cursor.execute(f"""insert into entradas (id_produto, dt_hr_entrada, quantidade)
                               values ({produto_atual[0]}, '{self.tempo_atual()}', {float(values['quantidade_entrada_produtos'])})""")
                window['quantidade_entrada_produtos'].update(value = 1)
                window['vr_custo_entrada_produtos'].update(value = '')
                window['margem_entrada_produtos'].update(value = 0)
                window['vr_venda_entrada_produtos'].update(value = '')
                window['vr_calculado_entrada_produtos'].update(value = 'R$ 0.00')
                self.conn.commit()
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
                    valor_troco = float(values['vr_pago']) - valor_total
                    window['vr_total_venda'].update(value = f'R$ {float(valor_total)}')
                    window['troco'].update(value = f'R$ {valor_troco}')

        window.close()

main().window()
