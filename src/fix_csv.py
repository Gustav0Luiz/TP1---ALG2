# Script para corrigir os bairros faltantes do CSV.
# Os outros erros de formatação foram manualmente corrigidos.

from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).parent.parent
CSV_PATH = PROJECT_ROOT / 'assets' / 'butecos_bh.csv'
district_idx = 3

with open(CSV_PATH, "r", encoding='utf-8') as infile:
	reader = csv.reader(infile)
	header = next(reader)
	
	modified_rows = []
	for row in reader:
		if len(row) > district_idx and "belo horizonte" in row[district_idx].lower():
			row.insert(district_idx, "")
		modified_rows.append(row)

with open(CSV_PATH, mode='w', encoding='utf-8', newline='') as outfile:
	writer = csv.writer(outfile)
	writer.writerow(header)
	writer.writerows(modified_rows)
