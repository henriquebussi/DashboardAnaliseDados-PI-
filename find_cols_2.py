import csv

with open('santa_casa.registros_medicos.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
print("Total columns:", len(header))
print("First 50 columns:")
for i, c in enumerate(header[:50]):
    print(f"{i}: {c}")
