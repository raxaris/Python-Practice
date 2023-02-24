import requests
import pandas as pd
from bs4 import BeautifulSoup
import fake_useragent

user = fake_useragent.UserAgent().random
header = {'user-agent': user}

data = []

def parse_resume(text):
    page = 0
    url = f'https://hh.kz/search/resume?area=40&label=only_with_age&label=only_with_salary&relocation=living_or_relocation&gender=unknown&text={text}&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page={page}'
    while page < 2:
        response = requests.get(url, headers=header)

        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find_all('a', 'serp-item__title'):
            parsingLinks(i.get('href'))

        page += 1

    df = pd.DataFrame(data, columns=["Title", "Specialization", "Salary", "Age", "Sex"])
    df.to_csv("CV.csv", index=False)

def parsingLinks(link):

    url = 'https://hh.kz' + link
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("span", "resume-block__title-text").get_text()
    specialization = soup.find('li', 'resume-block__specialization').get_text()
    salary_block = soup.find('span', 'resume-block__salary').get_text().replace(u'\u2009', '').split()
    salary = int(salary_block[0])
    age = soup.find("span", {"data-qa": "resume-personal-age"}).text.strip()
    age = age[:2]
    sex = soup.find('span', attrs={'data-qa': 'resume-personal-gender'}).get_text()
    if sex == "Male":
        sex = "Мужчина"
    if sex == "Female":
        sex = "Женщина"

    data.append([title, specialization, salary, age, sex])

parse_resume("js")