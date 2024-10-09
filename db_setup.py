import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, db_name, user, password):
        self.conn = psycopg2.connect(dbname=db_name, user=user, password=password)
        self.cursor = self.conn.cursor()

    def create_tables(self):
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

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert_company(self, name):
        self.cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id;", (name,))
        return self.cursor.fetchone()[0]

    def insert_vacancy(self, title, salary_min, salary_max, company_id):
        self.cursor.execute("""
        INSERT INTO vacancies (title, salary_min, salary_max, company_id)
        VALUES (%s, %s, %s, %s);
        """, (title, salary_min, salary_max, company_id))
