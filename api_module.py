import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_vacancies(self, params):
        """Отправляем запрос на API для получения вакансий"""
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


