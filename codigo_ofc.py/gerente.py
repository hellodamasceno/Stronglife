import sqlite3
from mensalidades import menu_planos
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

def gerenciar_mensalidades():
    menu_planos()


    while opcao != 5:

        print("\n====== GERENCIAR PLANOS ======")
        print("1 - Cadastrar plano")
        print("2 - Listar planos")
        print("3 - Atualizar plano")
        print("4 - Excluir plano")
        print("5 - Voltar")

    try:
         opcao = imput("Digite a opção desejada: ")


        if opcao == 1: cadastrar_plano()
        elif opcao == 2: listar_planos()
        elif opcao == 3: atualizar_plano()
        elif opcao == 4: excluir_plano()
        elif opcao == 5:
            print("Programa encerrado!")
            break

    except ValueError:
            print("Digite uma opção válida!")



