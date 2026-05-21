import pandas as pd
import csv

with open('santa_casa.registros_medicos.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
keywords = ['cidade', 'bairro', 'sexo', 'idade', 'data_nascimento', 'nascimento', 'municipio', 'gender', 'age']
relevant_cols = []
for col in header:
    col_lower = col.lower()
    # Check if any keyword is a standalone word in the column name (split by . _ or space)
    parts = col_lower.replace('.', ' ').replace('_', ' ').split()
    if any(k in parts for k in keywords):
        relevant_cols.append(col)

print("Found relevant columns:")
for c in relevant_cols:
    print(c)
