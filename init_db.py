import sqlite3


def initialize_database():
    connection = sqlite3.connect('calories_data.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS meal_items (
                    id INTEGER PRIMARY KEY,
                    meal_name TEXT,
                    calorie_count REAL
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS consumption_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_id INTEGER,
                    record_date TEXT,
                    FOREIGN KEY (meal_id) REFERENCES meal_items(id)
                )''')
    connection.commit()
    connection.close()
