# Решение задачи №6

**Автор**: Рахимов Ворис

##
Ссылка на видео с основными возможностями приложения - https://disk.yandex.ru/d/Ra_4OZLbu5zPgQ

## Компиляция и запуск

Для запуска приложения выполните следующие шаги:

1. **Установка зависимостей**

   Установите необходимые библиотеки с помощью команды:
   ```bash
   pip install matplotlib
   ```
   Также необходимо убедиться, что библиотека `Tkinter` установлена.

2. **Запуск приложения**

   Выполните следующую команду для запуска приложения:
   ```bash
   python3 main.py
   ```
## Принятые проектные решения

1. **Разделение логики на несколько файлов**:
   Код приложения был разделен на несколько модулей.
   - `init_db.py` -  Инициализация базы данных.
   - `db_operations.py` - Базовые операции с базой данных.
   - `main.py` - Основной интерфейс приложения.

2. **Графический интерфейс**:
   Используется библиотека `Tkinter` для создания удобного и простого интерфейса.
   
4. **Matplotlib для графиков**:
   Для отображения графиков потребления калорий была выбрана библиотека `matplotlib`.

