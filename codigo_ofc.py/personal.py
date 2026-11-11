import sqlite3

def montar_treino(id_personal):

    conexao = None

    try:
        conexao = sqlite3.connect("sistema_academia.db")
        cursor = conexao.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        print("\n--- CONFIGURAÇÃO DE TREINO (ÁREA DO PERSONAL) ---")

        cursor.execute(
            "SELECT nome FROM personais WHERE id = ?",
            (id_personal,)
        )

        personal = cursor.fetchone()

        match personal:
            case None:
                print("Acesso negado: Personal não encontrado.")
                return

            case _:
                print(f"Professor(a): {personal[0]}")

        lista_exercicios = [
            "Leg Press 45º",
            "Extensora",
            "Flexora Horizontal",
            "Puxada Alta na Polia",
            "Remada Baixa na Máquina",
            "Supino Sentado na Máquina",
            "Desenvolvimento de Ombros Máquina",
            "Tríceps Corda Polia",
            "Rosca Biceps na Polia",
            "Cadeira Abdutora/Adutora"
        ]

        for exercicio in lista_exercicios:
            cursor.execute(
                "INSERT OR IGNORE INTO exercicios (nome) VALUES (?)",
                (exercicio,)
            )

        conexao.commit()

        # Escolha do aluno
        print("\n--- ALUNOS VINCULADOS AO PERSONAL ---")

        cursor.execute(
            """
            SELECT id, nome_aluno
            FROM alunos
            WHERE id_personal = ?
            """,
            (id_personal,)
        )

        alunos = cursor.fetchall()

        match alunos:
            case []:
                print("Nenhum aluno vinculado a este personal.")
                return

            case _:
                for aluno in alunos:
                    print(f"[{aluno[0]}] - {aluno[1]}")

        id_aluno = int(input("\nDigite o ID do aluno: "))

        cursor.execute(
            """
            SELECT nome_aluno
            FROM alunos
            WHERE id = ? AND id_personal = ?
            """,
            (id_aluno, id_personal)
        )

        aluno = cursor.fetchone()

        match aluno:
            case None:
                print("Aluno não encontrado ou não vinculado a você.")
                return

            case _:
                print(f"\nMontando treino para: {aluno[0]}")

        dia = input(
            "\nQual o dia da semana deste treino? "
        ).strip().capitalize()

        dias_validos = [
            "Segunda", "Terça", "Quarta",
            "Quinta", "Sexta", "Sábado", "Domingo"
        ]

        match dia:
            case "Segunda" | "Terça" | "Quarta" | "Quinta" | "Sexta" | "Sábado" | "Domingo":
                pass

            case _:
                print("Dia da semana inválido.")
                return

        cursor.execute("SELECT id, nome FROM exercicios")
        lista = cursor.fetchall()

        print("\n--- EXERCÍCIOS DISPONÍVEIS ---")

        for ex in lista:
            print(f"[{ex[0]}] - {ex[1]}")

        print("\nSelecione até 6 exercícios.")
        print("Digite 0 para encerrar.")

        selecionados = []

        for i in range(1, 7):

            escolha = int(input(f"ID do {i}º exercício: "))

            match escolha:
                case 0:
                    break

                case _:
                    cursor.execute(
                        "SELECT id FROM exercicios WHERE id = ?",
                        (escolha,)
                    )

                    exercicio = cursor.fetchone()

                    match exercicio:
                        case None:
                            print("Exercício não encontrado.")

                        case _:
                            match escolha in selecionados:
                                case True:
                                    print("Esse exercício já foi selecionado.")

                                case False:
                                    selecionados.append(escolha)

        match selecionados:
            case []:
                print("Nenhum exercício foi selecionado.")
                return

            case _:
                for exercicio in selecionados:
                    cursor.execute(
                        """
                        INSERT INTO treinos_diarios
                        (id_aluno, dia_semana, id_exercicio)
                        VALUES (?, ?, ?)
                        """,
                        (id_aluno, dia, exercicio)
                    )

                conexao.commit()

                print(f"\nTreino de {dia} salvo com sucesso!")
                print(f"Aluno: {aluno[0]}")
                print(f"Quantidade de exercícios: {len(selecionados)}")

    except ValueError:
        print("Erro: Digite um número válido.")

    except sqlite3.Error as e:
        if conexao:
            conexao.rollback()

        print(f"Erro no banco de dados: {e}")

    finally:
        if conexao:
            conexao.close()


def visualizar_ficha_aluno(id_personal):

    conexao = None

    try:
        conexao = sqlite3.connect("sistema_academia.db")
        cursor = conexao.cursor()

        print("\n--- VISUALIZAR FICHA DO ALUNO ---")

        cursor.execute(
            """
            SELECT id, nome_aluno
            FROM alunos
            WHERE id_personal = ?
            """,
            (id_personal,)
        )

        alunos = cursor.fetchall()

        match alunos:
            case []:
                print("Você não possui alunos vinculados.")
                return

            case _:
                print("\n--- SEUS ALUNOS ---")

                for aluno in alunos:
                    print(f"[{aluno[0]}] - {aluno[1]}")

        id_aluno = int(input("\nDigite o ID do aluno: "))

        cursor.execute(
            """
            SELECT
                a.nome_aluno,
                a.idade,
                a.status_acompanhamento,
                a.dia_aula,
                a.horario_aula,
                p.nome,
                a.plano
            FROM alunos a
            LEFT JOIN personais p ON a.id_personal = p.id
            WHERE a.id = ? AND a.id_personal = ?
            """,
            (id_aluno, id_personal)
        )

        dados = cursor.fetchone()

        match dados:
            case None:
                print("Aluno não encontrado ou não vinculado a você.")
                return

            case _:
                print("\n" + "=" * 50)
                print(f"FICHA DO ALUNO: {dados[0]}")
                print(f"Idade: {dados[1]} anos")
                print(f"Status: {dados[2]}")
                print(f"Personal responsável: {dados[5]}")
                print(f"Plano: {dados[6]}")
                print(f"Dia da aula: {dados[3]}")
                print(f"Horário: {dados[4]}")
                print("=" * 50)

        cursor.execute(
            """
            SELECT td.dia_semana, e.nome
            FROM treinos_diarios td
            JOIN exercicios e ON td.id_exercicio = e.id
            WHERE td.id_aluno = ?
            ORDER BY td.dia_semana
            """,
            (id_aluno,)
        )

        todos_os_treinos = cursor.fetchall()

        match todos_os_treinos:
            case []:
                print("\nNenhuma rotina de exercícios cadastrada.")

            case _:
                print("\n--- ROTINA DE EXERCÍCIOS ---")

                for treino in todos_os_treinos:
                    print(f"[{treino[0]}] - {treino[1]}")

        print("=" * 50)

    except ValueError:
        print("Erro: Digite um ID válido.")

    except sqlite3.Error as e:
        print(f"Erro ao buscar os dados: {e}")

    finally:
        if conexao:
            conexao.close()