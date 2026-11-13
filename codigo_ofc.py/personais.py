import sqlite3
conexao = sqlite3.connect("sistema_academia.db")
cursor = conexao.cursor()

def montar_treino(id_personal):

    conexao = None

    try:
        conexao = sqlite3.connect("sistema_academia.db")
        cursor = conexao.cursor()

        print("\n >>> MONTAR TREINOS <<<")

        cursor.execute(
            "SELECT nome FROM personais WHERE id = ?",
            (id_personal,)
        )

        personal = cursor.fetchone()

        if personal is None:
            print("Personal não encontrado.")
            return

        print(f"Personal: {personal[0]}")

        cursor.execute(
            '''
            SELECT id, nome_aluno
            FROM alunos
            WHERE id_personal = ?
            ''',
            (id_personal,)
        )

        alunos = cursor.fetchall()

        if len(alunos) == 0:
            print("Nenhum aluno vinculado a você.")
            return

        print("\n--- SEUS ALUNOS ---")

        for aluno in alunos:
            print(f"[{aluno[0]}] - {aluno[1]}")

        id_aluno = int(input("\nDigite o ID do aluno: "))

        cursor.execute(
            '''
            SELECT nome_aluno
            FROM alunos
            WHERE id = ? AND id_personal = ?
            ''',
            (id_aluno, id_personal)
        )

        aluno = cursor.fetchone()

        if aluno is None:
            print("Aluno não encontrado.")
            return

        print(f"\nMontando treino para: {aluno[0]}")

        dia = input("Digite o dia da semana: ").strip().capitalize()

        dias = [
            "Segunda", "Terça", "Quarta",
            "Quinta", "Sexta", "Sábado", "Domingo"
        ]

        if dia not in dias:
            print("Dia da semana inválido.")
            return

        cursor.execute(
            '''
            SELECT id FROM treinos_diarios
            WHERE id_aluno = ? AND dia_semana = ?
            ''',
            (id_aluno, dia)
        )

        if cursor.fetchone() is not None:
            print("Esse aluno já possui um treino nesse dia.")
            return

        cursor.execute("SELECT id, nome FROM exercicios")
        exercicios = cursor.fetchall()

        if len(exercicios) == 0:
            print("Nenhum exercício cadastrado.")
            return

        print("\n--- EXERCÍCIOS DISPONÍVEIS ---")

        for exercicio in exercicios:
            print(f"[{exercicio[0]}] - {exercicio[1]}")

        selecionados = []

        print("\nEscolha até 6 exercícios.")
        print("Digite 0 para finalizar.")

        while len(selecionados) < 6:

            escolha = int(input("Digite o ID do exercício: "))

            if escolha == 0:
                break

            cursor.execute(
                "SELECT id FROM exercicios WHERE id = ?",
                (escolha,)
            )

            exercicio = cursor.fetchone()

            if exercicio is None:
                print("Exercício não encontrado.")

            elif escolha in selecionados:
                print("Esse exercício já foi selecionado.")

            else:
                selecionados.append(escolha)
                print("Exercício selecionado!")

        if len(selecionados) == 0:
            print("Nenhum exercício selecionado.")
            return

        for id_exercicio in selecionados:

            cursor.execute(
                '''
                INSERT INTO treinos_diarios
                (id_aluno, dia_semana, id_exercicio)
                VALUES (?, ?, ?)
                ''',
                (id_aluno, dia, id_exercicio)
            )

        conexao.commit()

        print("\nTreino montado com sucesso!")
        print(f"Aluno: {aluno[0]}")
        print(f"Dia: {dia}")
        print(f"Quantidade de exercícios: {len(selecionados)}")

    except ValueError:
        print("Erro: digite um número válido.")

    except sqlite3.Error as e:
        if conexao:
            conexao.rollback()

        print(f"Erro no banco de dados: {e}")

    finally:
        if conexao:
            conexao.close()
            
montar_treino(id_personal)
