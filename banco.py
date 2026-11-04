import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()




def criar_tabela():

    cursor.execute("PRAGMA foreign_keys = ON;")


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_aluno TEXT NOT NULL,
        idade INTEGER NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        mensalidade REAL NOT NULL,
        id_personal INTEGER NOT NULL,
        dia_aula TEXT NOT NULL,
        horario_aula TEXT NOT NULL,
        status_acompanhamento TEXT NOT NULL,
<<<<<<< HEAD
        FOREIGN KEY (id_personal) REFERENCES personal(id) 
=======
        plano TEXT NOT NULL,
        FOREIGN KEY (id_personal) REFERENCES personais(id) 
>>>>>>> 9ac47d45355ceb9b3597457c8ed8174765170b13
    )''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        telefone TEXT NOT NULL
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
        cpf TEXT NOT NULL UNIQUE,
        id_aluno INTEGER NOT NULL,
        FOREIGN KEY (id_aluno) REFERENCES alunos(id)
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
        plano_aluno TEXT NOT NULL,
        FOREIGN KEY (id_aluno) REFERENCES alunos(id),
        FOREIGN KEY (plano_aluno) REFERENCES alunos(plano)
    )
    ''')

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
            FOREIGN KEY (id_exercicio) REFERENCES exercicios(id) JA tem tabela
        )''')

    conexao.commit()
    print("Tabelas criadas com sucesso!")
