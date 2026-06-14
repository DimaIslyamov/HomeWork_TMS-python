INSERT INTO authors (first_name, last_name) VALUES
('Robert', 'Martin'),
('Martin', 'Fowler'),
('Eric', 'Freeman'),
('Joshua', 'Bloch'),
('Kent', 'Beck'); -- автор без книг для проверки LEFT JOIN

INSERT INTO books (title, author_id, publication_year) VALUES
('Clean Code', 1, 2008),
('Clean Architecture', 1, 2017),
('Refactoring', 2, 1999),
('Head First Design Patterns', 3, 2004),
('Effective Java', 4, 2001),
('Java Concurrency in Practice', 4, 2006) -- книга без продаж
'Unknown Book', NULL, 2025); -- книга без автора RIGHT JOIN

INSERT INTO sales (book_id, quantity) VALUES
(1, 150),
(1, 80),
(2, 120),
(3, 90),
(3, 40),
(4, 200),
(5, 170);