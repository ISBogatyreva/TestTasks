import calendar
import requests
import xlrd
from requests_html import HTMLSession

url = "https://bashesk.ru/corporate/tariffs/unregulated/"
search_string = "г) объем фактического пикового потребления гарантирующего поставщика на оптовом рынке, МВт"
params = ("filter_date_from", "filter_date_to")
start_year = 2019
start_month_idx = 6
month_period = 12

# Корректные значение для заданных параметров (извлечены вручную)
correct_values = [1422.71, 1491.433, 1693.642, 1792.235, 2054.841, 2146.946,
                  2066.84, 2045.08, 1873.812, 1638.088, 1397.15, 1328.968]

values = []
session = HTMLSession()
for month in range(month_period):
    month_idx = (start_month_idx + month) % 12 + 1
    year = start_year + ((start_month_idx + month) // 12)

    # Первый и последний день месяца
    date_from = "1." + str(month_idx) + "." + str(year)
    date_to = str(calendar.monthrange(year, month_idx)[1]) + "." + str(month_idx) + "." + str(year)
    print("Month:", str(month_idx) + "." + str(year))

    response = session.post(url, params={params[0]: date_from, params[1]: date_to})
    links = response.html.absolute_links
    # Поиск нужного файла
    for link in links:
        if link.find("ПУНЦЭМ_до 670кВт") != -1:
            download_url = link
            break
    else:
        print("Xls file not found")
        continue
    # Скачивание и запись файла
    print("Url for download:", download_url)
    resp = requests.get(download_url)
    if resp.status_code != 200:
        print("Unsuccessful get-attempt, status code:", resp.status_code)
        continue
    excel_name = str(date_from) + ".xls"
    output = open(excel_name, "wb")
    output.write(resp.content)
    output.close()

    # Поиск нужной строки
    excel_file = xlrd.open_workbook(excel_name)
    sheet = excel_file.sheet_by_index(0)
    for rx in range(sheet.nrows):
        if sheet.row(rx)[0].value.strip() == search_string:
            row_idx = rx
            break
    else:
        print("Xls search string not found")
        continue
    
    for i in range(sheet.ncols):
        val = sheet.row(row_idx)[i].value
        if type(val) is float:
            print("Value:", val)
            values.append(val)
            break
    else:
        print("Value not found")
    print()

print("All values:", values)
assert values == correct_values
