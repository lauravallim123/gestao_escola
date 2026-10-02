from database import conectar, criar_tabelas


def popular_dados_iniciais():
    """Insere dados de teste para validação das regras de integridade."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO ALUNOS (nome, email, idade, data_nascimento)
        VALUES ('Ana Silva', 'ana.silva@escola.com', 16, '2008-05-14')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO TURMAS (nome, ano_letivo, periodo)
        VALUES ('1º Ano EM - Turma A', 2026, 'Matutino')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO DISCIPLINAS (nome, codigo, carga_horaria)
        VALUES ('Matemática', 'MAT101', 80)
    """)

    conn.commit()

    aluno_id = cursor.execute("SELECT id FROM ALUNOS WHERE email = 'ana.silva@escola.com'").fetchone()[0]
    turma_id = cursor.execute("SELECT id FROM TURMAS WHERE nome = '1º Ano EM - Turma A'").fetchone()[0]
    disciplina_id = cursor.execute("SELECT id FROM DISCIPLINAS WHERE codigo = 'MAT101'").fetchone()[0]

    cursor.execute("""
        INSERT INTO ALUNO_TURMA (aluno_id, turma_id)
        VALUES (?, ?)
    """, (aluno_id, turma_id))

    cursor.execute("""
        INSERT INTO NOTAS (aluno_id, turma_id, disciplina_id, nota, etapa)
        VALUES (?, ?, ?, ?, ?)
    """, (aluno_id, turma_id, disciplina_id, 9.5, 1))

    cursor.execute("""
        INSERT INTO FREQUENCIAS (aluno_id, turma_id, disciplina_id, data_aula, presente)
        VALUES (?, ?, ?, '2026-03-01', 1)
    """, (aluno_id, turma_id, disciplina_id))

    conn.commit()
    conn.close()


def exibir_relatorio():
    """Exibe um resumo das informações cadastradas."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.nome, t.nome, d.nome, n.nota, f.presente
        FROM NOTAS n
        JOIN ALUNOS a ON n.aluno_id = a.id
        JOIN TURMAS t ON n.turma_id = t.id
        JOIN DISCIPLINAS d ON n.disciplina_id = d.id
        JOIN FREQUENCIAS f ON f.aluno_id = a.id AND f.disciplina_id = d.id
    """)

    registros = cursor.fetchall()
    print("\n=== RELATÓRIO DO PROJETO GESTÃO ESCOLAR ===")
    for reg in registros:
        print(f"Aluno: {reg[0]} | Turma: {reg[1]} | Disciplina: {reg[2]} | Nota: {reg[3]} | Presença: {'Sim' if reg[4] == 1 else 'Não'}")

    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    popular_dados_iniciais()
    exibir_relatorio()