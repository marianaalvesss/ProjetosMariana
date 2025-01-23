import pyodbc
import re
from datetime import datetime

def conectar_bd():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-4JDM2AGL\SQLEXPRESS2022;'
            'DATABASE=levantamento_livros;'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def livro_existe(nome_livro, autor, editora):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        query = '''
        SELECT COUNT(*) 
        FROM estante 
        WHERE nome_livro = ? AND autor = ? AND editora = ?
        '''
        cursor.execute(query, (nome_livro, autor, editora))
        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado > 0
    return False

def inserir_livro(dados_livro):
    dados_livro = re.split(r'\s*-\s*', dados_livro)

    dados_livro = [dado.strip() for dado in dados_livro]

    if len(dados_livro) != 12:
        print(f"Erro: É necessário fornecer exatamente 12 valores. Foram recebidos {len(dados_livro)} valores.")
        return

    nome_livro, autor, genero, numero_paginas, editora, data_compra, valor_compra, valor_atual, status, data_concluido, formato, nota = dados_livro
    print(f"Valores a serem inseridos: nome_livro={nome_livro}, autor={autor}, genero={genero}, numero_paginas={numero_paginas}, editora={editora}, data_compra={data_compra}, valor_compra={valor_compra}, valor_atual={valor_atual}, status={status}, data_concluido={data_concluido}, formato={formato}, nota={nota}")

    try:
        if livro_existe(nome_livro, autor, editora):
            print(f"Erro: O livro '{nome_livro}' de {autor} publicado pela {editora} já está cadastrado.")
            return

        numero_paginas = int(numero_paginas)
        valor_compra = float(valor_compra.replace(',', '.'))
        valor_atual = float(valor_atual.replace(',', '.'))
        
        data_compra = datetime.strptime(data_compra, "%d/%m/%Y").date()

        if status.lower() == 'não lido':
            data_concluido = None
            formato = None
            nota = None
        else:
            if data_concluido and data_concluido.strip().lower() != "null":
                data_concluido = datetime.strptime(data_concluido, "%d/%m/%Y").date()
            else:
                data_concluido = None
            
            if nota and nota.strip().lower() != "null":
                nota = int(nota)
            else:
                nota = None

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO estante (nome_livro, autor, genero, numero_paginas, editora, data_compra, valor_compra, valor_atual, status, data_concluido, formato, nota)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome_livro, autor, genero, numero_paginas, editora, data_compra, valor_compra, valor_atual, status, data_concluido, formato, nota))

            conn.commit()
            print("Livro inserido com sucesso!")
        else:
            print("Erro ao conectar ao banco de dados.")
    except Exception as e:
        print(f"Erro ao inserir o livro: {e}")

def consultar_livros():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estante")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()
    else:
        print("Erro ao conectar ao banco de dados.")

# Menu
def menu():
    while True:
        print("\nMenu:")
        print("1. Cadastrar novo livro")
        print("2. Consultar livros existentes")
        print("9. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            dados_livro = input("Digite os dados do livro no formato: Nome - Autor - Gênero - Número de páginas - Editora - Data de compra (dd/mm/aaaa) - Valor de compra - Valor atual - Status - Data concluído (dd/mm/aaaa) ou null - Formato ou null - Nota ou null:\n")
            inserir_livro(dados_livro)
        elif escolha == '2':
            consultar_livros()
        elif escolha == '9':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

menu()
