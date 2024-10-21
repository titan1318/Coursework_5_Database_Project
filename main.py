import sys
from db_module import DbManager
from config import config
from api_module import APIClient
from requests.exceptions import RequestException, Timeout

def main():
    try:
        # Загружаем параметры подключения
        params = config()

        # Автоматически создаём базу данных
        DbManager.create_database(**params)

        # Подключаемся к базе данных
        db = DbManager(**params)
        db.create_tables()

        # Инициализируем API клиента
        api_client = APIClient()

        # Список ID компаний для загрузки вакансий
        company_ids = [1740, 1455, 3529, 39399, 4783, 78638, 1299, 10606, 8454, 10218]

        # Загружаем и сохраняем вакансии
        for company_id in company_ids:
            try:
                vacancies = api_client.get_vacancies({"employer_id": company_id})
                db.save_vacancies_to_db(vacancies)
                print(f"Вакансии для компании {company_id} успешно сохранены.")
            except RequestException as e:
                print(f"Ошибка при запросе вакансий для компании {company_id}: {e}")
                continue

        print("Все данные успешно загружены и сохранены в базе данных.")

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
