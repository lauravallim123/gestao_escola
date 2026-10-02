import sqlite3
import pytest
from database import criar_tabelas


@pytest.fixture
def db_conn():
    """Fixture que fornece uma conexão ativa com o banco em memória e tabelas criadas."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    criar_tabelas(conn=conn)
    yield conn
    conn.close()


def test_criacao_tabelas(db_conn):
    """Testa se todas as 6 tabelas exigidas foram criadas corretamente."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas_existentes = [row[0] for row in cursor.fetchall()]

    tabelas_esperadas = ["ALUNOS", "TURMAS", "DISCIPLINAS", "ALUNO_TURMA", "NOTAS", "FREQUENCIAS"]

    for t in tabelas_esperadas:
        assert t in tabelas_existentes, f"A tabela {t} não foi encontrada."


def test_insercao_aluno_e_unicidade_email(db_conn):
    """Testa a inserção e a restrição UNIQUE do e-mail do aluno."""
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO ALUNOS (nome, email, idade) VALUES ('João', 'joao@email.com', 15)")
    db_conn.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO ALUNOS (nome, email, idade) VALUES ('Maria', 'joao@email.com', 16)")
        db_conn.commit()


def test_insercao_nota(db_conn):
    """Testa a inserção de nota associando aluno, turma e disciplina."""
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO ALUNOS (nome, email, idade) VALUES ('Carlos', 'carlos@email.com', 17)")
    cursor.execute("INSERT INTO TURMAS (nome, ano_letivo, periodo) VALUES ('3º Ano B', 2026, 'Vespertino')")
    cursor.execute("INSERT INTO DISCIPLINAS (nome, codigo, carga_horaria) VALUES ('Física', 'FIS101', 60)")

    aluno_id = cursor.lastrowid
    turma_id = 1
    disciplina_id = 1

    cursor.execute("""
        INSERT INTO NOTAS (aluno_id, turma_id, disciplina_id, nota, etapa)
        VALUES (?, ?, ?, ?, ?)
    """, (aluno_id, turma_id, disciplina_id, 8.5, 1))
    db_conn.commit()

    cursor.execute("SELECT nota FROM NOTAS WHERE aluno_id = ?", (aluno_id,))
    res = cursor.fetchone()
    assert res[0] == 8.5