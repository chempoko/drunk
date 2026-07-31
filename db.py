import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "sobriety.db"


def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            started_at TIMESTAMP,
            last_drink TIMESTAMP,
            total_abstinence_days INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    conn.commit()
    conn.close()


def get_user(user_id):
    """Получить пользователя по ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None


def create_or_update_user(user_id, username, first_name):
    """Создать или обновить пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    user = get_user(user_id)
    
    if not user:
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        """, (user_id, username, first_name))
    else:
        cursor.execute("""
            UPDATE users SET username = ?, first_name = ?
            WHERE user_id = ?
        """, (username, first_name, user_id))
    
    conn.commit()
    conn.close()


def set_abstinence_start(user_id):
    """Зафиксировать начало аскезы"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    # Убедимся что пользователь существует
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if not cursor.fetchone():
        # Если пользователя нет, создадим его
        cursor.execute("""
            INSERT INTO users (user_id, started_at)
            VALUES (?, ?)
        """, (user_id, now))
    else:
        # Если существует, обновим
        cursor.execute("""
            UPDATE users SET started_at = ?, last_drink = NULL
            WHERE user_id = ?
        """, (now, user_id))
    
    cursor.execute("""
        INSERT INTO history (user_id, event) VALUES (?, ?)
    """, (user_id, "started_abstinence"))
    
    conn.commit()
    conn.close()


def record_drinking(user_id):
    """Зафиксировать употребление алкоголя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    cursor.execute("""
        UPDATE users SET last_drink = ?
        WHERE user_id = ?
    """, (now, user_id))
    
    cursor.execute("""
        INSERT INTO history (user_id, event) VALUES (?, ?)
    """, (user_id, "drank"))
    
    conn.commit()
    conn.close()


def is_abstinence_active(user_id):
    """Проверить есть ли активная аскеза (started_at установлен и нет drink после started_at)"""
    user = get_user(user_id)
    
    if not user or not user['started_at']:
        return False
    
    try:
        started = datetime.fromisoformat(user['started_at'])
    except (ValueError, TypeError):
        return False
    
    # Если была последняя пьянка после начала аскезы - аскеза не активна
    if user['last_drink']:
        try:
            last_drink = datetime.fromisoformat(user['last_drink'])
            if last_drink > started:
                return False
        except (ValueError, TypeError):
            pass
    
    return True


def get_days_of_abstinence(user_id):
    """Получить количество дней без алкоголя (если меньше 1 дня - 0)"""
    user = get_user(user_id)
    
    if not user:
        return 0
    
    # Если нет даты начала аскезы
    if not user['started_at']:
        return 0
    
    try:
        started = datetime.fromisoformat(user['started_at'])
    except (ValueError, TypeError):
        return 0
    
    # Если была последняя пьянка после начала аскезы - счетчик обнулен
    if user['last_drink']:
        try:
            last_drink = datetime.fromisoformat(user['last_drink'])
            if last_drink > started:
                return 0
        except (ValueError, TypeError):
            pass
    
    # Считаем полные 24-часовые периоды (меньше 24 часов = 0 дней)
    delta = datetime.now() - started
    days = max(0, int(delta.total_seconds() // 86400))
    return days


def get_user_stats(user_id):
    """Получить статистику пользователя"""
    user = get_user(user_id)
    
    if not user:
        return None
    
    days = get_days_of_abstinence(user_id)
    
    return {
        'days': days,
        'started_at': user['started_at'],
        'last_drink': user['last_drink']
    }


def get_all_active_users():
    """Получить всех пользователей с активной аскезой"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM users 
        WHERE started_at IS NOT NULL
        ORDER BY started_at DESC
    """)
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]


def get_group_stats():
    """Получить статистику группы (всех активных пользователей)"""
    users = get_all_active_users()
    
    stats_list = []
    for user in users:
        user_id = user['user_id']
        
        # Проверяем активна ли аскеза
        if not is_abstinence_active(user_id):
            continue
        
        days = get_days_of_abstinence(user_id)
        first_name = user.get('first_name', f'User {user_id}')
        
        stats_list.append({
            'user_id': user_id,
            'first_name': first_name,
            'days': days,
            'started_at': user['started_at']
        })
    
    # Сортируем по количеству дней (по убыванию)
    stats_list.sort(key=lambda x: x['days'], reverse=True)
    
    return stats_list

