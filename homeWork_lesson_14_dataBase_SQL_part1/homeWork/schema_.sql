-- 1. Создание таблицы
CREATE TABLE Employees (
  id SERIAL PRIMARY KEY,
  Name TEXT,
  Position TEXT,
  Departament TEXT,
  Salary DECIMAL(10,2)
);

-- 2. Добавил в таблицу записи
INSERT INTO Employees (Name, Position, Departament, Salary) VALUES
('Дмитрий Иванов', 'Backend Developer', 'Разработка', 4500),
('Анна Петрова', 'Frontend Developer', 'Разработка', 4200),
('Максим Сидоров', 'QA Engineer', 'Тестирование', 3500),
('Елена Кузнецова', 'HR Manager', 'HR', 3000),
('Алексей Смирнов', 'DevOps Engineer', 'Инфраструктура', 5200),
('Мария Волкова', 'UI/UX Designer', 'Дизайн', 4000),
('Олег Морозов', 'Project Manager', 'Менеджмент', 6000),
('Виктория Орлова', 'Data Analyst', 'Аналитика', 4800),
('Игорь Павлов', 'Database Administrator', 'Базы данных', 5500),
('София Белова', 'Marketing Specialist', 'Маркетинг', 3200);
