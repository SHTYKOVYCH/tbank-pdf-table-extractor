import pdfplumber
import pandas as pd
import sys

def extract_tables(pdf_path, pages=None):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        if pages is None:
            pages = range(len(pdf.pages))
        page = pdf.pages[0]
        tables = page.extract_tables({
            "vertical_strategy": "explicit",
            "explicit_vertical_lines": [55, 130, 197, 385, 541, 634, 731, 780]
        })
        for table in tables[0]:
            print(table)

def printX(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()
        # Выводим первые 20 слов с их x0 (левый край слова)
        for w in words:
            print(w["text"], w["x1"])
        print()

printX(sys.argv[1])
extract_tables(sys.argv[1])
