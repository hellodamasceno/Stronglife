import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()



def mensalidades():
    planos = {
        1: ("Mensal", 1, 100.00),
        2: ("Trimestral", 3, 90.00),
        3: ("Semestral", 6, 80.00),
        4: ("Anual", 12, 70.00)
    }

    print("\n====== PLANOS STRONGLIFE ======\n")

    for codigo, plano in planos.items():

        nome, duracao, valor = plano

        print(codigo, "-", nome)
        print("Duração:", duracao, "meses")
        print("Valor mensal: R$", valor)
        print("Valor total: R$", duracao * valor)
        print()

    try:
        opcao = int(input("Escolha seu plano: "))
    except ValueError:
        print("Digite uma opção válida!")
        return None

    if opcao not in planos:
        print("Opção inválida!")
        return None

    nome_plano, duracao, valor_mensal = planos[opcao]

    valor_total = duracao * valor_mensal

    print("\n====== PLANO ESCOLHIDO ======")
    print("Plano:", nome_plano)
    print("Duração:", duracao, "meses")
    print("Valor mensal: R$", valor_mensal)
    print("Valor total: R$", valor_total)

    confirmar = input("\nDeseja continuar? (S/N): ")

    if confirmar != "S" and confirmar != "s":
        print("Contrato cancelado!")
        return None

    return nome_plano, valor_mensal


def cadastrar_mensalidade(id_aluno, plano, valor):

    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO mensalidades
            (id_aluno, plano, valor, status)
            VALUES (?, ?, ?, ?)
        """, (id_aluno, plano, valor, "Pendente"))

        conexao.commit()
        print("Mensalidade cadastrada com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao cadastrar mensalidade: {e}")

    finally:
        conexao.close()