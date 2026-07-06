import re
import pdfplumber
import pandas as pd
import sys

PDF_FILE = sys.argv[1]
OUTPUT = "operations.xlsx"

text = ""

with pdfplumber.open(PDF_FILE) as pdf:
    for page in pdf.pages:
        text += page.extract_text(x_tolerance=2, y_tolerance=2)
        text += "\n"

lines = text.splitlines()

date_pattern = re.compile(r"^\d{2}\.\d{2}\.\d{4}")
time_pattern = re.compile(r"^\d{2}:\d{2}")

rows = []

current = None
prev_was_footer = False

for line in lines:
    if date_pattern.match(line):
        prev_was_footer = False
        if current:
            rows.append(current)

        chunks = line[22:-5].split("₽")

        current = {
            "Дата операции": line[0:10],# + " " + additional_chunks[:5],
            "Дата списания": line[11:21],# + " " + additional_chunks[6:12],
            "Сумма в валюте операции": chunks[0],
            "Сумма операции в валюте карты": chunks[1],
            "Описание": chunks[2],# + " " + additional_chunks[12:],
            "Карта": line[-5:]
        }
        
        continue

    if current == None:
        continue

    if time_pattern.match(line):
        prev_was_footer = False
        current["Дата операции"] += ' ' + line[:5]
        current["Дата списания"] += ' ' + line[6:12]
        current["Описание"] += ' ' + line[12:]

        continue

    if "АО «ТБанк»" in line:
        prev_was_footer = True
        continue

    if prev_was_footer:
        continue

    if current:
        current["Описание"] += ' ' + line

if current:
    rows.append(current)




df = pd.DataFrame(rows)

df.to_excel(OUTPUT, index=False)

print("Готово:", OUTPUT)
