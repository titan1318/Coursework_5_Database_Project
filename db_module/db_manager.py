import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DbManager:
    def __init__(self, dbname, user, password, host, port):
        """Подключение к существующей базе данных."""
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    @staticmethod
    def create_database(dbname, user, password, host, port):
        """Создаёт базу данных, если она не существует."""
        try:
            conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
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

    def save_company(self, company_id, company_name):
        """Сохраняет компанию в базу данных."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO companies (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (company_id, company_name))
            self.conn.commit()

    def save_vacancy(self, vacancy_id, title, salary_min, salary_max, company_id, url):
        """Сохраняет вакансию в базу данных."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO vacancies (id, title, salary_min, salary_max, company_id, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (vacancy_id, title, salary_min, salary_max, company_id, url))
            self.conn.commit()

    def save_vacancies_to_db(self, vacancies):
        """Сохраняет список вакансий в базу данных."""
        for vacancy in vacancies:
            employer = vacancy.get('employer', {})
            employer_id = employer.get('id')
            employer_name = employer.get('name')

            # Сохраняем компанию
            self.save_company(employer_id, employer_name)

            # Извлекаем данные о вакансии
            vacancy_id = vacancy.get('id')
            title = vacancy.get('name')
            salary = vacancy.get('salary')

            salary_min = salary.get('from') if salary else None
            salary_max = salary.get('to') if salary else None
            url = vacancy.get('alternate_url')

            # Сохраняем вакансию
            self.save_vacancy(vacancy_id, title, salary_min, salary_max, employer_id, url)

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()
