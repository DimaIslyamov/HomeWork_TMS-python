SELECT

	b.title,
    a.first_name || ' ' || a.last_name AS author,
    s.quantity

FROM books AS b

INNER JOIN authors AS a
	ON b.author_id = a.id

INNER JOIN sales AS s
	ON s.book_id = b.id;