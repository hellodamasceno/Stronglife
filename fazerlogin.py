print("FAZER LOGIN - STRONG LIFE")
print("1 - LOGIN ALUNO | 2 - LOGIN PERSONAL | 3 - LOGIN RECEPCIONISTA")

opcao = int(input("Digite a opção: "))

match opcao:

    case 1:
        print("LOGIN ALUNO")
        usuario_aluno = input("Digite o seu CPF: ")
        senha = input("Digite sua senha: ")

        print(f"Login no CPF {usuario_aluno} realizado")

    case 2:
        print("LOGIN PERSONAL")
        usuario = input("Digite o seu CPF: ")
        senha = input("Digite sua senha: ")

        print(f"Login no CPF {usuario} realizado")

    case 3:
        print("LOGIN RECEPCIONISTA")
        recepcionista = input("Digite o nome da recepcionista: ")
        recepcionista_senha = input("Digite sua senha: ")

        print(f"Login da recepcionista {recepcionista} realizado")

        print("REGISTRAR PRESENÇA ALUNO")
        nome_aluno = input("Digite o nome do aluno: ")
        data = input("Digite a data da presença: ")

        print(f"Presença do {nome_aluno} na data {data} registrada")

    case _:
        print("Opção inválida")


