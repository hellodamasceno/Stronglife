import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()


def criar_tabelas_recepcao_gerencia():
    conexao = sqlite3.connect('sistema_academia.db')
    cursor = conexao.cursor()
    conexao = None

    try: 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gerentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cpf TEXT NOT NULL
            )
            ''')


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recepcionistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL 
            )
            ''')

    except sqlite3.Error as e:
        print("Erro no banco de dados!", e) 

     finally:
        if conexao:
            conexao.commit() 
            conexao.close()

criar_tabelas_recepcao_gerencia()

def cadastrar_gerentes():
    try:
        nome_gerente = input("Informe o nome do gerente: ")
        telefone_gerente = input("Insira o numero de telefone: ")
        cpf = input("Infore o CPF: ")

        comando_inserir = "INSERT INTO gerentes (nome_gerente, telefone_gerente, cpf) VALUES (?, ?)"

        cursor.execute(comando_inserir, (nome_gerente, telefone_gerente, cpf))
        conexao.commit()
        print("Cadastro concluido")

    except ValueError as e:
        print("Digite apenas nomes! ", e)
    except sqlite3.IntegrityError as e:
        print("Erro! Informações já cadastradas! ", e)

    finally:
        conexao.close
  

criar_tabelas_recepcao_gerencia()
cadastrar_gerentes()
