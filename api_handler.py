import requests

class APIHandler:
    BASE_URL = "https://api.hh.ru"

    def get_employers(self, employer_ids):
        employers = []
        for employer_id in employer_ids:
            response = requests.get(f"{self.BASE_URL}/employers/{employer_id}")
            if response.status_code == 200:
                employers.append(response.json())
        return employers

    def get_vacancies(self, employer_id):
        response = requests.get(f"{self.BASE_URL}/vacancies?employer_id={employer_id}")
        return response.json().get('items', [])
