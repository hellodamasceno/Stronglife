import sqlite3


def cadastrar_alunos():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        print("\n---- CADASTRO DE ALUNO ----")

        nome_aluno = input("Nome do aluno: ")
        idade_aluno = int(input("Idade do aluno: "))

        if idade_aluno < 12:
            print("\nAVISO: Alunos menores de 12 anos só podem treinar acompanhados de um personal ou dos pais!")

        if idade_aluno < 18:
            print("\nATENÇÃO: Aluno menor de 18 anos precisa de autorização dos pais ou responsáveis.")
            autorizacao = input("Possui autorização assinada pelos pais? (S/N): ").strip().upper()
            if autorizacao != "S":
                print("Cadastro cancelado! Não é possível cadastrar menores sem autorização.")
                return

        cpf_aluno = input("CPF do aluno: ")

        cursor.execute('SELECT id, nome, valor FROM planos')
        planos = cursor.fetchall()

        if not planos:
            print("Nenhum plano cadastrado! Cadastre um plano primeiro.")
            return

        print("\n---- PLANOS DISPONÍVEIS ----")
        for p in planos:
            print(f"ID: {p[0]} | Plano: {p[1]} | Valor: R$ {p[2]:.2f}")

        id_plano = int(input("Escolha o ID do plano: "))

        cursor.execute('SELECT valor FROM planos WHERE id = ?', (id_plano,))
        plano = cursor.fetchone()

        if plano is None:
            print("Plano não encontrado!")
            return

        mensalidade = plano[0]

        cursor.execute('SELECT id, nome FROM personais')
        personais = cursor.fetchall()

        if not personais:
            print("Nenhum personal cadastrado!")
            return

        print("\n---- PERSONAIS DISPONÍVEIS ----")
        for p in personais:
            print(f"ID: {p[0]} | Nome: {p[1]}")

        id_personal = int(input("Escolha o ID do personal: "))

        cursor.execute('SELECT id FROM personais WHERE id = ?', (id_personal,))
        if cursor.fetchone() is None:
            print("Personal não encontrado!")
            return

        cursor.execute('''
            INSERT INTO alunos
            (nome_aluno, idade, cpf, mensalidade, id_personal, id_plano)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            nome_aluno,
            idade_aluno,
            cpf_aluno,
            mensalidade,
            id_personal,
            id_plano
        ))

        conexao.commit()
        print(f"Aluno '{nome_aluno}' cadastrado com sucesso!")

    except ValueError:
        print("Erro: informe números válidos para idade e IDs!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar aluno: {e}")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    finally:
        if conexao:
            conexao.close()


def listar_aluno():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()

        print("\n---- LISTA DE ALUNOS ----")

        cursor.execute('''
            SELECT id, nome_aluno, idade, cpf, mensalidade,
                   id_personal, id_plano
            FROM alunos
        ''')

        alunos = cursor.fetchall()

        if not alunos:
            print("Nenhum aluno cadastrado no momento.")
            return

        for a in alunos:
            print(
                f"ID: {a[0]} | "
                f"NOME: {a[1]} | "
                f"IDADE: {a[2]} | "
                f"CPF: {a[3]} | "
                f"MENSALIDADE: R$ {a[4]:.2f} | "
                f"PERSONAL: {a[5]} | "
                f"PLANO: {a[6]}"
            )

    except sqlite3.Error as e:
        print(f"Erro ao listar alunos: {e}")
    finally:
        if conexao:
            conexao.close()


def atualizar_cadastro():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        listar_aluno()

        id_aluno = int(input("\nDigite o ID do aluno que deseja atualizar: "))

        cursor.execute('SELECT * FROM alunos WHERE id = ?', (id_aluno,))
        aluno = cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        while True:
            print("\n>>> ATUALIZAR CADASTRO <<<")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Idade")
            print("4 - Plano")
            print("5 - Voltar")

            opcao = int(input("Escolha o que deseja atualizar: "))

            match opcao:
                case 1:
                    novo_valor = input("Digite o novo nome: ")
                    cursor.execute(
                        'UPDATE alunos SET nome_aluno = ? WHERE id = ?',
                        (novo_valor, id_aluno)
                    )
                    conexao.commit()
                    print("Nome atualizado com sucesso!")

                case 2:
                    novo_valor = input("Digite o novo CPF: ")
                    cursor.execute(
                        'UPDATE alunos SET cpf = ? WHERE id = ?',
                        (novo_valor, id_aluno)
                    )
                    conexao.commit()
                    print("CPF atualizado com sucesso!")

                case 3:
                    nova_idade = int(input("Digite a nova idade: "))
                    if nova_idade < 12:
                        print("AVISO: Alunos menores de 12 anos só podem treinar acompanhados!")
                    if nova_idade < 18:
                        aut = input("Possui autorização dos pais? (S/N): ").strip().upper()
                        if aut == "S":
                            cursor.execute(
                                'UPDATE alunos SET idade = ? WHERE id = ?',
                                (nova_idade, id_aluno)
                            )
                            conexao.commit()
                            print("Idade atualizada com sucesso!")
                        else:
                            print("Atualização de idade cancelada por falta de autorização.")
                case 4:
                    cursor.execute('SELECT id, nome, valor FROM planos')
                    planos = cursor.fetchall()
                    for p in planos:
                        print(f"ID: {p[0]} | Plano: {p[1]} | Valor: R$ {p[2]:.2f}")
                    
                    novo_plano = int(input("Digite o ID do novo plano: "))
                    cursor.execute('SELECT valor FROM planos WHERE id = ?', (novo_plano,))
                    plano_encontrado = cursor.fetchone()
                    
                    if plano_encontrado:
                        cursor.execute(
                            'UPDATE alunos SET id_plano = ?, mensalidade = ? WHERE id = ?',
                            (novo_plano, plano_encontrado[0], id_aluno)
                        )
                        conexao.commit()
                        print("Plano e mensalidade atualizados com sucesso!")
                    else:
                        print("Plano não encontrado!")

                case 5:
                    print("Voltando ao menu...")
                    break

                case _:
                    print("Opção inválida!")

    except sqlite3.Error as e:
        print(f"Erro no banco ao atualizar aluno: {e}")
    except ValueError:
        print("Erro: digite um número válido!")
    finally:
        if conexao:
            conexao.close()


def deletar_aluno():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR ALUNO ----")
        listar_aluno()
        id_aluno = int(input("\nDigite o ID do aluno que deseja deletar: "))

        cursor.execute('SELECT nome_aluno FROM alunos WHERE id = ?', (id_aluno,))
        aluno = cursor.fetchone()
        
        if aluno:
            cursor.execute('DELETE FROM alunos WHERE id = ?', (id_aluno,))
            conexao.commit()
            print(f"Aluno '{aluno[0]}' removido com sucesso!")
        else:
            print("Erro: Aluno não encontrado com o ID informado.")
            
    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")
    except sqlite3.IntegrityError:
        print("Erro: Não é possível deletar este aluno pois ele possui treinos ou registros vinculados!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar aluno: {e}")
    finally:
        if conexao:
            conexao.close()


def cadastrar_personal():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- CADASTRO DE PERSONAL ----")
        nome = input("Nome do personal: ")
        cpf = input("CPF do personal: ")
        telefone = input("Telefone do personal: ") 

        cursor.execute('INSERT INTO personais (nome, cpf, telefone) VALUES (?, ?, ?)', (nome, cpf, telefone))
        
        conexao.commit()
        print(f"Personal '{nome}' cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar personal: {e}")
    finally:
        if conexao:
            conexao.close()


def listar_personal():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        print("\n---- LISTA DE PERSONAIS ----")
        cursor.execute('SELECT id, nome, cpf, telefone FROM personais')
        personais = cursor.fetchall()
        
        if not personais:
            print("Nenhum personal cadastrado no momento.")
            return
            
        for p in personais:
            print(f"ID: {p[0]} | NOME: {p[1]} | CPF: {p[2]} | TELEFONE: {p[3]}")
    except sqlite3.Error as e:
        print(f"Erro ao listar personais: {e}")
    finally:
        if conexao:
            conexao.close()


def atualizar_cadastrop():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        listar_personal()

        id_personal = int(input("\nDigite o ID do personal que deseja atualizar: "))

        cursor.execute('SELECT * FROM personais WHERE id = ?', (id_personal,))
        personal = cursor.fetchone()

        if not personal:
            print("Personal não encontrado!")
            return

        while True:
            print("\n>>> ATUALIZAR CADASTRO DE PERSONAL <<<")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Telefone")
            print("4 - Voltar")

            opcao = input("Escolha o que deseja atualizar: ")

            match opcao:
                case "1":
                    novo_valor = input("Digite o novo nome: ")
                    cursor.execute(
                        'UPDATE personais SET nome = ? WHERE id = ?',
                        (novo_valor, id_personal)
                    )
                    conexao.commit()
                    print("Nome atualizado com sucesso!")

                case "2":
                    novo_valor = input("Digite o novo CPF: ")
                    cursor.execute(
                        'UPDATE personais SET cpf = ? WHERE id = ?',
                        (novo_valor, id_personal)
                    )
                    conexao.commit()
                    print("CPF atualizado com sucesso!")

                case "3":
                    novo_valor = input("Digite o novo telefone: ")
                    cursor.execute(
                        'UPDATE personais SET telefone = ? WHERE id = ?',
                        (novo_valor, id_personal)
                    )
                    conexao.commit()
                    print("Telefone atualizado com sucesso!")

                case "4":
                    print("Voltando ao menu...")
                    break

                case _:
                    print("Opção inválida!")

    except sqlite3.Error as e:
        print(f"Erro no banco ao atualizar personal: {e}")
    except ValueError:
        print("Erro: ID deve ser um número inteiro!")
    finally:
        if conexao:
            conexao.close()


def deletar_personal():
    conexao = None
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n---- DELETAR PERSONAL ----")
        listar_personal()
        id_personal = int(input("\nDigite o ID do personal que deseja deletar: "))

        cursor.execute('SELECT nome FROM personais WHERE id = ?', (id_personal,))
        personal = cursor.fetchone()
        
        if personal:
            cursor.execute('DELETE FROM personais WHERE id = ?', (id_personal,))
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
        if conexao:
            conexao.close()
