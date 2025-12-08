import sqlite3
import os

# Caminho do seu banco Gold
db_path = os.path.expanduser("~/projeto_fraude__bdd2/data_lakehouse/gold/fraud_analysis.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Executando a query
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas encontradas no SQLite:")
for tabela in tabelas:
    print(f"- {tabela[0]}")

conn.close()