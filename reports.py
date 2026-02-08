import csv

from utils import path_normalizer


class Report:

    def __init__(self, name='', headers=None, rows=None):
        self.name = name
        self.headers = headers
        self.rows = rows

    def read_files(self, paths):
        rows = []

        for path in paths:
            path =  path_normalizer(path)
            if not path:
                continue
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    file_data = list(reader)
                    rows.extend(file_data)
            except FileNotFoundError:
                print('Ошибка Неверный путь к файлу или не его не существует',path)
                continue
            except Exception:
                print('Ошибка чтения файла')
                continue
            self.headers = headers
            self.rows = rows

    def sort_report(self, ind_key, reverse=False):
        if not self.rows:
            return 'не созданы строки таблицы'
        rows = sorted(self.rows, key=lambda row: row[ind_key], reverse=reverse)
        self.rows = rows

    def create_report_gdp(self):
        report = {}
        count = {}
        if not self.headers or not  self.rows:
            return 'не созданы строки таблицы или заголовки'
        for i in range(len(self.rows)):
            country = self.rows[i][0]
            gdp = int(self.rows[i][2])
            if country not in report:
                report[country] = gdp
                count[country] = 1
            else:
                report[country] += gdp
                count[country] += 1
        headers = [self.headers[0], self.headers[2]]
        rows = []
        for country in report:
            rows.append((country, round(report[country] / count[country], 2)))

        self.headers = headers
        self.rows = rows
