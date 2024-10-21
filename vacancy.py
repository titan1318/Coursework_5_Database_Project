
class Vacancy:
    def __init__(self, vacancy_id, name, salary_min, salary_max, employer_id, url):
        self.vacancy_id = vacancy_id
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.employer_id = employer_id
        self.url = url

    def __repr__(self):
        return f"Vacancy('{self.name}', {self.salary_min}, {self.salary_max}, {self.url})"
