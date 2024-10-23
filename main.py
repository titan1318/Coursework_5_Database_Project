import sys
import psycopg2
from db_module.db_manager import DbManager
from config import config
from api_module.api_client import APIClient
from requests.exceptions import RequestException, Timeout

def main():
    try:
        params = config()
        DbManager.create_database(**params)
        db = DbManager(**params)
        db.create_tables()
        api_client = APIClient(base_url="https://api.hh.ru/vacancies")

        company_ids = [1740, 1455, 3529, 39399, 4783, 78638, 1299, 10606, 8454, 10218]

        for company_id in company_ids:
            print(f"Запрашиваем вакансии для компании с ID: {company_id}")
            try:
                vacancies = api_client.get_vacancies({"employer_id": company_id})
                db.save_vacancies_to_db(vacancies)
                print(f"Вакансии для компании {company_id} успешно сохранены.")
            except RequestException as e:
                print(f"Ошибка при запросе вакансий для компании {company_id}: {e}")
                continue

        print("\nВсе данные успешно загружены и сохранены в базе данных.\n")

        print("Список компаний и количество вакансий:")
        companies = db.get_companies_and_vacancies_count()
        for company in companies:
            print(f"Компания: {company[0]}, Вакансий: {company[1]}")

        print("\nСписок всех вакансий:")
        vacancies = db.get_all_vacancies()
        for vacancy in vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: от {vacancy[2]} до {vacancy[3]}, Ссылка: {vacancy[4]}")

        avg_salary = db.get_avg_salary()
        print(f"\nСредняя зарплата: {avg_salary:.2f}")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        sys.exit(1)

    except (RequestException, Timeout) as e:
        print(f"Ошибка при работе с API: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)

    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()
