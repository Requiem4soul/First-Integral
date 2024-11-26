import pymysql

# Конфигурация подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Akila',
    'charset': 'utf8mb4'
}

# Данные голосования
vote_id = 881  # ID голосования
votes_data = {
    'в_пользу_игрока': ["azerty.qosmos", "xalo0099", "tomsktoluene", "ja_homak" ],  # Список Discord-ников, проголосовавших "за"
    'против_игрока': ["pg_9720", "requiem4soul", "fanigive", "cellingo", "tuman207", "soda4e6", "stoloshkaw", "fortengamer", "bobrpupsik", "yzbe4k", "larisael"],   # Список Discord-ников, проголосовавших "против"
}

# Подключаемся к базе данных
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    for vote_type, users in votes_data.items():
        for username in users:
            # Получаем ID пользователя из таблицы users
            cursor.execute("SELECT id FROM users WHERE discord_name = %s", (username,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                
                # Добавляем запись в таблицу vote_details
                cursor.execute(
                    "INSERT INTO vote_details (vote_id, user_id, vote_type) VALUES (%s, %s, %s)",
                    (vote_id, user_id, vote_type)
                )
            else:
                # Сообщение, если пользователь не найден
                print(f"[Ошибка] Пользователь с Discord-ником '{username}' не найден в таблице users. Пропускаем.")

    # Подтверждаем изменения
    connection.commit()

except pymysql.MySQLError as e:
    print(f"[Ошибка] Произошла ошибка при работе с базой данных: {e}")

finally:
    # Закрываем соединение
    if cursor:
        cursor.close()
    if connection:
        connection.close()
