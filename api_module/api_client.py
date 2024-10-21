import requests

class APIClient:
    def __init__(self, base_url='https://api.hh.ru/vacancies'):
        self.base_url = base_url

    def get_vacancies(self, params=None):
        """Получает данные о вакансиях с API hh.ru."""
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json().get('items', [])

# Пример использования:
api_client = APIClient()
vacancies = api_client.get_vacancies({'per_page': 10, 'page': 0})
