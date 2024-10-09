import psycopg2
from psycopg2 import sql


class DatabaseManager:
    """Class to manage PostgreSQL database operations."""

    def __init__(self, db_name, user, password):
        # Указываем кодировку при подключении
        self.conn = psycopg2.connect(dbname=db_name, user=user, password=password)
        self.conn.set_client_encoding('UTF8')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create tables in the database."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            company_id INTEGER REFERENCES companies(id)
        );
        """)
        self.conn.commit()

    def insert_company(self, name):
        """Insert a new company into the database."""
        self.cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id;", (name,))
        return self.cursor.fetchone()[0]

    def insert_vacancy(self, title, salary_min, salary_max, company_id):
        """Insert a new vacancy into the database."""
        self.cursor.execute("""
        INSERT INTO vacancies (title, salary_min, salary_max, company_id)
        VALUES (%s, %s, %s, %s);
        """, (title, salary_min, salary_max, company_id))

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()


class DBManager:
    """Class for managing database operations related to companies and vacancies."""

    def __init__(self, db_name, user, password):
        self.db_manager = DatabaseManager(db_name, user, password)

    def get_companies_and_vacancies_count(self):
        """Get a list of all companies and their vacancies count."""
        self.db_manager.cursor.execute("""
        SELECT c.name, COUNT(v.id)
        FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id
        GROUP BY c.name;
        """)
        return self.db_manager.cursor.fetchall()

    def get_all_vacancies(self):
        """Get a list of all vacancies with company name, vacancy title, and salary."""
        self.db_manager.cursor.execute("""
        SELECT v.title, c.name, v.salary_min, v.salary_max
        FROM vacancies v JOIN companies c ON v.company_id = c.id;
        """)
        return self.db_manager.cursor.fetchall()

    def get_avg_salary(self):
        """Get the average salary of vacancies."""
        self.db_manager.cursor.execute("""
        SELECT AVG((salary_min + salary_max) / 2) FROM vacancies;
        """)
        return self.db_manager.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Get a list of vacancies with salaries higher than the average."""
        avg_salary = self.get_avg_salary()
        self.db_manager.cursor.execute("""
        SELECT * FROM vacancies WHERE (salary_min + salary_max) / 2 > %s;
        """, (avg_salary,))
        return self.db_manager.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Get a list of vacancies with a specific keyword in the title."""
        self.db_manager.cursor.execute("""
        SELECT * FROM vacancies WHERE title ILIKE %s;
        """, (f'%{keyword}%',))
        return self.db_manager.cursor.fetchall()
