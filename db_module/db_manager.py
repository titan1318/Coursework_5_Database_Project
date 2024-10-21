import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DbManager:
    def __init__(self, dbname, user, password, host, port):
        """Подключение к уже существующей базе данных."""
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    @staticmethod
    def create_database(dbname, user, password, host, port):
        """Создаёт базу данных, если она не существует."""
        try:
            # Подключаемся к базе 'postgres' для создания новой базы данных.
            conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                # Проверяем, существует ли база данных.
                cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
                exists = cur.fetchone()

                if not exists:
                    cur.execute(f'CREATE DATABASE "{dbname}";')
                    print(f"База данных '{dbname}' успешно создана.")
                else:
                    print(f"База данных '{dbname}' уже существует.")
            conn.close()
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")

    def create_tables(self):
        """Создаёт таблицы 'companies' и 'vacancies', если они не существуют."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                    url TEXT NOT NULL
                );
            """)
            self.conn.commit()

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.conn:
            self.conn.close()
