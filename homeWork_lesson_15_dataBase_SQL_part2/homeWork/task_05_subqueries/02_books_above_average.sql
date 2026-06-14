SELECT

    b.title,
    SUM(s.quantity) AS total_sales

FROM books AS b

INNER JOIN sales AS s
    ON b.id = s.book_id

GROUP BY b.title

HAVING SUM(s.quantity) > (

    SELECT AVG(total)
    FROM (

        SELECT
            SUM(s2.quantity) AS total

        FROM books AS b2

        INNER JOIN sales AS s2
            ON b2.id = s2.book_id

        GROUP BY b2.id
    ) AS average_sales
);