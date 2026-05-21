import pandas as pd
import numpy as np
from datetime import datetime
import json

# 1. Load data
print("Carregando os dados...")
columns_to_load = ["cidade", "bairro", "sexo", "dataNascimento"]
df = pd.read_csv("santa_casa.registros_medicos.csv", usecols=columns_to_load, dtype=str)

# Initial validation
print("\n--- Validação Inicial ---")
print(f"Total de registros originais: {len(df)}")
print("Valores nulos originais por coluna:")
print(df.isnull().sum())

# 2. Padronizar colunas (lowercase, snake_case)
df.columns = [col.lower().replace("nascimento", "_nascimento") for col in df.columns]

# 3. Clean strings, missing values
for col in ["cidade", "bairro", "sexo"]:
    df[col] = df[col].astype(str).str.strip().str.upper()
    df[col] = df[col].replace(["NAN", "NONE", "NULL", ""], np.nan)

df["cidade"] = df["cidade"].fillna("NÃO INFORMADA")
df["bairro"] = df["bairro"].fillna("NÃO INFORMADO")
df["sexo"] = df["sexo"].fillna("NÃO INFORMADO")


def clean_sex(x):
    if pd.isna(x):
        return "NÃO INFORMADO"
    if x in ["M", "MASCULINO", "MASC"]:
        return "MASCULINO"
    if x in ["F", "FEMININO", "FEM"]:
        return "FEMININO"
    return "OUTRO/NÃO INFORMADO"


df["sexo"] = df["sexo"].apply(clean_sex)

# 4. Handle Age
df["data_nascimento"] = df["data_nascimento"].astype(str).str.strip()
df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce")
df["data_nascimento"] = df["data_nascimento"].dt.tz_localize(None)  # Fix timezone issue

current_date = pd.to_datetime("2026-05-05")
df["idade"] = np.floor((current_date - df["data_nascimento"]).dt.days / 365.25)


# 5. Create Age Bracket
def get_age_bracket(age):
    if pd.isna(age):
        return "NÃO INFORMADO"
    if age <= 12:
        return "0-12"
    elif age <= 17:
        return "13-17"
    elif age <= 35:
        return "18-35"
    elif age <= 59:
        return "36-59"
    else:
        return "60+"


df["faixa_etaria"] = df["idade"].apply(get_age_bracket)

print("\n--- Validação Após Tratamento ---")
print(f"Total de registros após tratamento: {len(df)}")
print("Valores nulos após tratamento:")
print(df.isnull().sum())

# 6. Agrupamentos
print("\n--- Tabelas Finais ---")
print("\n1. Atendimentos por Cidade (Top 10)")
city_counts = df["cidade"].value_counts().head(10).reset_index()
city_counts.columns = ["cidade", "total_atendimentos"]
print(city_counts.to_string(index=False))

print("\n2. Atendimentos por Bairro (Top 10)")
bairro_counts = df["bairro"].value_counts().head(10).reset_index()
bairro_counts.columns = ["bairro", "total_atendimentos"]
print(bairro_counts.to_string(index=False))

print("\n3. Distribuição por Sexo")
sexo_counts = df["sexo"].value_counts().reset_index()
sexo_counts.columns = ["sexo", "total_atendimentos"]
print(sexo_counts.to_string(index=False))

print("\n4. Distribuição por Faixa Etária")
faixa_counts = df["faixa_etaria"].value_counts().reset_index()
faixa_counts.columns = ["faixa_etaria", "total_atendimentos"]
print(faixa_counts.to_string(index=False))

# Export for dashboard
df["ano_nascimento"] = df["data_nascimento"].dt.year
export_cols = ["cidade", "bairro", "sexo", "idade", "ano_nascimento", "faixa_etaria"]
df[export_cols].to_json("pacientes_data.json", orient="records", force_ascii=False)
print("Dados exportados para pacientes_data.json")
