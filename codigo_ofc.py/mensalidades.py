import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

def cadastrar_plano():
    cursor.execute("""
    INSERT INTO planos (nome, valor, duracao)
    VALUES (?, ?, ?)
""", ("Mensal", 100.00, 30))

    conexao.commit()

    print("Plano cadastrado!")

def listar_planos():

    print("\n====== PLANOS STRONGLIFE ======\n")

    cursor.execute('''SELECT * FROM planos''')
    mensalidades = cursor.fetchall()

    if not mensalidades:
        print("Nenhum plano cadastrado!")
        return

    for mensalidade in mensalidades:

        print("ID:", mensalidade[0])
        print("Plano:", mensalidade[2])
        print("Duração:", mensalidade[3], "meses")
        print("--------------------------")



def atualizar_plano():

    try:
        codigo = int(input("\nInforme o ID do plano que deseja atualizar: "))

        if codigo in planos:

            print("\n====== ATUALIZAR PLANO ======")

            nome = input("Novo nome: ")
            duracao = int(input("Nova duração em meses: "))
            valor = float(input("Novo valor mensal: R$ "))

            planos[codigo] = (nome, duracao, valor)

            print("Plano atualizado com sucesso!")

        else:
            print("Plano não encontrado!")

    except ValueError:
        print("Digite valores válidos!")