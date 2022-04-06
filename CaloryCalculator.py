from bs4 import BeautifulSoup
import os
import requests
import ctypes
import math

ctypes.windll.kernel32.SetConsoleTitleW("CaloryCalc")

kkal_title_form = ['калорий', 'kcal', 'Calories']

def print_result(name, fna):
    gram = input('Вес в граммах: ')
    x = int(gram) / 100
    result = int(fna) * x

    print(name + ' (' + fna + 'ккал/100г): ' + str(math.floor(result)) + ' ккал.')
    input()
    main()

def not_found(name):
    print(name + ' не найдено!')
    input()
    main()

def find_kkal(fna, name):
    calories_position = fna.find('ккал')

    for x in kkal_title_form:
        if calories_position <= 0:
            calories_position = fna.find(x)

    count_character = len(fna)
    fna = fna[0:-(count_character - calories_position)]

    for x in range(0, len(fna)):
        try:
            calories = int(fna[x:])
            if calories < 0:
                calories = -calories
            print_result(name, str(calories))
        except:
            pass

    not_found(name)

def main():
    os.system('cls')
    name = input('Название продукта: ')
    url = 'https://www.google.com/search?client=firefox-b-d&q=' + name + '+калорийность'
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        fna = soup.find('div', class_='Z0LcW an_fna')
        fna_table = soup.find('div', class_='webanswers-webanswers_table__webanswers-table')
        if fna != None and fna_table == None:
            try:
                print_result(name, fna.text[0:-6])
            except Exception as error:
                not_found(name + '\n Error: ' + error)
        elif fna == None and fna_table == None:
            characters = soup.find('span', class_='hgKElc').text.lower()
            find_kkal(characters, name)
        elif fna_table != None:
            characters = fna_table.find('table')
            find_kkal(characters.text.lower(), name)

    else:
        print('Status code:' + resp.status_code + '. Сайт не доступен.')
        input()
    main()

if __name__ == "__main__":
    main()
