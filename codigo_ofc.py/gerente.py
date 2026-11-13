import sqlite3
from mensalidades import listar_planos, atualizar_plano
conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()

def gerenciar_mensalidades():
    menu_planos()