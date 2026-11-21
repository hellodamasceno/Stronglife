import sqlite3

conexao = sqlite3.connect('sistema_academia.db')
cursor = conexao.cursor()


def agendar_aula():

    print("\n>>> AGENDAR AULA EXPERIMENTAL <<<")

    cpf = input("Digite o CPF: ").strip()

    cursor.execute('SELECT id FROM alunos WHERE cpf = ?', (cpf,))

    if cursor.fetchone():
        print('Esta pessoa já está cadastrada como aluno!')
        return

    cursor.execute('SELECT id FROM aulas_experimentais WHERE cpf = ?', (cpf,))

    if cursor.fetchone():
        print("Esta pessoa já possui uma aula experimental agendada!")
        return

    nome = input("Digite o nome: ").strip()
    data = input("Digite a data da aula (DD/MM/AAAA): ").strip()
    horario = input("Digite o horário da aula (HH:MM): ").strip()

    cursor.execute('''
        INSERT INTO aulas_experimentais (cpf, aluno, data, horario, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (cpf, nome, data, horario, "Agendada"))

    conexao.commit()

    print("Aula experimental agendada com sucesso!")


def remarcar_aula():
    print("\n>>> REMARCAR AULA EXPERIMENTAL <<<")
    cpf = input("Digite o CPF: ").strip()

    with conectar() as conexao:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT cpf, aluno, data, horario FROM aulas_experimentais WHERE cpf = ?',
            (cpf,),
        )
        aula = cursor.fetchone()

        if not aula:
            print("Nenhuma aula experimental encontrada para este CPF.")
            return

        print("\nAgendamento encontrado!")
        print(f"Nome: {aula[1]}")
        print(f"Data atual: {aula[2]}")
        print(f"Horário atual: {aula[3]}")

        nova_data = input("\nDigite a nova data (DD/MM/AAAA): ").strip()
        novo_horario = input("Digite o novo horário (HH:MM): ").strip()

        cursor.execute(
            '''
            UPDATE aulas_experimentais
            SET data = ?, horario = ?, status = 'Remarcada'
            WHERE cpf = ?
            ''',
            (nova_data, novo_horario, cpf),
        )
        conexao.commit()
        print("Aula remarcada com sucesso!")


def cancelar_aula():
    print("\n>>> CANCELAR AULA EXPERIMENTAL <<<")
    cpf = input("Digite o CPF: ").strip()

    with conectar() as conexao:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT cpf, aluno, data, horario FROM aulas_experimentais WHERE cpf = ?',
            (cpf,),
        )
        aula = cursor.fetchone()

        if not aula:
            print("Nenhuma aula experimental encontrada para este CPF.")
            return

        print("\nAgendamento encontrado!")
        print(f"Nome: {aula[1]}")
        print(f"Data: {aula[2]}")
        print(f"Horário: {aula[3]}")

        confirmar = input("\nDeseja realmente cancelar? (S/N): ").strip().upper()

        if confirmar == "S":
            cursor.execute('DELETE FROM aulas_experimentais WHERE cpf = ?', (cpf,))
            conexao.commit()
            print("Aula cancelada com sucesso!")
        else:
            print("Cancelamento não realizado.")


def visualizar_minha_ficha():
    print('\n---- MINHA FICHA ----')

    try:
        id_aluno = int(input("Informe o seu ID: "))
    except ValueError:
        print("ID inválido! Digite apenas números.")
        return

    cursor.execute('''
        SELECT alunos.id, alunos.nome_aluno, alunos.idade,
            alunos.status_acompanhamento, alunos.dia_aula,
            alunos.horario_aula, personais.nome, planos.nome
        FROM alunos
        LEFT JOIN personais ON alunos.id_personal = personais.id
        LEFT JOIN planos ON alunos.id_plano = planos.id
        WHERE alunos.id = ?
    ''', (id_aluno,))

    dados = cursor.fetchone()
    if not dados:
        print("Ficha não encontrada!")
        return

        personal = dados[6] if dados[6] else "Não atribuído"
        plano = dados[7] if dados[7] else "Sem plano"
        status = dados[3] if dados[3] else "Sem status"
        dia = dados[4] if dados[4] else "Não definido"
        horario = dados[5] if dados[5] else "Não definido"

        print(
            f"\nID: {dados[0]} | NOME: {dados[1]} | IDADE: {dados[2]} | "
            f"STATUS: {status} | PERSONAL: {personal} | PLANO: {plano} | "
            f"AULA: {dia} às {horario}"
        )

        cursor.execute(
            '''
            SELECT treinos_diarios.dia_semana, exercicios.nome
            FROM treinos_diarios
            JOIN exercicios ON treinos_diarios.id_exercicio = exercicios.id
            WHERE treinos_diarios.id_aluno = ?
            ''',
            (id_aluno,),
        )
        treinos = cursor.fetchall()

        print("\n---- MEUS TREINOS ----")
        if not treinos:
            print("Você ainda não tem treinos cadastrados.")
        else:
            for treino in treinos:
                print(f"DIA: {treino[0]} | EXERCÍCIO: {treino[1]}")