import psycopg2


            self.conn.commit()


    def get_companies_and_vacancies_count(self):
            """)

    def get_all_vacancies(self):
            """)

    def get_avg_salary(self):
            """)

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
            """, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword):
