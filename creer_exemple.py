import csv
from pathlib import Path
from openpyxl import Workbook
root=Path(__file__).resolve().parent
rows=[
["type","civilite","nom","prenom","date","motif","montant","note","email"],
["attestation","M.","RAKOTO","Jean","23/10/2026","Stage informatique","0","0","jean@example.com"],
["convocation","Mme","RASOA","Marie","25/10/2026","Examen","0","0","marie@example.com"],
["recu","M.","ANDRIA","Paul","23/10/2026","Frais de formation","25000","0","paul@example.com"],
["bulletin","Mme","RABE","Sarah","23/10/2026","Trimestre 1","0","16.5","sarah@example.com"],
]
(root/"data").mkdir(exist_ok=True)
with (root/"data"/"exemple.csv").open("w",encoding="utf-8-sig",newline="") as f: csv.writer(f).writerows(rows)
wb=Workbook(); ws=wb.active; ws.title="Documents"
for row in rows: ws.append(row)
wb.save(root/"data"/"exemple.xlsx")
print("Exemples créés.")
