import json
from db_manager import DbManager
from config import config

def load_vacancies_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file).get('items', [])

def save_vacancies_to_db(vacancies, db):
    for vacancy in vacancies:
        employer = vacancy.get('employer', {})
        employer_id = employer.get('id')
        employer_name = employer.get('name')

        db.save_company(employer_id, employer_name)

        vacancy_id = vacancy.get('id')
        title = vacancy.get('name')
        salary = vacancy.get('salary')

        if salary:
            salary_min = salary.get('from')
            salary_max = salary.get('to')
        else:
            salary_min = None
            salary_max = None

        url = vacancy.get('url')
        db.save_vacancy(vacancy_id, title, salary_min, salary_max, employer_id, url)

def main():
    params = config()
    db = DbManager(**params)

    db.create_tables()

    vacancies = load_vacancies_from_json('vacancies (1).json')
    save_vacancies_to_db(vacancies, db)

    companies = db.get_companies_and_vacancies_count()
    for company in companies:
        print(f"Компания: {company[0]}, Вакансий: {company[1]}")

    vacancies = db.get_all_vacancies()
    for vacancy in vacancies:
        print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: от {vacancy[2]} до {vacancy[3]}, Ссылка: {vacancy[4]}")

    avg_salary = db.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary}")

    db.close()

if __name__ == "__main__":
    main()

