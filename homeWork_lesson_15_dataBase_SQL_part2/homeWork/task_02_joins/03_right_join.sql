SELECT
    b.title,
    a.first_name,
    a.last_name
FROM authors AS a
RIGHT JOIN books AS b
    ON a.id = b.author_id;