import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

def mensalidades():
    planos = [
        ("Mensal", 1, 100.00),
        ("Trimestral", 3, 90.00),
        ("Semestral", 6, 80.00),
        ("Anual", 12, 70.00)
    ]

    print("1 - Mensal")
    print("2 - Trimestral")
    print("3 - Semestral")
    print("4 - Anual")

    opcao = int(input("Escolha seu plano: "))

    if opcao == 1:
        print("Plano Mensal - R$ 100,00 por mês")

    elif opcao == 2:
        print("Plano Trimestral - R$ 90,00 por mês")

    elif opcao == 3:
        print("Plano Semestral - R$ 80,00 por mês")

    elif opcao == 4:
        print("Plano Anual - R$ 70,00 por mês")

    else:
        print("Opção inválida!")

mensalidades()