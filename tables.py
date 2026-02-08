from tabulate import tabulate

class TableCreator:
    table = None
    def create_table(self,data,headers):
        table = tabulate(data, headers=headers, tablefmt='orgtbl')
        self.table = table
        return table

    def print_table(self,name=None):
        if name:
            print(f"Отчет {name}")
        print(self.table)

