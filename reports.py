import csv


class Report:
    name = ''

    def __init__(self, name='', headers=None, rows=None):
        self.name = name
        self.headers = headers
        self.rows = rows

    def read_files(self, paths):
        rows = []
        for path in paths:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                file_data = list(reader)
                rows.extend(file_data)

            self.headers = headers
            self.rows = rows

    def sort_report(self, ind_key, reverse=False):

        rows = sorted(self.rows, key=lambda row: row[ind_key], reverse=reverse)
        self.rows = rows

    def create_report_gdp(self):
        report = {}
        count = {}
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
