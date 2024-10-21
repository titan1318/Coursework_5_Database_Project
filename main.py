from db_module.db_manager import DbManager
from config import config

def main():
    # Загружаем параметры подключения из конфигурации
    params = config()

    # Автоматически создаём базу данных, если её нет
    DbManager.create_database(**params)

    # Подключаемся к базе данных
    db = DbManager(**params)

    # Создаём таблицы
    db.create_tables()

    # Здесь можно добавить дальнейшую логику работы с базой
    print("База данных и таблицы успешно настроены.")

    # Закрываем соединение
    db.close()

if __name__ == "__main__":
    main()
