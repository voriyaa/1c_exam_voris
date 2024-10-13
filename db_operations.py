import sqlite3


def add_meal(meal_name, calorie_count):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM meal_items')
    current_count = cursor.fetchone()[0]
    new_id = current_count + 1
    cursor.execute('''INSERT INTO meal_items (id, meal_name, calorie_count) VALUES (?, ?, ?)''', (new_id, meal_name, calorie_count))
    connection.commit()
    connection.close()


def get_meals(search_query=None):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    if search_query:
        cursor.execute("SELECT id, meal_name, calorie_count FROM meal_items WHERE LOWER(meal_name) LIKE ?", (f"%{search_query}%",))
    else:
        cursor.execute('SELECT id, meal_name, calorie_count FROM meal_items')
    meals = cursor.fetchall()
    connection.close()
    return meals


def update_meal(meal_id, updated_name, updated_calories):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE meal_items SET meal_name = ?, calorie_count = ? WHERE id = ?''', (updated_name, updated_calories, meal_id))
    connection.commit()
    connection.close()


def delete_meal(meal_id):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('''DELETE FROM meal_items WHERE id = ?''', (meal_id,))
    connection.commit()
    cursor.execute('''UPDATE meal_items SET id = id - 1 WHERE id > ?''', (meal_id,))
    connection.commit()
    connection.close()


def record_consumption(meal_id, record_date):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO consumption_records (meal_id, record_date) VALUES (?, ?)''', (meal_id, record_date))
    connection.commit()
    connection.close()


def fetch_consumed_data(start_date, end_date):
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT record_date, SUM(meal_items.calorie_count) FROM consumption_records
                     JOIN meal_items ON consumption_records.meal_id = meal_items.id
                     WHERE record_date BETWEEN ? AND ?
                     GROUP BY record_date ORDER BY record_date''', (start_date.isoformat(), end_date.isoformat()))
    data = cursor.fetchall()
    connection.close()
    return data
