-- 3. Обновил должность на более высокую
UPDATE Employees
SET Position='Senior Beckend Developer'
WHERE id=1;

-- 4. Добавил новое поле с датой
ALTER TABLE Employees
ADD COLUMN HireDate DATE;

-- 5. Добавление даты для всех сотрудников
UPDATE Employees
SET HireDate =
CASE id
    WHEN 1 THEN '2023-03-15'::DATE
    WHEN 2 THEN '2022-08-10'::DATE
    WHEN 3 THEN '2024-01-20'::DATE
    WHEN 4 THEN '2021-11-05'::DATE
    WHEN 5 THEN '2020-06-18'::DATE
    WHEN 6 THEN '2023-09-25'::DATE
    WHEN 7 THEN '2019-04-12'::DATE
    WHEN 8 THEN '2022-12-01'::DATE
    WHEN 9 THEN '2020-02-28'::DATE
    WHEN 10 THEN '2024-05-10'::DATE
END;

SELECT * FROM Employees;