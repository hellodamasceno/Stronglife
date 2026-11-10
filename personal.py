import sqlite3


def montar_treino():
    
    try:
        conexao = sqlite3.connect("sistema_academia.db")
        cursor = conexao.cursor()

        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Leg Press 45º')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Extensora')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Flexora Horizontal')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Puxada Alta na Polia')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Remada Baixa na Máquina')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Supino Sentado na Máquina')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Desenvolvimento de Ombros Máquina')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Tríceps Corda Polia')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Rosca Biceps na Polia')")
        cursor.execute("INSERT OR IGNORE INTO exercicios (nome) VALUES ('Cadeira Abdutora/Adutora')")
        conexao.commit()

        print("\n--- CONFIGURAÇÃO DE TREINO (ÁREA DO PERSONAL) ---")

        id_personal = int(input("Digite o ID do Personal: "))

        cursor.execute("SELECT nome FROM personais WHERE id = ?", (id_personal,))
        personal = cursor.fetchone()

        match personal:
            case None:
                print("Acesso Negado: Personal não encontrado.")
                conexao.close()
                return
            case _:
                print(f"Identidade Confirmada: Professor(a) {personal[0]}")

        id_aluno = int(input("Digite o ID do Aluno: "))

        cursor.execute("SELECT nome_aluno, status_acompanhamento FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()

        match aluno:
            case None:
                print("Erro: Aluno não encontrado.")
                conexao.close()
                return
            case _:
                print(f"Montando treino para: {aluno[0]} ({aluno[1]})")
        
        dia = input("Qual o dia da semana deste treino? (ex: Segunda): ")

        cursor.execute("SELECT id, nome FROM exercicios")
        lista_exercicios = cursor.fetchall()
        
        print("\n--- EXERCÍCIOS DISPONÍVEIS ---")
        for ex in lista_exercicios:
            print(f"[{ex[0]}] - {ex[1]}")

        print("\nSelecione até 6 exercícios (ou digite 0 para encerrar):")

        for i in range(1, 7):
            escolha = int(input(f"ID do {i}º exercício: "))

            match escolha:
                case 0:
                    break
                case _:
                    cursor.execute(
                        "INSERT INTO treinos_diarios (id_aluno, dia_semana, id_exercicio) VALUES (?, ?, ?)",
                        (id_aluno, dia, escolha)
                    )
        
        conexao.commit()
        print(f"Treino de {dia} salvo com sucesso!")
        conexao.close()

    except:
        print("Ocorreu um erro no sistema.")


def visualizar_ficha_aluno():
    
    try:
        conexao = sqlite3.connect("sistema_academia.db")
        cursor = conexao.cursor()

        id_aluno = int(input("\nDigite o ID do aluno para ver a ficha: "))

        cursor.execute(
            "SELECT nome_aluno, idade, status_acompanhamento, dia_aula, horario_aula, id_personal FROM alunos WHERE id = ?", 
            (id_aluno,)
        )
        dados = cursor.fetchone()

        match dados:
            case None:
                print("Aluno não encontrado.")
                conexao.close()
                return

        id_do_professor = dados[5]
        nome_professor = "Nenhum Atribuído"

        match id_do_professor:
            case None:
                nome_professor = "Nenhum Atribuído"
            case _:
                cursor.execute("SELECT nome FROM personais WHERE id = ?", (id_do_professor,))
                personal_dados = cursor.fetchone()

                match personal_dados:
                    case None:
                        nome_professor = "Nenhum Atribuído"
                    case _:
                        nome_professor = personal_dados[0]

        print("\n=======================================================")
        print(f"FICHA COMPLETA DO ALUNO(A): {dados[0]}")
        print(f"Idade: {dados[1]} anos | {dados[2]}")
        print(f"Personal Responsável: Prof. {nome_professor}")
        print(f"Agendamento de Aula Fixa: {dados[3]} às {dados[4]}")
        print("=======================================================")

        cursor.execute(
            """
            SELECT td.dia_semana, e.nome 
            FROM treinos_diarios td
            JOIN exercicios e ON td.id_exercicio = e.id
            WHERE td.id_aluno = ?
            ORDER BY td.dia_semana""", (id_aluno,)
        )
        todos_os_treinos = cursor.fetchall()

        match todos_os_treinos:
            case []:
                print("Nenhuma rotina de exercícios montada para este aluno.")
            case _:
                print("\nROTINA DE EXERCÍCIOS:")
                contador = 1
                for treino in todos_os_treinos:
                    print(f"[{treino[0]}] - {contador}º exercício: {treino[1]}")
                    contador = contador + 1
                
        print("=======================================================")
        conexao.close()

    except:
        print("Ocorreu um erro ao buscar os dados.")

montar_treino()
visualizar_ficha_aluno()
