import pymysql
import openpyxl
import re
import os

# Конфигурация подключения к MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Akila',
    'charset': 'utf8mb4'
}

# Путь к файлу Excel
excel_file = 'WhiteList/ТаблицаИгроковWL.xlsx'

# Проверяем, существует ли файл
if not os.path.exists(excel_file):
    print(f"Ошибка: файл {excel_file} не найден.")
    exit()

try:
    # Загружаем данные из Excel
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['Отзывы']
except KeyError:
    print("Ошибка: лист с именем 'Отзывы' не найден в файле Excel.")
    exit()

# Подключаемся к базе данных
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Обработка данных из Excel
for row in sheet.iter_rows(min_row=2):
    excel_id = row[0].value  # ID из столбца A
    from_user = row[1].value  # От кого (столбец B)
    to_user = row[2].value    # На кого (столбец C)
    
    # Проверяем гиперссылку или формулу HYPERLINK в столбце D
    cell_value = row[3].value
    if isinstance(cell_value, str) and cell_value.startswith('=HYPERLINK'):
        # Извлекаем ссылку с помощью регулярного выражения
        match = re.search(r'"(https://[^"]+)"', cell_value)
        discord_link = match.group(1) if match else None
    elif row[3].hyperlink:
        discord_link = row[3].hyperlink.target
    else:
        discord_link = None

    # Проверяем, есть ли ссылка
    if not discord_link:
        print(f"Ошибка: ссылка отсутствует для строки с 'На кого' = {to_user}")
        continue

    # Получаем ID игрока по Discord-нику (to_user) из таблицы users
    cursor.execute("SELECT id FROM users WHERE discord_name = %s", (to_user,))
    result = cursor.fetchone()

    if result:
        voted_user_id = result[0]
    else:
        print(f"Ошибка: игрок с Discord-ником {to_user} не найден!")
        continue

    # Вставляем запись в таблицу votes с учётом excel_id
    cursor.execute(
        "INSERT INTO votes (voted_user_id, review_url, excel_id) VALUES (%s, %s, %s)",
        (voted_user_id, discord_link, excel_id)
    )

# Подтверждаем изменения
connection.commit()

# Закрываем соединение
cursor.close()
connection.close()
