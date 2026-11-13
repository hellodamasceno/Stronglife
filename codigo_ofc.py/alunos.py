import sqlite3
from personal import visualizar_ficha_aluno


conexao = sqlite3.connect("sistema_academia.db")
cursor = conexao.cursor()


def agendar_aula():

    print("\n>>> AGENDAR AULA EXPERIMENTAL <<<")

    cpf = input("Digite o CPF: ")


    cursor.execute("SELECT * FROM alunos WHERE cpf = ?", (cpf,))
    aluno = cursor.fetchone()

    if aluno:
        print("Esta pessoa já está cadastrada como aluno!")
        return

    nome = input("Digite o nome: ")


    cursor.execute('''
    SELECT * FROM aulas_experimentais
    WHERE cpf = ?
    ''', (cpf,))

    aula = cursor.fetchone()

    if aula:
        print("Esta pessoa já possui uma aula experimental agendada!")
        return

    data = input("Digite a data da aula: ")
    horario = input("Digite o horário da aula: ")

    cursor.execute('''
    INSERT INTO aulas_experimentais (cpf, nome, data, horario)
    VALUES (?, ?, ?, ?)
    ''', (cpf, nome, data, horario))

    conexao.commit()

    print("Aula experimental agendada com sucesso!")


def remarcar_aula():

    print("\n>>> REMARCAR AULA EXPERIMENTAL <<<")

    cpf = input("Digite o CPF: ")

    cursor.execute('''
    SELECT * FROM aulas_experimentais
    WHERE cpf = ?
    ''', (cpf,))

    aula = cursor.fetchone()

    if aula:
        print("\nAgendamento encontrado!")
        print("Nome:", aula[2])
        print("Data atual:", aula[3])
        print("Horário atual:", aula[4])

        nova_data = input("\nDigite a nova data: ")
        novo_horario = input("Digite o novo horário: ")

        cursor.execute('''
        UPDATE aulas_experimentais
        SET data = ?, horario = ?
        WHERE cpf = ?
        ''', (nova_data, novo_horario, cpf))

        conexao.commit()

        print("Aula remarcada com sucesso!")

    else:
        print("Nenhuma aula experimental encontrada para este CPF.")



def cancelar_aula():

    print("\n>>> CANCELAR AULA EXPERIMENTAL <<<")

    cpf = input("Digite o CPF: ")

    cursor.execute('''
    SELECT * FROM aulas_experimentais
    WHERE cpf = ?
    ''', (cpf,))

    aula = cursor.fetchone()

    if aula:
        print("\nAgendamento encontrado!")
        print("Nome:", aula[2])
        print("Data:", aula[3])
        print("Horário:", aula[4])

        confirmar = input("\nDeseja realmente cancelar? (S/N): ")

        if confirmar == "S" or confirmar == "s":

            cursor.execute('''
            DELETE FROM aulas_experimentais
            WHERE cpf = ?
            ''', (cpf,))

            conexao.commit()

            print("Aula cancelada com sucesso!")

        else:
            print("Cancelamento não realizado.")

    else:
        print("Nenhuma aula experimental encontrada para este CPF.")


import sqlite3


def visualizar_minha_ficha():
    conexao = sqlite3.connect("sistema_academia.db")
    cursor = conexao.cursor()

    print("\n--- MINHA FICHA ---")

    id_aluno = int(input("Informe o seu ID: "))

    cursor.execute(
        """
        SELECT
            alunos.nome_aluno,
            alunos.idade,
            alunos.status_acompanhamento,
            alunos.dia_aula,
            alunos.horario_aula,
            personais.nome,
            alunos.plano
        FROM alunos
        LEFT JOIN personais ON alunos.id_personal = personais.id
        WHERE alunos.id = ?
        """,
        (id_aluno,),
    )

    dados = cursor.fetchone()

    match dados:
        case None:
            print("Ficha não encontrada!")
            conexao.close()
            return

        case _:
            print("\n----------------------------------------")
            print("Nome:", dados[0])
            print("Idade:", dados[1], "anos")
            print("Status:", dados[2])
            print("Personal:", dados[5])
            print("Plano:", dados[6])
            print("Dia da aula:", dados[3])
            print("Horário:", dados[4])
            print("----------------------------------------")

    cursor.execute(
        """
        SELECT treinos_diarios.dia_semana, exercicios.nome
        FROM treinos_diarios
        JOIN exercicios ON treinos_diarios.id_exercicio = exercicios.id
        WHERE treinos_diarios.id_aluno = ?
        """,
        (id_aluno,),
    )

    treinos = cursor.fetchall()

    match treinos:
        case []:
            print("\nVocê ainda não tem treinos cadastrados.")

        case _:
            print("\n--- MEUS TREINOS ---")
            for treino in treinos:
                print(treino[0], "-", treino[1])

    print("----------------------------------------")
    conexao.close()