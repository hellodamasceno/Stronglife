import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()


def criar_aula():

    nome = input("Digite o nome da aula: ")
    professor = input("Digite o nome do professor: ")
    data = input("Digite a data: ")
    hora = input("Digite a hora: ")
    vagas = int(input("Digite o número de vagas: "))

    cursor.execute("""
        INSERT INTO aulas (nome, professor, data, hora, vagas)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, professor, data, hora, vagas))

    conexao.commit()

    print("Aula criada com sucesso!")

def listar_aulas():

    cursor.execute("""
        SELECT id, nome, professor, data, hora, vagas
        FROM aulas
        ORDER BY data, hora
    """)

    aulas = cursor.fetchall()

    print("\n--- AULAS DISPONÍVEIS ---")

    for aula in aulas:
        print(
            "ID:", aula[0],
            "| Aula:", aula[1],
            "| Professor:", aula[2],
            "| Data:", aula[3],
            "| Hora:", aula[4],
            "| Vagas:", aula[5]
        )

def agendar_aula():
    aluno = input("Digite o nome do aluno: ")
    listar_aulas()
    aula_id = int(input("\nDigite o ID da aula que deseja: "))

    cursor.execute(
        "SELECT nome, vagas FROM aulas WHERE id = ?",
        (aula_id,)
    )

    aula = cursor.fetchone()

    if aula is None:
        print("Aula não encontrada.")
        return
    nome_aula = aula[0]
    vagas = aula[1]

    cursor.execute("""
        SELECT id
        FROM agendamentos
        WHERE aula_id = ?
    """, (aula_id,))
    agendamentos = cursor.fetchall()
    quantidade = len(agendamentos)

    if quantidade >= vagas:
        print("Aula lotada!")
        return

    cursor.execute("""
        SELECT id
        FROM agendamentos
        WHERE aula_id = ? AND aluno = ?
    """, (aula_id, aluno))

    if cursor.fetchone():
        print("Você já está agendado nessa aula.")
        return

    cursor.execute("""
        INSERT INTO agendamentos (aula_id, aluno)
        VALUES (?, ?)
    """, (aula_id, aluno))

    conexao.commit()

    print(f"{aluno} agendado com sucesso! Na categoria {nome_aula}")
    


def listar_alunos():

    aula_id = int(input("Digite o ID da aula: "))

    cursor.execute("""
        SELECT aluno
        FROM agendamentos
        WHERE aula_id = ?
    """, (aula_id,))

    alunos = cursor.fetchall()

    print("\n--- ALUNOS AGENDADOS ---")

    if not alunos:
        print("Nenhum aluno agendado.")
        return

    for aluno in alunos:
        print("-", aluno[0])


while True:
    print("\n===== STRONG LIFE =====")
    print("1 - Criar aula")
    print("2 - Ver aulas")
    print("3 - Agendar aula")
    print("4- Ver alunos")
    print("5 - Sair")   

    opcao = input("Digite a opção desejada: ")
    match opcao:

        case "1":
            criar_aula()

        case "2":
            listar_aulas()

        case "3":
            agendar_aula()

        case "4":
            listar_alunos()
            
        case "5":
            print("Saindo do sistema")
            break

        case _:
            print("Opção inválida.")

conexao.commit()
conexao.close()



