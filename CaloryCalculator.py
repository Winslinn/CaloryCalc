from bs4 import BeautifulSoup
from pyfiglet import Figlet
import os
import requests
import ctypes
import math
import webbrowser

ctypes.windll.kernel32.SetConsoleTitleW("CaloryCalc")

kсal_title_form = ['Calories', 'ккал', 'kcal', 'калорий']

def get_site(url):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    return resp

def print_result(name, fna, description, url):
    gram = input('Вага в граммах: ')
    x = int(gram) / 100
    result = int(fna) * x

    def def_command(result):
        print('Отримана інформація для ручної фільтрації: ' + description + '\nВідкрити посилання на результат: b\n\nРезультат:')
        print(name + ' (' + fna + 'ккал/100г): ' + str(math.floor(result)) + f' ккал.')
        command = input().replace(' ', '')
        if command == 'b':
            try:
                webbrowser.open(url)
                main()
            except:
                return
        elif command[:1] == '+' and command[len(command) - 1:] == '%':
            os.system('cls')
            def_command(result + result * int(command[:-1][1:]) / 100)
        elif command[:1] == '-' and command[len(command) - 1:] == '%':
            os.system('cls')
            def_command(result - result * int(command[:-1][1:]) / 100)
        elif command[:1] == '+' and command[len(command) - 1:] != '%':
            os.system('cls')
            def_command(result + int(command[1:]))
        elif command[:1] == '-' and command[len(command) - 1:] != '%':
            os.system('cls')
            def_command(result - int(command[1:]))

    def_command(result)

def not_found(name):
    print(name)
    input()
    main()

def find_kkal(fna, name, url):
    description = fna
    for title in kсal_title_form:
        calories_position = fna.rfind(title)
        if calories_position > 0:
            for x in kсal_title_form:
                if calories_position <= 0:
                    calories_position = fna.find(x)

            count_character = len(fna)
            fna = fna[0:-(count_character - calories_position)]

            for x in range(0, len(fna)):
                try:
                    calories = int(fna[x:])
                    if calories < 0:
                        calories = -calories
                    print_result(name, str(calories), description, url)
                except:
                    pass

def main():
    os.system('cls')
    name = input('Назва продукту: ')
    url = 'https://www.google.com/search?client=firefox-b-d&q=' + name.replace(' ', '+') + '+калорийность'
    resp = get_site(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    if resp.status_code == 200:
        try:
            fna = soup.find('div', class_='Z0LcW an_fna')
            fna_table = soup.find('div', class_='webanswers-webanswers_table__webanswers-table')
            if fna != None and fna_table == None:
                try:
                    print_result(name, fna.text[0:-6], fna.text, url)
                except Exception as error:
                    not_found(name + ' не знайдено!' + '\n Error: ' + error)
            elif fna == None and fna_table == None:
                characters = soup.find('span', class_='hgKElc').text
                find_kkal(characters, name, url)
            elif fna_table != None:
                characters = fna_table.find('table').text.lower()
                find_kkal(characters, name, url)
        except:
            input()
    else:
        print('Status code:' + resp.status_code + '. Сайт не доступний.')
        input()
    main()

if __name__ == "__main__":
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('Calory Calculator v1'))
    input('Для продовження натисніть на Enter...')
    main()