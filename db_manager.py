import psycopg2

class DbManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def save_company(self, company_id, company_name):
        """Сохранение компании в базу данных"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO companies (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (company_id, company_name))
            self.conn.commit()

    def save_vacancy(self, vacancy_id, title, salary_min, salary_max, company_id, url):
        """Сохранение вакансии в базу данных"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO vacancies (id, title, salary_min, salary_max, company_id, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (vacancy_id, title, salary_min, salary_max, company_id, url))
            self.conn.commit()

    def create_tables(self):
        """Создание таблиц в базе данных"""
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
                    company_id INTEGER REFERENCES companies(id),
                    url TEXT NOT NULL
                );
            """)
            self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получить список всех компаний и количество вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, COUNT(vacancies.id)
                FROM companies
                JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получить список всех вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.title, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Получить среднюю зарплату"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_min + salary_max)/2) AS avg_salary
                FROM vacancies
                WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;
            """)
            return cur.fetchone()[0]

    def close(self):
        if self.conn:
            self.conn.close()
