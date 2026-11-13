
import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()


def criar_tabela():

    # Ativar chaves estrangeiras
    cursor.execute("PRAGMA foreign_keys = ON")

    # =====================================
    # TABELA PERSONAIS
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        telefone TEXT NOT NULL
    )
    ''')

    # =====================================
    # TABELA PLANOS
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS planos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        duracao INTEGER NOT NULL
    )
    ''')

    # =====================================
    # TABELA ALUNOS
    # =====================================

    cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_aluno TEXT NOT NULL,
    idade INTEGER NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    mensalidade REAL NOT NULL,
    id_personal INTEGER NOT NULL,
    dia_aula TEXT,
    horario_aula TEXT,
    status_acompanhamento TEXT,
    id_plano INTEGER NOT NULL,

    FOREIGN KEY (id_personal) REFERENCES personais(id),
    FOREIGN KEY (id_plano) REFERENCES planos(id)
)
    ''')

    # =====================================
    # TABELA MENSALIDADES
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mensalidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER NOT NULL,
        plano TEXT NOT NULL,
        valor REAL NOT NULL,
        status TEXT NOT NULL,
        dias_atraso INTEGER DEFAULT 0,

        FOREIGN KEY (id_aluno) REFERENCES alunos(id)
    )
    ''')

    # =====================================
    # TABELA RECEPCIONISTAS
    # =====================================

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

    # =====================================
    # TABELA GERENTES
    # =====================================

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

    # =====================================
    # TABELA PRESENCAS
    # =====================================

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
    )
    ''')

    # =====================================
    # TABELA TREINOS
    # =====================================

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

    # =====================================
    # TABELA AULAS EXPERIMENTAIS
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aulas_experimentais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno TEXT,
        data TEXT,
        cpf TEXT,
        horario TEXT,
        status TEXT,
        id_aluno INTEGER NOT NULL,
        id_personal INTEGER NOT NULL,

        FOREIGN KEY (id_aluno) REFERENCES alunos(id),
        FOREIGN KEY (id_personal) REFERENCES personais(id)
    )
    ''')

    # =====================================
    # TABELA EXERCICIOS
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    ''')

    # =====================================
    # TABELA TREINOS DIARIOS
    # =====================================

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treinos_diarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER NOT NULL,
        dia_semana TEXT NOT NULL,
        id_exercicio INTEGER NOT NULL,

        FOREIGN KEY (id_aluno) REFERENCES alunos(id),
        FOREIGN KEY (id_exercicio) REFERENCES exercicios(id)
    )
    ''')

    conexao.commit()

    print("Tabelas criadas com sucesso!")

criar_tabela()

