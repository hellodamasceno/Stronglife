import sqlite3

from personsl import montar_treino, visualizar_ficha_aluno

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

def menu():

    try:
        while True:
            print("\n=== ACADEMIA - SISTEMA DE CONTROLE ===")
            print("1. Montar Treino do Aluno (Apenas Personal)")
            print("2. Ver Ficha e Agendamento do Aluno")
            print("3. Sair")

            opcao = int(input("Selecione uma opção: "))


            match opcao:
                case 1:
                    montar_treino()
                case 2:
                    vincular_treino_aluno()
                case 3:
                    print("Encerrando o sistema...")
                    break
                case _:
                    print("Opção inválida! Tente novamente.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado no menu: {e}")

menu()