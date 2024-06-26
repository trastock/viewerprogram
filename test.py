from tabulate import tabulate

header = ["header1", "header2", "header3"]

table = [['one','two','three'],['four','five','six'],['seven','eight','nine']]

print(tabulate(table, tablefmt='html', headers=header))
