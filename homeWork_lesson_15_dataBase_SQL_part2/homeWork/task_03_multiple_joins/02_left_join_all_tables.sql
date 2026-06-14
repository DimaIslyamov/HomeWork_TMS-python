SELECT

	b.title,
    a.first_name || ' ' || a.last_name AS author,
    s.quantity

FROM authors AS a

LEFT JOIN books AS b
	ON a.id = b.author_id

LEFT JOIN sales AS s
	ON b.id = s.book_id;