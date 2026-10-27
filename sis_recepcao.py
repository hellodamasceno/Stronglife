print("---LOGIN RECEPCIONISTA---")

def login_rec():
    nome_rece = input("Nome: ")
    senha_rece = input("Insira a senha: ")


def cadastrar_alunos():
    nome_aluno = input("Informe o nome do aluno para o cadastro: ")
    cpf_aluno = input("Informe o cpf do aluno para o cadastro: ")
    tel_aluno = input("Informe o telefone do aluno: ")
    idade_aluno = int(input("Informe a idade do aluno: "))
    plano_aluno = input("Informe o plano que o aluno será vinculado: ")

    comando_inserir = "INSERT INTO alunos (nome, cpf, telefone, idade, plano) VALUES (?, ?, ?, ?, ?)"

        cursor.execute(comando_inserir, (nome_aluno, cpf_aluno, tel_aluno, idade_aluno, plano_aluno))
        conexao.commit()
        print("ALUNO CADASTRADO COM SUCESSO!")

    except sqlite3.IntegrityError as e:
        print("Erro! Informações já cadastradas! ", e)


def listar_alunos():

    print(">>> ALUNOS CADASTRADOS <<<")
    print("1 - Listar todos os alunos")
    print("2 - Buscar aluno pelo id")

    opcao = int(input("Informe a opção desejada: "))

    mach opcao:
        case 1:
            cursor.execute("SELECT * FROM alunos")
            inf_alunos = cursor.fetchall()

            if inf_alunos:
                for aluno in inf_alunos:
                    print(aluno)
            else:
                print("Nenhum aluno encontrado!")

        case 2: 
            cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
            info_alunos = cursor.fetchone()

            if info_alunos:
                print(">>> ALUNO ENCONTRADO <<<")
                print(info_alunos)
            else:
                print("Nenhum aluno encontrado com esse id!")
        case _:
            print("Opção inválida!")


def atualizar_cadastro():
    listar_alunos()

    try:
        def atualizar_cadastro():
    listar_alunos()

    id_aluno = input("Digite o ID do aluno que deseja atualizar: ")

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


def excluir_cadastro():
    listar_alunos()


    try:
        id_rede = int(input("Informe o id do cadastro que deseja excluir: "))
        cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))


        conexao.commit()
        print("Cadastro deletado com sucesso!")

    except sqlite3.Error as e:
            print("Erro: Cadastro não deletado.", e)


def cadastrar_personais():
    nome_personal = input("Informe o nome do porfessor para o cadastro: ")
    cpf_personal = input("Informe o cpf do professor para o cadastro: ")
    tel_personal = input("Informe o telefone do professor: ")

    comando_inserir = "INSERT INTO personais (nome, cpf, telefone) VALUES (?, ?, ?)"

        cursor.execute(comando_inserir, (nome_personal, cpf_personal, tel_personal))
        conexao.commit()
        print("PERSONAL CADASTRADO COM SUCESSO!")

    except sqlite3.IntegrityError as e:
        print("Erro! Informações já cadastradas! ", e)


def atualizar_




    



    



  