import re
import pdfplumber
import pandas as pd
import sys

PDF_FILE = sys.argv[1]
OUTPUT = "operations.xlsx"

text = ""

print("Программа начинает работу")

rows = []

with pdfplumber.open(PDF_FILE) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables({
            "vertical_strategy": "explicit",
            "explicit_vertical_lines": [55, 130, 197, 385, 541, 634, 731, 785]
        })

        for table in tables:
            for row in table:
                rows.append({
                    "Дата операции": row[0],
                    "Сумма": row[1],
                    "Описание": row[2].replace('\n', ' '),
                    "Банк, адрес операции": row[3].replace('\n', ' '),
                    "Контрагент": row[4].replace('\n', ' '),
                    "Номер карты отправителя/получателя": row[5].replace('\n', ' '),
                    "Реквизиты операции": row[6].replace('\n', ' ', 2)
                })
        

df = pd.DataFrame(rows)

df.to_excel(OUTPUT, index=False)

print("Готово:", OUTPUT)

input("Нажмите любую кнопку для выхода")
