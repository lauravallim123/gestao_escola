import sqlite3

DB_NAME = "gestao_escolar.db"


def conectar(db_path=DB_NAME):
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def criar_tabelas(conn=None, db_path=DB_NAME):
    """Cria todas as 6 tabelas do Projeto Gestão Escolar."""
    fechar_ao_final = False
    if conn is None:
        conn = conectar(db_path)
        fechar_ao_final = True

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ALUNOS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        idade INTEGER NOT NULL,
        data_nascimento DATE,
        ativo INTEGER NOT NULL DEFAULT 1,
        criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TURMAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ano_letivo INTEGER NOT NULL,
        periodo TEXT NOT NULL,
        ativo INTEGER NOT NULL DEFAULT 1,
        criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DISCIPLINAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        carga_horaria INTEGER NOT NULL,
        ativo INTEGER NOT NULL DEFAULT 1,
        criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ALUNO_TURMA (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        turma_id INTEGER NOT NULL,
        data_matricula DATE NOT NULL DEFAULT CURRENT_DATE,
        FOREIGN KEY (aluno_id) REFERENCES ALUNOS(id) ON DELETE CASCADE,
        FOREIGN KEY (turma_id) REFERENCES TURMAS(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS NOTAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        turma_id INTEGER NOT NULL,
        disciplina_id INTEGER NOT NULL,
        nota REAL NOT NULL,
        etapa INTEGER NOT NULL,
        data_lancamento DATE NOT NULL DEFAULT CURRENT_DATE,
        FOREIGN KEY (aluno_id) REFERENCES ALUNOS(id) ON DELETE CASCADE,
        FOREIGN KEY (turma_id) REFERENCES TURMAS(id) ON DELETE CASCADE,
        FOREIGN KEY (disciplina_id) REFERENCES DISCIPLINAS(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FREQUENCIAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        turma_id INTEGER NOT NULL,
        disciplina_id INTEGER NOT NULL,
        data_aula DATE NOT NULL,
        presente INTEGER NOT NULL,
        FOREIGN KEY (aluno_id) REFERENCES ALUNOS(id) ON DELETE CASCADE,
        FOREIGN KEY (turma_id) REFERENCES TURMAS(id) ON DELETE CASCADE,
        FOREIGN KEY (disciplina_id) REFERENCES DISCIPLINAS(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    if fechar_ao_final:
        conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados e tabelas criados com sucesso!")