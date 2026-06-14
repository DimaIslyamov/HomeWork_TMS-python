SELECT

    a.first_name || ' ' || a.last_name AS author,
    SUM(s.quantity) AS total_sales

FROM authors AS a

LEFT JOIN books AS b
    ON a.id = b.author_id

LEFT JOIN sales AS s
    ON b.id = s.book_id

GROUP BY author;