import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aula_id INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    FOREIGN KEY (aula_id) REFERENCES aulas(id),
    FOREIGN KEY (id_aluno) REFERENCES alunos(id)
)
''')

conexao.commit()


def cancelar_aula():
    try:
        id_agendamento = int(input("Digite o id do agendamento: "))

        cursor.execute("""
            SELECT * FROM agendamentos
            WHERE id = ?
        """, (id_agendamento,))

        agendamento = cursor.fetchone()

        if agendamento:
            cursor.execute("""
                DELETE FROM agendamentos
                WHERE id = ?
            """, (id_agendamento,))

            conexao.commit()
            print("Agendamento cancelado com sucesso!")

        else:
            print("Agendamento não encontrado.")

    except ValueError:
        print("Digite um número válido.")


cancelar_aula()