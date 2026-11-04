import sqlite3

def criar_tabela():
    try:
        conexao = sqlite3.connect('teste1.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS personais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT NOT NULL,
            idade INTEGER NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            mensalidade REAL NOT NULL,
            id_personal INTEGER,
            dia_aula TEXT,
            horario_aula TEXT,
            status_acompanhamento TEXT,
            plano TEXT,
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recepcionistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
        ) ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gerentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            id_aluno INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
        ) ''')

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
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            treino TEXT NOT NULL,
            id_aluno INTEGER NOT NULL,
            id_personal INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        ) ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS aulas_experimentais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT,
            data TEXT,
            horario TEXT,
            status TEXT,
            cpf TEXT NOT NULL,
            id_aluno INTEGER,
            id_personal INTEGER,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_personal) REFERENCES personais(id)
        ) ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensalidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT,
            valor REAL,
            status TEXT,
            dias_atraso INTEGER,
            id_aluno INTEGER NOT NULL,
            plano_aluno TEXT NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
        ) ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos_diarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno INTEGER NOT NULL,
            dia_semana TEXT NOT NULL,
            id_exercicio INTEGER NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id),
            FOREIGN KEY (id_exercicio) REFERENCES exercicios(id)
        )''')
        
        conexao.commit()
        print("Tabelas criadas com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conexao.close()

def cadastrar_aluno():
    
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n----CADASTRO DE ALUNO----")
        nome = input("Nome do aluno: ")
        idade = int(input("Idade do aluno: "))
        cpf = input("CPF do aluno: ")
        mensalidade = float(input("Qual o valor do plano?: "))
        
        cursor.execute("""
            INSERT INTO alunos (nome_aluno, idade, cpf, mensalidade) 
            VALUES (?, ?, ?, ?)
        """, (nome, idade, cpf, mensalidade))
        
        conexao.commit()
        print(f"Aluno '{nome}' cadastrado com sucesso!")
    except ValueError:
        print("Erro: Idade e mensalidade devem ser apenas números!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar aluno: {e}")
    finally:
        conexao.close()

def cadastrar_personal():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n----CADASTRO DE PERSONAL----")
        nome = input("Nome do personal: ")
        cpf = input("CPF personal: ")
        telefone = input("Telefone do personal: ") 

        cursor.execute("INSERT INTO personais (nome, cpf, telefone) VALUES (?, ?, ?)", (nome, cpf, telefone))
        
        conexao.commit()
        print(f"Personal '{nome}' cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar personal: {e}")
    finally:
        conexao.close()

def listar_aluno():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        
        print("\n----LISTA DE ALUNOS----")
        cursor.execute("SELECT * FROM alunos;")
        alunos = cursor.fetchall() 

        if not alunos:
            print("Nenhum aluno cadastrado no momento.")
            return
            
        for a in alunos:
            print(f"ID: {a[0]} | NOME: {a[1]} | Idade: {a[2]} | CPF: {a[3]} | Mensalidade: R${a[4]:.2f}")
    except sqlite3.Error as e:
        print(f"Erro ao listar alunos: {e}")
    finally:
        conexao.close()

def listar_personal():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        
        print("\n---- LISTA DE PERSONAIS ----")
        cursor.execute("SELECT id, nome, cpf, telefone FROM personais;")
        personais = cursor.fetchall()
        
        if not personais:
            print("Nenhum personal cadastrado no momento.")
            return
            
        for p in personais:
            print(f"ID: {p[0]} | NOME: {p[1]} | CPF: {p[2]} | TELEFONE: {p[3]}")
    except sqlite3.Error as e:
        print(f"Erro ao listar personais: {e}")
    finally:
        conexao.close()

def deletar_aluno():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR ALUNO ----")
        id_aluno = int(input("Digite o ID do aluno que deseja deletar: "))

        cursor.execute("SELECT nome_aluno FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()
        
        if aluno:
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
            conexao.commit()
            print(f"Aluno '{aluno[0]}' removido com sucesso!")
        else:
            print("Erro: Aluno não encontrado com o ID informado.")
            
    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar aluno: {e}")
    finally:
        conexao.close()

def deletar_personal():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR PERSONAL ----")
        id_personal = int(input("Digite o ID do personal que deseja deletar: "))

        cursor.execute("SELECT nome FROM personais WHERE id = ?", (id_personal,))
        personal = cursor.fetchone()
        
        if personal:
            cursor.execute("DELETE FROM personais WHERE id = ?", (id_personal,))
            conexao.commit()
            print(f"Personal '{personal[0]}' removido com sucesso!")
        else:
            print("Erro: Personal não encontrado com o ID informado.")
            
    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")
    except sqlite3.IntegrityError:
        print("Erro: Não é possível deletar este personal pois ele está vinculado a um ou mais alunos!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar personal: {e}")
    finally:
        conexao.close()

def aula_experimental():
    try:
        conexao = sqlite3.connect('sistem_academia.db')
        cursor = conexao.cursor()
        
        print("\n---AULAS EXPERIMENTAIS---")
        nome = input("Nome do aluno: ")
        data = input("Data (DD/MM/AAAA): ")
        horario = input("Horário (HH:MM): ")
        cpf = input("CPF do aluno: ")

        cursor.execute("SELECT * FROM aulas_experimentais WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"Aluno com CPF {cpf} já possui aula experimental marcada!")
        else:
            cursor.execute("""
                INSERT INTO aulas_experimentais (aluno, data, horario, status, cpf) 
                VALUES (?, ?, ?, ?, ?)
            """, (nome, data, horario, "Agendado", cpf))
            conexao.commit()
            print(f"Aula experimental marcada com sucesso para {nome}!")
            
    except sqlite3.Error as e:
        print(f"ERRO no banco de dados: {e}")
    finally:
        conexao.close()

def menu():
criar_tabela()
    
    while True:
        print("\n ----- MENU RECEPCIONISTA ----- ")
        print("1. Cadastrar aluno.")
        print("2. Cadastrar personal.")
        print("3. Listar alunos.")
        print("4. Listar personais.") 
        print("5. Deletar aluno.") 
        print("6. Deletar personal.") 
        print("7. Aulas experimentais.")
        print("8. Sair.")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            cadastrar_personal()
        elif opcao == "3":
            listar_aluno()
        elif opcao == "4":
            listar_personal()
        elif opcao == "5":
            deletar_aluno()
        elif opcao == "6":
            deletar_personal()
        elif opcao == "7":
            aula_experimental()
        elif opcao == "8":
            print("Encerrando o sistema... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente!")

menu()