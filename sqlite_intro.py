import sqlite3

# Подключаемся к базе данных (файл mybase.db)
# Если файла нет, он создастся автоматически
conn = sqlite3.connect('mybase.db')

# Создаём курсор — объект для выполнения запросов
cursor = conn.cursor()

print("База данных создана и подключена!")
# Создаём таблицу users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# Сохраняем изменения
conn.commit()

print("Таблица users создана!")
# Добавляем одного пользователя
cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Анна', 25))

# Добавляем нескольких пользователей
users = [
    ('Иван', 30),
    ('Мария', 22),
    ('Петр', 35)
]
cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)

conn.commit()
print("Пользователи добавлены!")
# Получаем всех пользователей
cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()

print("\n--- Все пользователи ---")
for user in all_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")
# Получаем пользователей старше 25 лет
cursor.execute('SELECT * FROM users WHERE age > 25')
older_users = cursor.fetchall()

print("\n--- Пользователи старше 25 ---")
for user in older_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")
# Увеличиваем возраст всех пользователей на 1 год
cursor.execute('UPDATE users SET age = age + 1')
conn.commit()

# Проверяем результат
cursor.execute('SELECT * FROM users')
updated_users = cursor.fetchall()

print("\n--- После увеличения возраста ---")
for user in updated_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")
# Удаляем пользователя с id = 2
cursor.execute('DELETE FROM users WHERE id = ?', (2,))
conn.commit()

# Проверяем результат
cursor.execute('SELECT * FROM users')
remaining_users = cursor.fetchall()

print("\n--- После удаления id=2 ---")
for user in remaining_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")
# Закрываем соединение
conn.close()
print("\nСоединение закрыто.")





print("ЗАДАНИЯ 10-17: Работа с таблицей products")

# Открываем новое соединение
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

# Задание 10: Создаём таблицу products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()
print("Таблица products создана!")

# Задание 11: Добавляем товары
products_data = [
    ('Яблоки', 50, 100),
    ('Бананы', 80, 50),
    ('Молоко', 70, 30),
    ('Хлеб', 40, 0),
    ('Сыр', 150, 20)
]
cursor.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', products_data)
conn.commit()
print("Товары добавлены!")

# Задание 12: Выводим все товары
cursor.execute('SELECT * FROM products')
all_products = cursor.fetchall()
print("\n--- Все товары ---")
for product in all_products:
    print(f"{product[0]}. {product[1]} - {product[2]} руб, в наличии: {product[3]}")

# Задание 13: Находим товары с ценой меньше 100 рублей
cursor.execute('SELECT name FROM products WHERE price < 100')
cheap_products = cursor.fetchall()
print("\n--- Товары дешевле 100 рублей ---")
for product in cheap_products:
    print(product[0])

# Задание 14: Находим товары, которых нет в наличии
cursor.execute('SELECT name FROM products WHERE quantity = 0')
out_of_stock = cursor.fetchall()
print("\n--- Товары, которых нет в наличии ---")
for product in out_of_stock:
    print(product[0])

# Задание 15: Увеличиваем цену всех товаров на 10 рублей
cursor.execute('UPDATE products SET price = price + 10')
conn.commit()
print("\n--- Цены увеличены на 10 рублей ---")
cursor.execute('SELECT * FROM products')
updated_prices = cursor.fetchall()
for product in updated_prices:
    print(f"{product[1]} - {product[2]} руб")

# Задание 16: Удаляем товары с ценой выше 100 рублей
cursor.execute('DELETE FROM products WHERE price > 100')
conn.commit()
print("\n--- После удаления товаров дороже 100 рублей ---")
cursor.execute('SELECT * FROM products')
after_delete = cursor.fetchall()
for product in after_delete:
    print(f"{product[1]} - {product[2]} руб")

# Задание 17: Добавляем поле category
cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "другое"')
conn.commit()
print("\nПоле category добавлено!")

# Обновляем категории для товаров
cursor.execute('UPDATE products SET category = "фрукты" WHERE name IN ("Яблоки", "Бананы")')
cursor.execute('UPDATE products SET category = "молочные" WHERE name = "Молоко"')
cursor.execute('UPDATE products SET category = "выпечка" WHERE name = "Хлеб"')
conn.commit()

# Проверяем результат
cursor.execute('SELECT name, price, quantity, category FROM products')
with_categories = cursor.fetchall()
print("\n--- Товары с категориями ---")
for product in with_categories:
    print(f"{product[0]} - {product[1]} руб, в наличии: {product[2]}, категория: {product[3]}")

# Закрываем соединение
conn.close()
print("\nСоединение закрыто.")


# ==================== ПРОВЕРКА ЗНАНИЙ ====================
print("ПРОВЕРКА ЗНАНИЙ")

print("""
1. Как подключиться к базе данных SQLite в Python?
   → sqlite3.connect('имя_файла.db')

2. Что делает cursor.execute()?
   → Выполняет SQL-запрос к базе данных

3. Зачем нужен conn.commit()?
   → Сохраняет (фиксирует) изменения в базе данных

4. Что означает ? в запросе INSERT INTO users (name, age) VALUES (?, ?)?
   → Это заполнитель (placeholder), который защищает от SQL-инъекций.
     Вместо него подставляются значения из второго аргумента execute()

5. Как получить все строки из таблицы?
   → cursor.fetchall()

6. Чем отличается fetchone() от fetchall()?
   → fetchone() - возвращает одну строку (следующую)
   → fetchall() - возвращает все оставшиеся строки в виде списка

7. Как обновить данные в таблице?
   → UPDATE таблица SET поле = значение WHERE условие

8. Как удалить данные из таблицы?
   → DELETE FROM таблица WHERE условие
""")