import pymysql

# Конфигурация подключения к MySQL
db_config = {
    'host': 'localhost',         # Ваш хост (обычно localhost)
    'user': 'root',              # Имя пользователя MySQL
    'password': '',              # Пароль от MySQL
    'database': 'Akila',         # Название базы данных
    'charset': 'utf8mb4'         # Кодировка
}

# Создание таблицы users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, -- Уникальный ID пользователя
    ckey VARCHAR(255) UNIQUE NOT NULL,            -- Уникальный сикей игрока
    discord_name VARCHAR(255) NOT NULL            -- Ник в Discord
);
"""

# Создание таблицы votes с добавлением excel_id
create_votes_table = """
CREATE TABLE IF NOT EXISTS votes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,            -- Уникальный ID голосования
    voted_user_id BIGINT UNSIGNED NOT NULL,                   -- ID игрока, за которого голосуют (FK на users.id)
    review_url TEXT,                                          -- Ссылка на отзыв (опционально)
    excel_id VARCHAR(255) NOT NULL,                          -- ID из таблицы Excel для поиска
    FOREIGN KEY (voted_user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
"""

# Создание таблицы vote_details
create_vote_details_table = """
CREATE TABLE IF NOT EXISTS vote_details (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,           -- Уникальный ID записи
    vote_id BIGINT UNSIGNED NOT NULL,                         -- ID голосования (FK на votes.id)
    user_id BIGINT UNSIGNED NOT NULL,                         -- ID игрока, голосующего (FK на users.id)
    vote_type ENUM('в_пользу_игрока', 'против_игрока') NOT NULL, -- Тип голоса
    FOREIGN KEY (vote_id) REFERENCES votes(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
"""

# Создание таблиц
try:
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        # Создаём таблицу users
        cursor.execute(create_users_table)
        print("Таблица 'users' создана.")
        
        # Создаём таблицу votes
        cursor.execute(create_votes_table)
        print("Таблица 'votes' создана.")
        
        # Создаём таблицу vote_details
        cursor.execute(create_vote_details_table)
        print("Таблица 'vote_details' создана.")
        
    # Подтверждаем изменения
    connection.commit()
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    connection.close()
