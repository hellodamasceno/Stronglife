import sqlite3
from personal import 


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




























def menu_alunos():
    while True:
        print("\n====== ÁREA DO ALUNO ======")
        print("1 - Agendar aula experimental")
        print("2 - Atualizar aula experimental")
        print("3 - Remarcar aula experimental")
        print("4 - Visualizar meu treino")
        print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    match opcao:
        case "1":

