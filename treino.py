import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

def montar_treino():

    try:
        exercicios_maquina = [
        ("Leg Press 45º",), ("Extensora",), ("Flexora Horizontal",),
        ("Puxada Alta na Polia",), ("Remada Baixa na Máquina",), ("Supino Sentado na Máquina",),
        ("Desenvolvimento de Ombros Máquina",), ("Tríceps Corda Polia",),
        ("Rosca Biceps na Polia",), ("Cadeira Abdutora/Adutora",)
    ]
        cursor.executemany("INSERT OR IGNORE INTO exercicios (nome) VALUES (?)", exercicios_maquina) 
        conexao.commit()
        
    except sqlite3.Error as erro:
        print(f"Erro ao inicializar o banco de dados: {erro}")
    finally:
        if conexao:
            conexao.close()

    print("\n--- CONFIGURAÇÃO DE TREINO (ÁREA DO PERSONAL) ---")
        
        id_personal = int(input("Digite o ID do Personal que está montando o treino: "))
        cursor.execute("SELECT nome_personal FROM personal WHERE id = ?", (id_personal,))
        personal_valido = cursor.fetchone()
        
        if not personal_valido:
            print(" Acesso Negado: Apenas um Personal cadastrado pode prescrever treinos.")
            return
            
        print(f" Identidade Confirmada: Professor(a) {personal_valido[0]}")
        
        id_aluno = int(input("Digite o ID do Aluno que receberá o treino: "))
        
        cursor.execute("SELECT nome_aluno, status_acompanhamento FROM alunos WHERE id = ?", (id_aluno,))
        aluno_dados = cursor.fetchone()
        if not aluno_dados:
            print(" Erro: Aluno não encontrado.")
            return
            
        print(f"Montando treino para: {aluno_dados[0]} ({aluno_dados[1]})")
        dia_semana = input("Qual o dia da semana deste treino? (ex: Segunda): ")

        cursor.execute("SELECT * FROM exercicios")
        maquinas = cursor.fetchall()
        print("\n--- MÁQUINAS DISPONÍVEIS ---")
        for m in maquinas:
            print(f"[{m[0]}] - {m[1]}")
            
        print("\nSelecione até 6 exercícios digitando os IDs das máquinas:")
        exercicios_escolhidos = []
        
        for i in range(1, 7):
            escolha = input(f"ID da {i}ª máquina (ou pressione Enter para encerrar): ")
            if escolha == "":
                break
            exercicios_escolhidos.append(int(escolha))
            
        if not exercicios_escolhidos:
            print("Nenhum exercício foi selecionado pelo personal.")
            return

        for id_ex in exercicios_escolhidos:
            cursor.execute('''
                INSERT INTO treinos_diarios (id_aluno, dia_semana, id_exercicio) 
                VALUES (?, ?, ?)''', (id_aluno, dia_semana, id_ex))
                
        conexao.commit()
        print(f" Treino de {dia_semana} salvou com sucesso para o aluno pelo Personal!")
        
    except ValueError:
        print("Erro: Digite apenas números válidos para os IDs.")
    except sqlite3.Error as e:
        print(f"Erro ao vincular treino: {e}")
    finally:
        if conexao:
            conexao.close()

    def visualizar_ficha_aluno():
    
        try:
            conexao = sqlite3.connect('sistema_academia.db')
            cursor = conexao.cursor()
        
            id_aluno = int(input("\nDigite o ID do aluno para ver a ficha detalhada: "))
        
            cursor.execute('''
                SELECT a.nome_aluno, a.idade, a.status_acompanhamento, a.dia_aula, a.horario_aula, p.nome_personal 
                FROM alunos a 
                JOIN personal p ON a.id_personal = p.id 
                WHERE a.id = ?''', (id_aluno,))
            dados = cursor.fetchone()
        
            if not dados:
            print("Aluno não encontrado.")
            return
            
            print("\n=======================================================")
            print(f"FICHA COMPLETA DO ALUNO(A): {dados[0]}")
            print(f"Idade: {dados[1]} anos | {dados[2]}")
            print(f"Personal Responsável: Prof. {dados[5]}")
            print(f"Agendamento de Aula Fixa: {dados[3]} às {dados[4]}")
            print("=======================================================")
        
        cursor.execute('''
            SELECT td.dia_semana, e.nome 
            FROM treinos_diarios td
            JOIN exercicios e ON td.id_exercicio = e.id
            WHERE td.id_aluno = ?
            ORDER BY td.dia_semana''', (id_aluno,))
        treinos = cursor.fetchall()
        
        if not treinos:
            print("Nenhuma rotina de exercícios montada para este aluno.")
        else:
            agenda = {}
            for dia, ex in treinos:
                if dia not in agenda:
                    agenda[dia] = []
                agenda[dia].append(ex)
                
            for dia, lista_ex in agenda.items():
                print(f"\n[Treino de {dia.upper()}]:")
                for index, ex_nome in enumerate(lista_ex, 1):
                    print(f"   {index}º exercício: {ex_nome}")
        print("=======================================================")
        
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
    except sqlite3.Error as e:
        print(f"Erro ao buscar ficha do aluno: {e}")
    finally:
        if conexao:
            conexao.close()