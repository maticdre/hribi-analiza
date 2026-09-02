import csv
import re

IN_FILE = "../podatki/raw_hribi.csv"
OUT_FILE = "../podatki/hribi.csv"

ocisceni_podatki = []

with open(IN_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for vrstica in reader:
        nova_vrstica = vrstica.copy()
        
        # Razbijemo koordinate in zamenjamo vejico s piko
        sirina_dolzina = nova_vrstica.pop("sirina_dolzina", "")
        koordinate = re.findall(r"([\d,.]+)", sirina_dolzina)
        nova_vrstica["sirina"] = koordinate[0].replace(",", ".") if len(koordinate) > 0 else ""
        nova_vrstica["dolzina"] = koordinate[1].replace(",", ".") if len(koordinate) > 1 else ""

        # Ločimo odstotek od mesta na lestvici priljubljenosti
        priljubljenost = nova_vrstica.pop("priljubljenost", "")
        odstotki = re.search(r"(\d+)%", priljubljenost)
        mesto = re.search(r"(\d+)\.", priljubljenost)
        nova_vrstica["priljubljenost_pct"] = odstotki.group(1) if odstotki else ""
        nova_vrstica["mesto"] = mesto.group(1) if mesto else ""

        # Odstranimo odvečne presledke med vrstami obiskanih točk
        vrsta = nova_vrstica.get("vrsta", "")
        nova_vrstica["vrsta"] = ",".join(v.strip() for v in vrsta.split(",") if v.strip())

        # Povezave pri analizi ne potrebujemo več
        nova_vrstica.pop("povezava", None)

        ocisceni_podatki.append(nova_vrstica)

if ocisceni_podatki:
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ocisceni_podatki[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(ocisceni_podatki)

print("Podatki o hribih so očiščeni.")