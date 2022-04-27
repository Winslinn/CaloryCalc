from bs4 import BeautifulSoup
from ui import *
import os
import requests
import ctypes
import asyncio
import math
import webbrowser

ctypes.windll.kernel32.SetConsoleTitleW("CaloryCalc")

kсal_title_form = ['Calories', 'ккал', 'kcal', 'калорий']

def get_site(url):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    return resp

def find_kkal(fna, name, url):
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
                    return name, str(calories), url
                except:
                    pass

def main(name):
    url = 'https://www.google.com/search?client=firefox-b-d&q=' + name.replace(' ', '+') + '+калорийность'
    resp = get_site(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    if resp.status_code == 200:
        try:
            fna = soup.find('div', class_='Z0LcW an_fna')
            fna_table = soup.find('div', class_='webanswers-webanswers_table__webanswers-table')
            if fna != None and fna_table == None:
                try:
                    return name, fna.text[:-6], url
                except:
                    pass
            elif fna == None and fna_table == None:
                characters = soup.find('span', class_='hgKElc').text
                return find_kkal(characters, name, url)
            elif fna_table != None:
                characters = fna_table.find('table').text.lower()
                return find_kkal(characters, name, url)
        except:
            return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow().setupUi(MainWindow)
    kcal100 = None
    url = None

    def kcal_calculate(kcal):
        try:
            if kcal == '':
                kcal = 0
            ui.label_3.setText('Калорії: ' + str(math.floor(int(kcal) * (int(kcal100) / 100))))
            ui.label_2.setText(str(kcal100) + 'ккал/100грам')
        except Exception as error:
            print(error)

    def open_result_in_brouser():
        webbrowser.open(url)

    def product_name_changed():
        try:
            global kcal100, url
            ui.lineEdit.clearFocus()
            text = ui.lineEdit.text()
            name, kcal100, url = main(text)
            ui.label_2.setText(str(kcal100) + 'ккал/100грам')
        except:
            return

    ui.lineEdit.editingFinished.connect(product_name_changed)
    ui.lineEdit_2.textChanged.connect(lambda: kcal_calculate(ui.lineEdit_2.text()))
    ui.pushButton.clicked.connect(open_result_in_brouser)

    MainWindow.show()
    sys.exit(app.exec_())