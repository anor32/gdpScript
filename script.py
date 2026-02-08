import argparse


from reports import Report
from tables import TableCreator

def main():
    parser = argparse.ArgumentParser(description='d')
    parser.add_argument('--files',nargs='+',required=True,help='требует указать путь к файлу отчета в формате csv')
    parser.add_argument('--report',required=True,help='Название для отчета')
    args = parser.parse_args()
    report = Report(name=args.report)
    report.read_files(args.files)
    report.create_report_gdp()
    report.sort_report(1,reverse=True)
    table = TableCreator()
    table.create_table(headers=report.headers,data=report.rows)
    table.print_table(name=report.name)


if __name__ == '__main__':
    main()