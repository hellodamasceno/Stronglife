import sqlite3
from mensalidades import menu_planos, listar_planos


def cadastrar_alunos():

    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
            
        print("\n----CADASTRO DE ALUNO----")

        nome_aluno = input("Informe o nome do aluno para o cadastro: ")
        idade_aluno = int(input("Informe a idade do aluno: "))
        cpf_aluno = input("Informe o cpf do aluno para o cadastro: ")

        listar_planos()
        id_personal_aluno = input("Informe o id do plano que o aluno será vinculado: ")
       
        comando_inserir = ('''
        INSERT INTO alunos
        (nome_aluno, idade, cpf, mensalidade, id_plano)
        VALUES (?, ?, ?, ?, ?)
        ''')

        cursor.execute(comando_inserir, (nome_aluno, idade_aluno, cpf_aluno, id_personal_aluno))

        conexao.commit()
        print(f"Aluno '{nome_aluno}' cadastrado com sucesso!")
    except ValueError:
        print("Erro: Idade e mensalidade devem ser apenas números!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar aluno: {e}")
    finally:
        conexao.close()

def listar_aluno():
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        print("\n----LISTA DE ALUNOS----")
        cursor.execute("SELECT * FROM alunos;")
        alunos = cursor.fetchall() 

        if not alunos:
            print("Nenhum aluno cadastrado no momento.")
            return
            
        for a in alunos:
            print(f"ID: {a[0]} | NOME: {a[1]} | Idade: {a[2]} | CPF: {a[3]} | Mensalidade: R${a[4]:.2f}")
    except sqlite3.Error as e:
        print(f"Erro ao listar alunos: {e}")
    finally:
        conexao.close()



def atualizar_cadastro():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        listar_aluno()

        id_aluno = int(input("Digite o ID do aluno que deseja atualizar: "))

        cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        while True:
            print("\n>>> ATUALIZAR CADASTRO <<<")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Telefone")
            print("4 - Idade")
            print("5 - Plano")
            print("6 - Voltar")

            opcao = input("Escolha o que deseja atualizar: ")

            match opcao:
                case "1":
                    novo_valor = input("Digite o novo nome: ")
                    cursor.execute(
                        "UPDATE alunos SET nome = ? WHERE id = ?",
                        (novo_valor, id_aluno)
                    )

                case "2":
                    novo_valor = input("Digite o novo CPF: ")
                    cursor.execute(
                        "UPDATE alunos SET cpf = ? WHERE id = ?",
                        (novo_valor, id_aluno)
                    )

                case "3":
                    novo_valor = input("Digite o novo telefone: ")
                    cursor.execute(
                        "UPDATE alunos SET telefone = ? WHERE id = ?",
                        (novo_valor, id_aluno)
                    )

                case "4":
                    novo_valor = input("Digite a nova idade: ")
                    cursor.execute(
                        "UPDATE alunos SET idade = ? WHERE id = ?",
                        (novo_valor, id_aluno)
                    )

                case "5":
                    novo_valor = input("Digite o novo plano: ")
                    cursor.execute(
                        "UPDATE alunos SET plano = ? WHERE id = ?",
                        (novo_valor, id_aluno)
                    )

                case "6":
                    print("Voltando ao menu...")
                    break

                case _:
                    print("Opção inválida!")
                    continue

            if opcao in ["1", "2", "3", "4", "5"]:
                conexao.commit()
                print("Cadastro atualizado com sucesso!")
    except sqlite3.Error as e:
        print("Error: no banco ao atualizar aluno!")
    except ValueError:
        print("Error: id deve ser um numro inteiro!")

def deletar_aluno():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR ALUNO ----")
        listar_aluno()
        id_aluno = int(input("Digite o ID do aluno que deseja deletar: "))

        cursor.execute("SELECT nome_aluno FROM alunos WHERE id = ?", (id_aluno,))
        aluno = cursor.fetchone()
        
        if aluno:
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
            conexao.commit()
            print(f"Aluno '{aluno[0]}' removido com sucesso!")
        else:
            print("Erro: Aluno não encontrado com o ID informado.")
            
    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar aluno: {e}")
    finally:
        conexao.close()


def cadastrar_personal():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n----CADASTRO DE PERSONAL----")
        nome = input("Nome do personal: ")
        cpf = input("CPF personal: ")
        telefone = input("Telefone do personal: ") 

        cursor.execute("INSERT INTO personais (nome, cpf, telefone) VALUES (?, ?, ?)", (nome, cpf, telefone))
        
        conexao.commit()
        print(f"Personal '{nome}' cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar personal: {e}")
    finally:
        conexao.close()



def listar_personal():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        print("\n---- LISTA DE PERSONAIS ----")
        cursor.execute("SELECT id, nome, cpf, telefone FROM personais;")
        personais = cursor.fetchall()
        
        if not personais:
            print("Nenhum personal cadastrado no momento.")
            return
            
        for p in personais:
            print(f"ID: {p[0]} | NOME: {p[1]} | CPF: {p[2]} | TELEFONE: {p[3]}")
    except sqlite3.Error as e:
        print(f"Erro ao listar personais: {e}")
    finally:
        conexao.close()


def atualizar_cadastrop():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        listar_personal()

        id_personal = input("Digite o ID do personal que deseja atualizar: ")

        cursor.execute("SELECT * FROM personais WHERE id = ?", (id_personal,))
        personal = cursor.fetchone()

        if not personal:
            print("Personal não encontrado!")
            return

        while True:
            print("\n>>> ATUALIZAR CADASTRO <<<")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Telefone")

            opcao = input("Escolha o que deseja atualizar: ")

            match opcao:
                case "1":
                    novo_valor = input("Digite o novo nome: ")
                    cursor.execute(
                        "UPDATE personais SET nome = ? WHERE id = ?",
                        (novo_valor, id_personal)
                    )

                case "2":
                    novo_valor = input("Digite o novo CPF: ")
                    cursor.execute(
                        "UPDATE personais SET cpf = ? WHERE id = ?",
                        (novo_valor, id_personal)
                    )

                case "3":
                    novo_valor = input("Digite o novo telefone: ")
                    cursor.execute(
                        "UPDATE personais SET telefone = ? WHERE id = ?",
                        (novo_valor, id_personal)
                    )

                case "4":
                    print("Voltando ao menu...")
                    break

                case _:
                    print("Opção inválida!")
                    continue

            if opcao in ["1", "2", "3", "4"]:
                conexao.commit()
                print("Cadastro atualizado com sucesso!")
    
    except sqlite3.Error as e:
        print("Error: no banco ao atualizar aluno!")
    except ValueError:
        print("Error: id deve ser um numro inteiro!")


def deletar_personal():
    
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR PERSONAL ----")
        listar_personal()
        id_personal = int(input("Digite o ID do personal que deseja deletar: "))

        cursor.execute("SELECT nome FROM personais WHERE id = ?", (id_personal,))
        personal = cursor.fetchone()
        
        if personal:
            cursor.execute("DELETE FROM personais WHERE id = ?", (id_personal,))
            conexao.commit()
            print(f"Personal '{personal[0]}' removido com sucesso!")
        else:
            print("Erro: Personal não encontrado com o ID informado.")
            
    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")
    except sqlite3.IntegrityError:
        print("Erro: Não é possível deletar este personal pois ele está vinculado a um ou mais alunos!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar personal: {e}")
    finally:
        conexao.close()

