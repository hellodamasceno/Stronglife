import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS presencas (
        id_presenca INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER NOT NULL,
        data_hora TEXT NOT NULL,
        FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
    )
''')

conexao.commit()


def registrar_presenca_aluno():
    id_aluno = int(input("Digite o id do aluno: "))
    data_hora = input("Digite a data e a hora da presença: ")

    cursor.execute('''
        INSERT INTO presencas (id_aluno, data_hora)
        VALUES (?, ?)
    ''', (id_aluno, data_hora))

    conexao.commit()
    print("Presença registrada com sucesso!")


def consultar_presencas():
    cursor.execute('''
        SELECT * FROM presencas
    ''')

    presencas = cursor.fetchall()

    if len(presencas) == 0:
        print("Nenhuma presença registrada.")
    else:
        for presenca in presencas:
            print(presenca)


registrar_presenca_aluno()
consultar_presencas()

conexao.close()