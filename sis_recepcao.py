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



    



  