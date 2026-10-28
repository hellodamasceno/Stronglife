import sqlite3

# --- 1. CONFIGURAÇÃO INICIAL DO BANCO DE DADOS ---

def inicializar_banco():
    """Cria todas as tabelas necessárias e popula os 10 exercícios de máquina."""
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Tabela de Personais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_personal TEXT NOT NULL,
                idade INTEGER NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                numero_de_telefone TEXT NOT NULL
            )''')

        # Tabela de Alunos (Adicionado campos de agendamento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_aluno TEXT NOT NULL,
                idade INTEGER NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                mensalidade REAL NOT NULL,
                id_personal INTEGER NOT NULL,
                dia_aula TEXT NOT NULL,
                horario_aula TEXT NOT NULL,
                status_acompanhamento TEXT NOT NULL,
                FOREIGN KEY (id_personal) REFERENCES personal(id) ja tem tabela
            )''')
            
        # Tabela de Exercícios de Máquina
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )''')
            
        # Tabela de Treinos Diários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treinos_diarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_aluno INTEGER NOT NULL,
                dia_semana TEXT NOT NULL,
                id_exercicio INTEGER NOT NULL,
                FOREIGN KEY (id_aluno) REFERENCES alunos(id),
                FOREIGN KEY (id_exercicio) REFERENCES exercicios(id) JA tem tabela
            )''')
            
        conexao.commit()

        exercicios_maquina = [
            ("Leg Press 45º",), ("Extensora",), ("Flexora Horizontal",),
            ("Puxada Alta na Polia",), ("Remada Baixa na Máquina",), ("Supino Sentado na Máquina",),
            ("Desenvolvimento de Ombros Máquina",), ("Tríceps Corda Polia",),
            ("Rosca Biceps na Polia",), ("Cadeira Abdutora/Adutora",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO exercicios (nome) VALUES (?)", exercicios_maquina) # Verificar isso
        conexao.commit()
        
    except sqlite3.Error as erro:
        print(f"Erro ao inicializar o banco de dados: {erro}")
    finally:
        if conexao:
            conexao.close()

def cadastrar_personal():
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        print("\n--- CADASTRO DE PERSONAL ---")
        nome = input("Nome do Personal: ")
        idade = int(input("Idade: "))
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        
        cursor.execute('''
            INSERT INTO personal (nome_personal, idade, cpf, numero_de_telefone) 
            VALUES (?, ?, ?, ?)''', (nome, idade, cpf, telefone))
            
        conexao.commit()
        print(f"Personal {nome} cadastrado com sucesso!")
        
    except ValueError:
        print("Erro: Idade deve ser um número inteiro.")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados ao cadastrar personal: {e}")
    finally:
        if conexao:
            conexao.close()

def listar_personais():
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id, nome_personal, numero_de_telefone FROM personal")
        personais = cursor.fetchall()
        
        print("\n--- PERSONAIS DISPONÍVEIS ---")
        if not personais:
            print("Nenhum personal cadastrado.")
            return []
            
        for p in personais:
            print(f"ID: {p[0]} | Nome: {p[1]} | Contato: {p[2]}")
        return personais
        
    except sqlite3.Error as e:
        print(f"Erro ao listar personais: {e}")
        return []
    finally:
        if conexao:
            conexao.close()


def cadastrar_aluno():
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
        print("\n--- CADASTRO DE NOVO ALUNO ---")
        nome = input("Nome do aluno: ")
        idade = int(input("Idade do aluno: "))
        
        if idade < 12:
            print(" Menor de 12 anos só pode treinar se for acompanhado DIRETAMENTE por um Personal.")
            status_acompanhamento = "Apenas acompanhado por Personal"
        elif idade < 18:
            permissao = input("Possui permissão assinada pelos pais? (S/N): ").strip().upper()
            if permissao == "S":
                print(" Permissão confirmada. Pode treinar sozinho.")
                status_acompanhamento = "Menor com permissão dos pais"
            else:
                print(" Cadastro Negado: Menores de 18 anos precisam de permissão dos pais para treinar sozinhos.")
                return
        else:
            print(" Maior de idade. Treino desacompanhado liberado.")
            status_acompanhamento = "Liberado (Maior de idade)"

        cpf = input("CPF: ")
        mensalidade = float(input("Valor da mensalidade: "))
        
        print("\n--- AGENDAMENTO DA AULA FIXA ---")
        dia_aula = input("Dia da semana para a aula (ex: Segunda-feira): ")
        horario_aula = input("Horário da aula (ex: 14:00): ")

        personais = listar_personais()
        if not personais:
            print(" Erro: Cadastre pelo menos um Personal no sistema antes de cadastrar alunos.")
            return
            
        id_personal = int(input("\nDigite o ID do Personal selecionado para o aluno: "))
        
        cursor.execute("SELECT id FROM personal WHERE id = ?", (id_personal,))
        if not cursor.fetchone():
            print(" Erro: ID de Personal inválido.")
            return

        cursor.execute('''
            INSERT INTO alunos (nome_aluno, idade, cpf, mensalidade, id_personal, dia_aula, horario_aula, status_acompanhamento) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            (nome, idade, cpf, mensalidade, id_personal, dia_aula, horario_aula, status_acompanhamento))
            
        conexao.commit()
        print(f" Aluno {nome} cadastrado com sucesso! Aula agendada para {dia_aula} às {horario_aula}.")
        
    except ValueError:
        print("Erro: Dados numéricos inválidos digitados.")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar aluno: {e}")
    finally:
        if conexao:
            conexao.close()

def vincular_treino_aluno():
    try:
        conexao = sqlite3.connect('sistema_academia.db')
        cursor = conexao.cursor()
        
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
        dia_semana = input("Qual o dia da semana deste treino? (ex: Segunda): ").strip()

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

def menu():
    try:
        inicializar_banco()
        while True:
            print("\n=== ACADEMIA - SISTEMA DE CONTROLE ===")
            print("1. Cadastrar Personal")
            print("2. Listar Personais")
            print("3. Cadastrar Aluno (Com regras de idade e agendamento)")
            print("4. Montar Treino do Aluno (Apenas Personal)")
            print("5. Ver Ficha e Agendamento do Aluno")
            print("0. Sair")
            
            opcao = input("Selecione uma opção: ").strip() # .strip? ver isso
            
            if opcao == "1":
                cadastrar_personal()
            elif opcao == "2":
                listar_personais()
            elif opcao == "3":
                cadastrar_aluno()
            elif opcao == "4":
                vincular_treino_aluno()
            elif opcao == "5":
                visualizar_ficha_aluno()
            elif opcao == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")
                
    except Exception as e:
        print(f"Ocorreu um erro inesperado no menu: {e}")

menu()