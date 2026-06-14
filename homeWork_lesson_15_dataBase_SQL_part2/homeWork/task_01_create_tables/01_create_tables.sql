CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER,
    publication_year INTEGER,

    FOREIGN KEY (author_id)
    REFERENCES authors(id)
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    book_id INTEGER,
    quantity INTEGER NOT NULL,

    FOREIGN KEY (book_id)
    REFERENCES books(id)
);