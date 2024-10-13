import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import timedelta
from init_db import initialize_database
from db_operations import *


class MealTrackerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Калькулятор Калорий")
        self.current_date = datetime.date.today()

        ttk.Label(window, text="Название приема пищи:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.mealNameInput = ttk.Entry(window)
        self.mealNameInput.grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(window, text="Калории:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.calorieInput = ttk.Entry(window)
        self.calorieInput.grid(row=1, column=1, padx=10, pady=5)
        self.addMealButton = ttk.Button(window, text="Добавить прием пищи", command=self.add_meal)
        self.addMealButton.grid(row=1, column=2, padx=10, pady=5)

        ttk.Label(window, text="Поиск приема пищи:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.searchInput = ttk.Entry(window)
        self.searchInput.grid(row=2, column=1, padx=10, pady=5)
        self.searchButton = ttk.Button(window, text="Поиск", command=self.search_meals)
        self.searchButton.grid(row=2, column=2, padx=10, pady=5)

        self.mealList = tk.Listbox(window, width=50, font=('Helvetica', 10))
        self.mealList.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.editMealButton = ttk.Button(window, text="Редактировать прием пищи", command=self.edit_meal)
        self.editMealButton.grid(row=4, column=0, padx=10, pady=5)
        self.deleteMealButton = ttk.Button(window, text="Удалить прием пищи", command=self.delete_meal)
        self.deleteMealButton.grid(row=4, column=1, padx=10, pady=5)
        self.recordMealButton = ttk.Button(window, text="Записать потребление", command=self.record_meal)
        self.recordMealButton.grid(row=4, column=2, padx=10, pady=5)

        ttk.Label(window, text="Дата начала (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.startDateInput = ttk.Entry(window)
        self.startDateInput.grid(row=5, column=1, padx=10, pady=5)
        self.setStartTodayButton = ttk.Button(window, text="Сегодня", command=self.set_start_today)
        self.setStartTodayButton.grid(row=5, column=2, padx=10, pady=5)

        ttk.Label(window, text="Дата окончания (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        self.endDateInput = ttk.Entry(window)
        self.endDateInput.grid(row=6, column=1, padx=10, pady=5)
        self.setEndTodayButton = ttk.Button(window, text="Сегодня", command=self.set_end_today)
        self.setEndTodayButton.grid(row=6, column=2, padx=10, pady=5)

        self.showGraphButton = ttk.Button(window, text="Показать график", command=self.display_graph)
        self.showGraphButton.grid(row=7, column=0, columnspan=3, pady=10)

        self.load_meals()

    def add_meal(self):
        meal_name = self.mealNameInput.get()
        try:
            calories = float(self.calorieInput.get())
        except ValueError:
            messagebox.showwarning('Ошибка', 'Пожалуйста, введите числовое значение для калорий.')
            return

        if meal_name:
            add_meal(meal_name, calories)
            self.load_meals()
            messagebox.showinfo('Успех', 'Прием пищи успешно добавлен!')
        else:
            messagebox.showwarning('Ошибка', 'Пожалуйста, введите название приема пищи.')

    def load_meals(self):
        self.mealList.delete(0, tk.END)
        meals = get_meals()
        for meal in meals:
            self.mealList.insert(tk.END, f"{meal[0]}: {meal[1]} - {meal[2]} ккал")

    def search_meals(self):
        search_query = self.searchInput.get().lower()
        self.mealList.delete(0, tk.END)
        meals = get_meals(search_query)
        for meal in meals:
            self.mealList.insert(tk.END, f"{meal[0]}: {meal[1]} - {meal[2]} ккал")

    def record_meal(self):
        selected_index = self.mealList.curselection()
        if selected_index:
            meal_id = int(self.mealList.get(selected_index).split(':')[0])
            record_date = (datetime.date.today() + timedelta(days=0)).isoformat() #timedelta for testing graphics
            record_consumption(meal_id, record_date)
            messagebox.showinfo('Успех', 'Потребление записано!')
        else:
            messagebox.showwarning('Ошибка', 'Пожалуйста, выберите прием пищи.')

    def edit_meal(self):
        selected_index = self.mealList.curselection()
        if selected_index:
            meal_id = int(self.mealList.get(selected_index).split(':')[0])
            updated_name = self.mealNameInput.get()
            try:
                updated_calories = float(self.calorieInput.get())
            except ValueError:
                messagebox.showwarning('Ошибка', 'Пожалуйста, введите числовое значение для калорий.')
                return

            if updated_name:
                update_meal(meal_id, updated_name, updated_calories)
                self.load_meals()
                messagebox.showinfo('Успех', 'Прием пищи успешно обновлен!')
            else:
                messagebox.showwarning('Ошибка', 'Пожалуйста, введите название приема пищи.')
        else:
            messagebox.showwarning('Ошибка', 'Пожалуйста, выберите прием пищи для редактирования.')

    def delete_meal(self):
        selected_index = self.mealList.curselection()
        if selected_index:
            meal_id = int(self.mealList.get(selected_index).split(':')[0])
            delete_meal(meal_id)
            self.load_meals()
            messagebox.showinfo('Успех', 'Прием пищи успешно удален!')
        else:
            messagebox.showwarning('Ошибка', 'Пожалуйста, выберите прием пищи для удаления.')

    def display_graph(self):
        start_date = self.startDateInput.get()
        end_date = self.endDateInput.get()

        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showwarning('Ошибка', 'Пожалуйста, введите даты в формате ГГГГ-ММ-ДД.')
            return

        data = fetch_consumed_data(start_date, end_date)

        if data:
            dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d') for row in data]
            calorie_values = [row[1] for row in data]
            plt.figure(figsize=(16, 9))
            plt.plot(dates, calorie_values, marker='o', markersize=8, linestyle='-')
            plt.xlabel('Дата')
            plt.ylabel('Потребленные калории')
            plt.title('График потребления калорий')
            plt.show()
        else:
            messagebox.showwarning('Ошибка', 'Нет данных для выбранного диапазона дат.')

    def set_start_today(self):
        self.startDateInput.delete(0, tk.END)
        self.startDateInput.insert(0, datetime.date.today().isoformat())

    def set_end_today(self):
        self.endDateInput.delete(0, tk.END)
        self.endDateInput.insert(0, datetime.date.today().isoformat())


if __name__ == '__main__':
    initialize_database()
    root = tk.Tk()
    app = MealTrackerApp(root)
    root.mainloop()
