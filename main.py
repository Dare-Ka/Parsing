import requests
from bs4 import BeautifulSoup
import json
from fake_headers import Headers
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
keywords = ['Django', 'Flask']
headers = Headers(browser='firefox', os='win').generate()
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    vacancies = soup.find_all(class_='vacancy-serp-item__layout')
    result = []
    for vacancy in vacancies:
        link = vacancy.find('a')['href']
        company = vacancy.find('a', class_='bloko-link').text
        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}, class_='bloko-text').text
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}, class_='bloko-header-section-2')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Зарплата не указана'
        vacancy_info = {
            'link': link,
            'company': company,
            'city': city,
            'salary': salary
            }
        result.append(vacancy_info)
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

else:
    print('Ошибка при выполнении запроса')