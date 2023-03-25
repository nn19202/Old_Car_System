import pandas as pd 

pd.read_csv('car.csv').to_excel('car.xlsx', index = False)
pd.read_csv('contact.csv').to_excel('contact.xlsx', index = False)