import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def fetch_currency_rates(start_date):
    url = "https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=" + str(start_date).replace('-','.')[:10]
    currency_data = []
    # Формируем URL с датой
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='data')

    # Проверяем, что таблица найдена
    if table:
        for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
            cols = row.find_all('td')
            if len(cols) >= 3:
                currency = {
                    'code': cols[0].text.strip(),
                    'name': cols[3].text.strip(),
                    'value': cols[4].text.strip().replace(',', '.')  # Заменяем запятую на точку
                }
            currency_data.append(currency)


    return currency_data

def date_input():
    date_to_input = input("Введите дату(день(число).месяц(число).год): ")
    d = datetime.now().strftime('%d.%m.%Y')
    d = datetime.strptime(d, '%d.%m.%Y')
    date_true = datetime.strptime(date_to_input, '%d.%m.%Y')
    dd = date_true.strftime('%d.%m.%Y')
    if d > date_true:
        return date_to_input
    else:
        print('Неверная дата')
        date_input()

def name_input():
    name_to_input = str(input("Введите название Валюты: "))
    return name_to_input

date_str = date_input()

arr_of_cur_rates= []
val_name = name_input()

val_arr = []
date_arr = [i for i in range(0,30)]

for i in range(30):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    date_obj += timedelta(days=i)
    start_date = datetime.strftime(date_obj, '%d.%m.%Y')
    currency_rates = fetch_currency_rates(start_date)
    arr_of_cur_rates.append(currency_rates)

for cur in arr_of_cur_rates:
    for smth in cur:
        if smth['name'] == val_name:
            val_arr.append(smth['value'])

sorted_arrays = sorted(zip(val_arr, date_arr))
sorted_array1, sorted_array2 = zip(*sorted_arrays)
sorted_array1 = list(sorted_array1)
sorted_array2 = list(sorted_array2)

plt.bar(sorted_array2, sorted_array1)
plt.show()