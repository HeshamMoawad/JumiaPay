import pandas ,sqlite3

con = sqlite3.connect('Database.db')
tables = ['WE','Etisalat','Noor','Orange']

print("""
Welcome to Extract DataBase 

Please Choose Vendor you want to get Data From

[1] We
[2] Etisalat
[3] Noor
[4] Orange

""")
choice = int(input("Enter Table you Want to get -> "))



vendor = tables[choice-1]


df = pandas.read_sql_query(f'SELECT * FROM {vendor}',con)

#print(df)
df.to_excel(f"DataBase[{vendor}].xlsx",index=False)
print(f'\nSuccessful Extract as DataBase[{vendor}].xlsx\n')

input("Press any key to Exit .....")




