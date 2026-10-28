import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()
conexao = None


try:
    def criar_tabela():

        cursor.execute("PRAGMA foreign_keys = ON;")


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            idade INTEGER NOT NULL,
            plano TEXT NOT NULL
        )
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS personais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recepcionistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
        )
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gerentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            cpf TEXT NOT NULL,
            plano_aluno TEXT NOT NULL,
            FOREIGN KEY (plano_aluno) REFERENCES alunos(plano)
        )
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS presencas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            id_personal INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            treino TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            id_personal INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        )
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS aulas_experimentais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT,
            data TEXT,
            horario TEXT,
            status TEXT,
            id_aluno INTEGER NOT NULL,
            id_personal INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        )
        ''')



        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensalidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT,
            valor REAL,
            status TEXT,
            dias_atraso INTEGER,
            id_aluno INTEGER NOT NULL,
            id_personal INTEGER NOT NULL,
            plano_aluno TEXT NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id),
            FOREIGN KEY (plano_aluno) REFERENCES alunos(plano)
        )
        ''')


        print("Tabelas criadas com sucesso!")



    except sqlite3.Error as e:
        print("Erro no banco de dados!", e) 

    finally:
        if conexao:
            conexao.commit() 
            conexao.close()



def cadastro_alunos():
    print("---------CADASTRO DE ALUNOS---------")

    try:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        idade = int(input("Idade: "))
        plano = input("Plano: ")

        cursor.execute('''
        INSERT INTO alunos (nome, cpf, telefone, idade, plano)
        VALUES (?, ?, ?, ?, ?)
        ''')

        print("Aluno cadastrado com sucesso!")

        conexao.commit()

    except ValueError as e:
        print("Digite apenas nomes! ", e)
    except sqlite3.IntegrityError as e:
        print("Erro! Informações já cadastradas! ", e) 


    print("Aluno cadastrado com sucesso!")


def listar_alunos():

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    for aluno in alunos:

        print("-----ALUNOS CADASTRADOS-----")
        print("ID:", aluno[0])
        print("Nome:", aluno[1])
        print("CPF:", aluno[2])
        print("Telefone:", aluno[3])
        print("Idade:", aluno[4])
        print("Plano:", aluno[5])



def atualizar_aluno():
    listar_alunos()


    try:
        id_aluno = int(input("Insira o id do aluno que deseja alterar: "))
        novo_plano = input("Informe o novo plano: ")
        cursor.execute("UPDATE cadastrar_alunos SET nome = ?, plano = ? WHERE id = ?", (novo_plano))

        conexao.commit()
        print("Nome atualizado com sucesso!")

    except sqlite3.Error as e:
        print("Não foi possivel atualizar!", e)

    print("Aluno atualizado!")

def excluir_aluno():

    cpf = input("CPF do aluno: ")

    cursor.execute('''
    DELETE FROM alunos
    WHERE cpf = ?
    ''', (cpf,))

    conexao.commit()

    print("Aluno excluído!")


def cadastrar_personais():
    

