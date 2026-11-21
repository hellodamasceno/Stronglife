
def fazer_login(tipo):

    match tipo:

        case "1":
            print("\n--- LOGIN ALUNO ---")
            usuario = input("Digite seu CPF: ")
            senha = input("Digite sua senha: ")

            if usuario == "12345678900" and senha == "123":
                print("Login realizado com sucesso!")
                return True
            else:
                print("CPF ou senha incorretos!")
                return False

        case "2":
            print("\n--- LOGIN PERSONAL ---")
            usuario = input("Digite seu CPF: ")
            senha = input("Digite sua senha: ")

            if usuario == "98765432100" and senha == "123":
                print("Login realizado com sucesso!")
                return True
            else:
                print("CPF ou senha incorretos!")
                return False
