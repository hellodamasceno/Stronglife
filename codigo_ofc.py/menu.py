import sqlite3

from alunos import agendar_aula, cancelar_aula, remarcar_aula, visualizar_minha_ficha
from gerente import gerenciar_mensalidades
from mensalidades import atualizar_plano, listar_planos, cadastrar_plano
from personal import montar_treino, visualizar_ficha_aluno
from recepcao import atualizar_cadastro, atualizar_cadastrop, cadastrar_alunos, cadastrar_personal, deletar_aluno, deletar_personal, listar_aluno, listar_personal
from banco import criar_tabela


conexao = sqlite3.connect("sistema_academia.db")
cursor = conexao.cursor()
cursor.execute("PRAGMA foreign_keys = ON")


def menu_aluno():
    while True:
        print("\n--- ÁREA DO ALUNO ---")
        print("1. Agendar aula experimental")
        print("2. Remarcar aula experimental")
        print("3. Cancelar aula experimental")
        print("4. Visualizar minha ficha")
        print("5. Voltar")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                agendar_aula()
            case "2":
                remarcar_aula()
            case "3":
                cancelar_aula()
            case "4":
                visualizar_minha_ficha()
            case "5":
                break
            case _:
                print("Opção inválida!")


def menu_personal():
    while True:
        print("\n--- ÁREA DO PERSONAL ---")
        print("1. Montar treino do aluno")
        print("2. Visualizar ficha do aluno")
        print("3. Voltar")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                montar_treino()
            case "2":
                id_personal = int(input("Digite seu ID de Personal: "))
                visualizar_ficha_aluno(id_personal)
            case "3":
                break
            case _:
                print("Opção inválida!")


def menu_recepcao():
    while True:
        print("\n--- ÁREA DA RECEPÇÃO ---")
        print("1. Cadastrar aluno")
        print("2. Listar alunos")
        print("3. Atualizar cadastro de aluno")
        print("4. Deletar aluno")
        print("5. Cadastrar personal")
        print("6. Listar personais")
        print("7. Atualizar cadastro de personal")
        print("8. Deletar personal")
        print("9. Voltar")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                cadastrar_alunos()
            case "2":
                listar_aluno()
            case "3":
                atualizar_cadastro()
            case "4":
                deletar_aluno()
            case "5":
                cadastrar_personal()
            case "6":
                listar_personal()
            case "7":
                atualizar_cadastrop()
            case "8":
                deletar_personal()
            case "9":
                break
            case _:
                print("Opção inválida!")


def menu_gerente():
    while True:
        print("\n--- ÁREA DO GERENTE ---")
        print("1. Gerenciar mensalidades")
        print("2. Listar planos")
        print("3. Atualizar planos")
        print("4. Voltar")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                gerenciar_mensalidades()
            case "2":
                listar_planos()
            case "3":
                atualiza_planos()
            case "4":
                break
            case _:
                print("Opção inválida!")


def menu():
        while True:
            print("\n=== ACADEMIA - SISTEMA DE CONTROLE ===")
            print("1. Área do Aluno")
            print("2. Área do Personal")
            print("3. Área da Recepção")
            print("4. Área do Gerente")
            print("5. Sair")

            opcao = input("Selecione uma opção: ")

            match opcao:
                case "1":
                    menu_aluno()
                case "2":
                    menu_personal()
                case "3":
                    menu_recepcao()
                case "4":
                    menu_gerente()
                case "5":
                    print("Encerrando o sistema...")
                    break
                case _:
                    print("Opção inválida! Tente novamente.")


criar_tabela()
menu()
cadastrar_plano
cadastrar_personal