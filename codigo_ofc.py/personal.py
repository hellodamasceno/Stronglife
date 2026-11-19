import sqlite3


def conectar():
    conexao = sqlite3.connect("sistema_academia.db")
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def montar_treino():
    try:
        print("\n---- CONFIGURAÇÃO DE TREINO (ÁREA DO PERSONAL) ----")
        id_personal = int(input("Informe o seu ID de Personal: "))

        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM personais WHERE id = ?", (id_personal,))
            personal = cursor.fetchone()

            if not personal:
                print("Acesso negado: Personal não encontrado.")
                return

            print(f"Professor(a): {personal}")

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
                "Cadeira Abdutora/Adutora",
            ]

            for exercicio in lista_exercicios:
                cursor.execute(
                    "INSERT OR IGNORE INTO exercicios (nome) VALUES (?)",
                    (exercicio,),
                )
            conexao.commit()

            print("\n---- ALUNOS VINCULADOS AO PERSONAL ----")
            cursor.execute(
                "SELECT id, nome_aluno FROM alunos WHERE id_personal = ?",
                (id_personal,),
            )
            alunos = cursor.fetchall()

            if not alunos:
                print("Nenhum aluno vinculado a este personal.")
                return

            for aluno in alunos:
                print(f"ID: {aluno} | NOME: {aluno}")

            id_aluno = int(input("\nDigite o ID do aluno: "))

            cursor.execute(
                "SELECT nome_aluno FROM alunos WHERE id = ? AND id_personal = ?",
                (id_aluno, id_personal),
            )
            aluno = cursor.fetchone()

            if not aluno:
                print("Aluno não encontrado ou não vinculado a você.")
                return

            print(f"\nMontando treino para: {aluno}")

            dia = input("\nQual o dia da semana deste treino? ").strip().capitalize()
            dias_validos = [
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
                "Domingo",
            ]

            if dia not in dias_validos:
                print("Dia da semana inválido.")
                return

            cursor.execute("SELECT id, nome FROM exercicios")
            lista = cursor.fetchall()

            print("\n---- EXERCÍCIOS DISPONÍVEIS ----")
            for ex in lista:
                print(f"ID: {ex} | EXERCÍCIO: {ex}")

            print("\nSelecione até 6 exercícios (Digite 0 para encerrar).")
            selecionados = []

            for i in range(1, 7):
                escolha = int(input(f"ID do {i}º exercício: "))

                if escolha == 0:
                    break

                cursor.execute("SELECT id FROM exercicios WHERE id = ?", (escolha,))
                if not cursor.fetchone():
                    print("Exercício não encontrado.")
                elif escolha in selecionados:
                    print("Esse exercício já foi selecionado.")
                else:
                    selecionados.append(escolha)

            if not selecionados:
                print("Nenhum exercício foi selecionado.")
                return

            for exercicio in selecionados:
                cursor.execute(
                    """
                    INSERT INTO treinos_diarios (id_aluno, dia_semana, id_exercicio)
                    VALUES (?, ?, ?)
                    """,
                    (id_aluno, dia, exercicio),
                )

            conexao.commit()
            print(
                f"\nTreino de {dia} salvo com sucesso! | ALUNO: {aluno} | EXERCÍCIOS: {len(selecionados)}"
            )

    except ValueError:
        print("Erro: Digite um número válido.")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")


def visualizar_ficha_aluno():
    try:
        print("\n---- VISUALIZAR FICHA DO ALUNO ----")
        id_personal = int(input("Informe o seu ID de Personal: "))

        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id, nome_aluno FROM alunos WHERE id_personal = ?",
                (id_personal,),
            )
            alunos = cursor.fetchall()

            if not alunos:
                print("Você não possui alunos vinculados.")
                return

            print("\n---- SEUS ALUNOS ----")
            for aluno in alunos:
                print(f"ID: {aluno} | NOME: {aluno}")

            id_aluno = int(input("\nDigite o ID do aluno: "))

            cursor.execute(
                """
                SELECT
                    a.id,
                    a.nome_aluno,
                    a.idade,
                    a.status_acompanhamento,
                    a.dia_aula,
                    a.horario_aula,
                    p.nome,
                    pl.nome
                FROM alunos a
                LEFT JOIN personais p ON a.id_personal = p.id
                LEFT JOIN planos pl ON a.id_plano = pl.id
                WHERE a.id = ? AND a.id_personal = ?
                """,
                (id_aluno, id_personal),
            )
            dados = cursor.fetchone()

            if not dados:
                print("Aluno não encontrado ou não vinculado a você.")
                return

            personal = dados if dados else "Não atribuído"
            plano = dados if dados else "Sem plano"
            status = dados if dados else "Sem status"
            dia = dados if dados else "Não definido"
            horario = dados if dados else "Não definido"

            print("\n---- FICHA DO ALUNO ----")
            print(
                f"ID: {dados} | NOME: {dados} | IDADE: {dados} | "
                f"STATUS: {status} | PERSONAL: {personal} | PLANO: {plano} | "
                f"AULA: {dia} às {horario}"
            )

            cursor.execute(
                """
                SELECT td.dia_semana, e.nome
                FROM treinos_diarios td
                JOIN exercicios e ON td.id_exercicio = e.id
                WHERE td.id_aluno = ?
                ORDER BY td.dia_semana
                """,
                (id_aluno,),
            )
            todos_os_treinos = cursor.fetchall()

            print("\n---- ROTINA DE EXERCÍCIOS ----")
            if not todos_os_treinos:
                print("Nenhuma rotina de exercícios cadastrada.")
            else:
                for treino in todos_os_treinos:
                    print(f"DIA: {treino} | EXERCÍCIO: {treino}")

    except ValueError:
        print("Erro: Digite um ID válido.")
    except sqlite3.Error as e:
        print(f"Erro ao buscar os dados: {e}")
