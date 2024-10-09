from api_handler import APIHandler
from db_manager import DBManager


def main():
    db_manager = DBManager('mydb', 'Kobra', '0000')
    db_manager.db_manager.create_tables()

    # Заполнение таблиц
    api_handler = APIHandler()
    employer_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # пример ID
    employers = api_handler.get_employers(employer_ids)

    for employer in employers:
        company_id = db_manager.db_manager.insert_company(employer['name'])
        vacancies = api_handler.get_vacancies(employer['id'])
        for vacancy in vacancies:
            db_manager.db_manager.insert_vacancy(vacancy['name'], vacancy.get('salary_min'), vacancy.get('salary_max'), company_id)

    # Взаимодействие с пользователем
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword('python'))

if __name__ == "__main__":
    main()

