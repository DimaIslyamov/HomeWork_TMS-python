# Техническое задание

## Консольное приложение «Библиотека»

**Вариант:** 1 — Библиотека  
**Тип:** консольное приложение  
**СУБД:** SQLite  
**Доступ к данным:** raw SQL (без ORM)  
**Язык:** Python 3.10+

---

# 1. Цель проекта

Создать приложение для управления библиотекой.

Система должна позволять:

- управлять книгами;
- управлять авторами;
- управлять жанрами;
- связывать книги с авторами;
- связывать книги с жанрами;
- выполнять CRUD операции;
- выполнять сложный поиск через SQL JOIN.

Главная учебная цель:

- понять связи Many-To-Many;
- закрепить JOIN;
- разделить приложение на слои.

---

# 2. Стек

| Компонент | Технология |
|---|---|
| Язык | Python 3.10+ |
| БД | SQLite |
| Работа с БД | sqlite3 raw SQL |
| Модели | dataclass |
| Типизация | typing |
| Стиль | flake8 |
| Проверка типов | mypy |

---

# 3. Структура проекта

```
library_system/
├── main.py
├── Makefile
├── setup.cfg
├── requirements.txt
├── requirements-dev.txt
│
├── data/
│   └── library.db
│
├── models/
│   ├── __init__.py
│   └── entities.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.py
│
├── repositories/
│   ├── __init__.py
│   ├── interfaces.py
│   ├── base.py
│   ├── authors.py
│   ├── books.py
│   └── genres.py
│
├── services/
│   └── search.py
│
└── cli/
    ├── helpers.py
    └── menu.py
```

---

# 4. Модели данных

Файл:

`models/entities.py`

Использовать @dataclass.

## Author

Поля:

- id Optional[int]
- first_name str
- last_name str
- birth_year Optional[int]


## Genre

Поля:

- id Optional[int]
- name str


## Book

Поля:

- id Optional[int]
- title str
- year int
- description str

---

# 5. Схема базы данных

## authors

- id PRIMARY KEY
- first_name
- last_name
- birth_year


## books

- id PRIMARY KEY
- title
- year
- description


## genres

- id PRIMARY KEY
- name UNIQUE


---

# Связующие таблицы

## books_authors

- book_id FK
- author_id FK

PRIMARY KEY(book_id, author_id)


## books_genres

- book_id FK
- genre_id FK

PRIMARY KEY(book_id, genre_id)


Связи:

```
authors
   |
books_authors
   |
books


books
   |
books_genres
   |
genres
```

---

# 6. Repository Pattern

Создать интерфейсы:

## IRepository[T]

Методы:

- add(entity) -> int
- get_by_id(id)
- get_all()
- update(entity)
- delete(id)


## ISearchRepository[T]

Дополнительно:

- search_by_name(pattern)


## AuthorRepository

Дополнительно:

- get_by_name()
- get_books(author_id)


## GenreRepository

Дополнительно:

- get_by_name()
- get_books(genre_id)


## BookRepository

Дополнительно:

- add_author(book_id, author_id)
- add_genre(book_id, genre_id)
- get_authors(book_id)
- get_genres(book_id)
- search_by_author()
- search_by_genre()

---

# 7. Функционал

## Авторы

CRUD:

- создать
- показать всех
- найти
- изменить
- удалить


## Жанры

CRUD полностью.


## Книги

CRUD +

- добавить автора книге
- добавить жанр книге
- показать авторов книги
- показать жанры книги

---

# 8. Сложные операции

## Найти книгу по автору

Использовать:

JOIN books_authors


## Найти книгу по жанру

Использовать:

JOIN books_genres


## Частичный поиск

Например:

"мар"

найдет:

"Мартин"

Использовать Python:

casefold()

---

# 9. CLI меню

Главное меню:

```
1. Авторы
2. Книги
3. Жанры
4. Поиск
0. Выход
```

---

# 10. Порядок выполнения

## Этап 1

- создать проект
- создать venv
- создать папки


## Этап 2

Создать модели:

- Author
- Book
- Genre


## Этап 3

База данных:

- connection.py
- schema.py


## Этап 4

Репозитории:

- AuthorRepository
- GenreRepository
- BookRepository


## Этап 5

Реализовать связи:

Book + Author

Book + Genre


## Этап 6

JOIN поиск.


## Этап 7

CLI.

---

# 11. Проверочный сценарий

1. Добавить автора:

Джордж Мартин

2. Добавить жанр:

Фэнтези

3. Добавить книгу:

Игра престолов

4. Связать книгу и автора

5. Связать книгу и жанр

6. Найти книгу через автора

Ожидаемый результат:

Игра престолов

---

# 12. Готовность проекта

- [ ] Есть модели
- [ ] Есть SQLite схема
- [ ] Есть M:N связи
- [ ] CRUD работает
- [ ] JOIN работает
- [ ] Repository Pattern используется
- [ ] CLI без SQL
- [ ] Код проходит flake8
- [ ] Код проходит mypy

