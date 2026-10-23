print("---CADASTRO PARA SISTEMA RECEPÇÃO---")

def cadastro_rec():
    nome_rec = input("Nome: ")
    cpf_rec = input("CPF: ")
    senha_rec = int(input("Insira a senha: "))
    comando_inserir = "INSERT INTO recepcionistas (nome_rec, cpf_rec, senha_rec) VALUES (?, ?)"

    cursor.execute(comando_inserir, (nome_rec, cpf_rec, senha_rec))
        conexao.commit()
        print("RECEPCIONISTA CADASTRADO(A) AO SISTEMA DA RECEPÇÃO!")

    except sqlite3.IntegrityError as e:
        print("Erro! Usuario já cadastrado! ", e)

#--------------------------------------------------------------------------------

print("---LOGIN RECEPCIONISTA---")

def login_rec():
    nome_rece = input("Nome: ")
    senha_rece = input("Insira a senha: ")
#-------------------------------------------------------------------------------

print("---LOGIN ALUNO---")
def login_aluno():
    email_aluno = input("Informe o email: ")
    senha_aluno = input("Insira a senha: ")
    
#-------------------------------------------------------------------------------

print("---LOGIN PERSONAL---")
def login_personal():
    email_personal = input("Informe o email: ")
    senha_personal = input("Informe a senha: ")

#-------------------------------------------------------------------------------

print("---CADASTRO PARA SISTEMA GERENTE---")
def cadastrar_gerente():
    nome_ger = input("Nome: ")
    cpf_ger = input("CPF: ")
    senha_ger = int(input("Insira a senha: "))
    comando_inserir = "INSERT INTO gerentes (nome_ger, cpf_ger, senha_ger) VALUES (?, ?, ?)"

    cursor.execute(comando_inserir, (nome_ger, cpf_ger, senha_ger))
        conexao.commit()
        print("GERENTE CADASTRADO(A) AO SISTEMA DA GERENCIA!")

    except sqlite3.IntegrityError as e:
        print("Erro! Usuario já cadastrado! ", e)

print("---LOGIN GERENTE---")
def login_gerente():
    email_gerente = input("Informe o email: ")
    senha_gerente = input("Informe a senha: ")

#------------------------------------------------------------------------------