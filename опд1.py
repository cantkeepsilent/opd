from bs4 import BeautifulSoup
import requests

url = 'https://omgtu.ru/general_information/the-structure/the-department-of-university.php'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    departments = soup.find('div', id = 'pagecontent')
    departments2 = departments.find_all('a')
    departments_list = [departments.text for departments in departments2]
    print(departments_list)
    with open('omtsu_departments.txt', 'a') as file:
        for department in departments_list:
            file.write(department + '\n')