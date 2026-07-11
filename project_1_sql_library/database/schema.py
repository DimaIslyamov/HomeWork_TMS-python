from database.connection import Database


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS authors (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    birth_date  TEXT,
    
    UNIQUE (first_name, last_name, birth_date)
);

CREATE TABLE IF NOT EXISTS books (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    year        INTEGER NOT NULL,
    description  TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS genres (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name        TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS books_authors (
    book_id     INTEGER NOT NULL,
    author_id   INTEGER NOT NULL,
    
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors (id) ON DELETE CASCADE,
    
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS books_genres (
    book_id     INTEGER NOT NULL,
    genre_id   INTEGER NOT NULL,
    
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres (id) ON DELETE CASCADE,
    
    PRIMARY KEY (book_id, genre_id)
);
"""


def init_schema(database: Database) -> None:
    """Create table if not exists"""
    connection = database.connect()
    connection.executescript(SCHEMA_SQL)
    connection.commit()


if __name__ == "__main__":
    with Database() as db:
        init_schema(db)
    print("Database schema created")
