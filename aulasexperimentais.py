import sqlite3

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


agendar_aula()