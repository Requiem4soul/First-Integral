import pymysql
import pandas as pd

# Конфигурация подключения к MySQL
db_config = {
    'host': 'localhost',         # Ваш хост (обычно localhost)
    'user': 'root',              # Имя пользователя MySQL
    'password': '',              # Пароль от MySQL
    'database': 'Akila',         # Название базы данных
    'charset': 'utf8mb4'         # Кодировка
}

# Путь к Excel-файлу
excel_file = "WhiteList/ТаблицаИгроковWL.xlsx"  # Замените на путь к вашему файлу

try:
    # Чтение данных из Excel в DataFrame
    df = pd.read_excel(excel_file, sheet_name="Список")  # Лист с данными

    # Переименовываем столбцы для удобства
    df = df.rename(columns={"C-Key": "ckey", "Discord": "discord_name"})
    
    # Убедимся, что берём только нужные столбцы
    df = df[['ckey', 'discord_name']]

    # Подключение к базе данных
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        # SQL-запрос для вставки данных, игнорируя дубли
        insert_query = """
        INSERT IGNORE INTO users (ckey, discord_name)
        VALUES (%s, %s)
        """

        # Перебор строк и вставка данных в таблицу
        for _, row in df.iterrows():
            cursor.execute(insert_query, (row['ckey'], row['discord_name']))
        
        # Подтверждаем изменения
        connection.commit()
        print("Данные успешно добавлены в таблицу 'users', дубли были проигнорированы.")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if 'connection' in locals():
        connection.close()
