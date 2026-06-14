SELECT

    a.first_name || ' ' || a.last_name AS author,
    SUM(s.quantity) AS total_sales

FROM authors AS a

INNER JOIN books AS b
    ON a.id = b.author_id

INNER JOIN sales AS s
    ON b.id = s.book_id

GROUP BY author

HAVING SUM(s.quantity) = (

    SELECT MAX(total)
    FROM (

        SELECT
            SUM(s2.quantity) AS total

        FROM authors AS a2

        INNER JOIN books AS b2
            ON a2.id = b2.author_id

        INNER JOIN sales AS s2
            ON b2.id = s2.book_id

        GROUP BY a2.id
    ) AS result
);