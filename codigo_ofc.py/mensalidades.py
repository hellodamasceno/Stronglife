import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

def cadastrar_plano():
    
    print("\n---CADASTRAR UM PLANO---")

    nome = input("Qual o nome do plano?(ex: Mensal, Trimestral): ")
    valor = float(input("qual o valor a cobrar desse plano?: "))
    duracao = input("quanto tempo? (ex: 1, 12): ")

    cursor.execute('''
    INSERT INTO planos (nome, valor, duracao)
    VALUES (?, ?, ?)
''', ("?, ?, ?"))

    conexao.commit()

    print("Plano cadastrado!")

def listar_planos():

    print("\n====== PLANOS STRONGLIFE ======\n")

    cursor.execute('SELECT * FROM planos')
    mensalidades = cursor.fetchall()

    if not mensalidades:
        print("Nenhum plano cadastrado!")
        return

    for mensalidade in mensalidades:

        print("ID:", mensalidade[0])
        print("Nome:", mensalidade[1])
        print("Valor: R$", f"{mensalidade[2]:.2f}")
        print("Duração:", mensalidade[3], "meses")
        print("--------------------------")


def atualizar_plano():

    try:
        codigo = int(input("\nInforme o ID do plano que deseja atualizar: "))

        cursor.execute('SELECT id FROM planos WHERE id = ?', (codigo,))
        plano = cursor.fetchone()

        if plano:

            print("\n====== ATUALIZAR PLANO ======")

            nome = input("Novo nome: ")
            duracao = int(input("Nova duração em meses: "))
            valor = float(input("Novo valor: R$ "))

            cursor.execute('''
                UPDATE planos
                SET nome = ?, valor = ?, duracao = ?
                WHERE id = ?
            ''', (nome, valor, duracao, codigo))

            conexao.commit()

            print("Plano atualizado com sucesso!")

        else:
            print("Plano não encontrado!")

    except ValueError:
        print("Digite valores válidos!")

