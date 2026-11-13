import sqlite3
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()



planos = {
    1: ("Mensal", 1, 100.00),
    2: ("Trimestral", 3, 90.00),
    3: ("Semestral", 6, 80.00),
    4: ("Anual", 12, 70.00)
}

def cadastrar_plano():

    try:
        print("\n====== CADASTRAR PLANO ======")

        codigo = int(input("Informe o ID do plano: "))

        if codigo in planos:
            print("Esse ID já está cadastrado!")
            return

        nome = input("Informe o nome do plano: ")
        duracao = int(input("Informe a duração em meses: "))
        valor = float(input("Informe o valor mensal: R$ "))

        planos[codigo] = (nome, duracao, valor)

        print("Plano cadastrado com sucesso!")

    except ValueError:
        print("Digite valores válidos!")



def listar_planos():

    print("\n====== PLANOS STRONGLIFE ======\n")

    if not planos:
        print("Nenhum plano cadastrado!")
        return

    for codigo, plano in planos.items():

        nome, duracao, valor = plano

        print("ID:", codigo)
        print("Plano:", nome)
        print("Duração:", duracao, "meses")
        print("Valor mensal: R$", valor)
        print("Valor total: R$", duracao * valor)
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



   
def excluir_plano():

    try:
        print("\n====== EXCLUIR PLANO ======")

        id_plano = int(input("Informe o ID do plano que deseja excluir: "))

        cursor.execute("SELECT nome FROM mensalidades WHERE id = ?", (id_plano,))
        plano = cursor.fetchone()

        if plano:
            cursor.execute("DELETE FROM mensalidades WHERE id = ?", (id_plano,))
            conexao.commit()

            print(f"Plano '{plano[0]}' removido com sucesso!")

        else:
            print("Erro: Plano não encontrado com o ID informado.")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro!")

    except sqlite3.Error as e:
        print(f"Erro ao deletar plano: {e}")

    finally:
        conexao.close()
           


def menu_planos():

    opcao = 0

    while opcao != 5:

        print("\n====== GERENCIAR PLANOS ======")
        print("1 - Cadastrar plano")
        print("2 - Listar planos")
        print("3 - Atualizar plano")
        print("4 - Excluir plano")
        print("5 - Voltar")

        try:
            opcao = int(input("\nEscolha uma opção: "))

            if opcao == 1:
                cadastrar_plano()

            elif opcao == 2:
                listar_planos()

            elif opcao == 3:
                atualizar_plano()

            elif opcao == 4:
                excluir_plano()

            elif opcao == 5:
                print("Voltando ao menu principal...")

            else:
                print("Opção inválida!")

        except ValueError:
            print("Digite uma opção válida!")


#chamar apenas no do gerente