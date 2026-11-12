import sqlite3

def conectar():
    conexao = sqlite3.connect("sistema_academia.db")
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def cadastrar_aluno():
    print("\n--- CADASTRAR NOVO ALUNO ---")
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        nome = input("Nome do aluno: ")
        idade = int(input("Idade: "))
        cpf = input("CPF (apenas números): ")
        id_personal = int(input("ID do Personal responsável: "))
        id_plano = int(input("ID do Plano: "))
        dia_aula = input("Dia da aula (ex: Segunda e Quarta): ")
        horario_aula = input("Horário da aula (ex: 08:00): ")
        status = "Ativo"

        cursor.execute('''
            INSERT INTO alunos (nome_aluno, idade, cpf, id_personal, id_plano, dia_aula, horario_aula, status_acompanhamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, idade, cpf, id_personal, id_plano, dia_aula, horario_aula, status))

        conexao.commit()
        print("\nAluno cadastrado com sucesso!")

    except ValueError:
        print("\nErro: Idade, ID do Personal e ID do Plano devem ser números.")
    except sqlite3.IntegrityError:
        print("\nErro: CPF já cadastrado ou ID de Personal/Plano não existe.")
    except sqlite3.Error as e:
        print(f"\nErro no banco de dados: {e}")
    finally:
        conexao.close()

def listar_alunos():
    print("\n--- LISTA DE ALUNOS ---")
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute('''
            SELECT id, nome_aluno, idade, cpf, id_personal, status_acompanhamento
            FROM alunos
        ''')
        alunos = cursor.fetchall()

        match alunos:
            case []:
                print("Nenhum aluno cadastrado no sistema.")
            case _:
                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | CPF: {aluno[3]} | Personal ID: {aluno[4]} | Status: {aluno[5]}")

    except sqlite3.Error as e:
        print(f"\nErro ao buscar alunos: {e}")
    finally:
        conexao.close()

def atualizar_aluno():
    print("\n--- ATUALIZAR DADOS DO ALUNO ---")
    listar_alunos()
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        id_aluno = int(input("\nDigite o ID do aluno que deseja atualizar: "))

        cursor.execute("SELECT nome_aluno FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()

        match aluno:
            case None:
                print("Aluno não encontrado.")
                return
            case _:
                print(f"\nEditando aluno: {aluno[0]}")
                print("1 - Mudar horário e dia da aula")
                print("2 - Mudar personal responsável")
                print("3 - Mudar status (Ativo / Inativo)")
                
                opcao = input("Escolha o que deseja alterar: ")

                match opcao:
                    case "1":
                        novo_dia = input("Novo dia da aula: ")
                        novo_horario = input("Novo horário: ")
                        cursor.execute("UPDATE alunos SET dia_aula = ?, horario_aula = ? WHERE id = ?", (novo_dia, novo_horario, id_aluno))
                    case "2":
                        novo_personal = int(input("ID do novo personal: "))
                        cursor.execute("UPDATE alunos SET id_personal = ? WHERE id = ?", (novo_personal, id_aluno))
                    case "3":
                        novo_status = input("Novo status (Ativo/Inativo): ")
                        cursor.execute("UPDATE alunos SET status_acompanhamento = ? WHERE id = ?", (novo_status, id_aluno))
                    case _:
                        print("Opção inválida.")
                        return

                conexao.commit()
                print("\nDados atualizados com sucesso!")

    except ValueError:
        print("\nErro: Digite um número válido.")
    except sqlite3.IntegrityError:
        print("\nErro: O ID do novo personal não existe.")
    except sqlite3.Error as e:
        print(f"\nErro ao atualizar: {e}")
    finally:
        conexao.close()

def deletar_aluno():
    print("\n--- EXCLUIR ALUNO ---")
    listar_alunos()
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        id_aluno = int(input("\nDigite o ID do aluno que deseja excluir: "))

        cursor.execute("SELECT nome_aluno FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()

        match aluno:
            case None:
                print("Aluno não encontrado.")
            case _:
                confirmacao = input(f"Tem certeza que deseja excluir {aluno[0]}? (S/N): ").strip().upper()
                
                match confirmacao:
                    case "S":
                        cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
                        conexao.commit()
                        print("\nAluno excluído com sucesso!")
                    case "N":
                        print("\nOperação cancelada.")
                    case _:
                        print("\nOpção inválida. Operação cancelada.")

    except ValueError:
        print("\nErro: Digite um ID numérico válido.")
    except sqlite3.IntegrityError:
        print("\nErro: Não é possível excluir este aluno pois ele possui treinos ou presenças vinculadas.")
    except sqlite3.Error as e:
        print(f"\nErro ao excluir: {e}")
    finally:
        conexao.close()