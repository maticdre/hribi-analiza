import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from utils import izlusci

BASE_URL = "https://www.hribi.net/gora/x/1/{}"
OUT_HRIBI = "../podatki/raw_hribi.csv"
OUT_POTI = "../podatki/raw_poti.csv"

hribi = []
poti = []
zaporedne_napake = 0

for gora_id in range(1, 10000):
    url = BASE_URL.format(gora_id)
    try:
        odgovor = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        print(f"Napaka pri povezavi: ID {gora_id}")
        continue

    if odgovor.status_code != 200:
        continue

    odgovor.encoding = "utf-8"
    soup = BeautifulSoup(odgovor.text, "html.parser")
    h1 = soup.find("h1")

    if odgovor.url == "https://www.hribi.net/" or not h1 or "Hribi.net" in h1.text:
        zaporedne_napake += 1
        if zaporedne_napake >= 50:
            print("Preveč zaporednih praznih ID-jev, prekinjam iskanje.")
            break
        continue

    zaporedne_napake = 0
    besedilo = soup.get_text()
    ime_gore = h1.text.strip()

    hribi.append({
        "id": gora_id,
        "ime_gore": ime_gore,
        "drzava": izlusci(r"Država:\s*([^\n\r]+)", besedilo),
        "gorovje": izlusci(r"Gorovje:\s*([^\n\r]+)", besedilo),
        "visina": izlusci(r"Višina:\s*(\d+)\s*m", besedilo, samo_stevilke=True),
        "sirina_dolzina": izlusci(r"Širina/Dolžina:\s*([^\n\r]+)", besedilo),
        "vrsta": izlusci(r"Vrsta:\s*([^\n\r]+)", besedilo),
        "ogledi": izlusci(r"Ogledov:\s*([\d\.]+)", besedilo, samo_stevilke=True),
        "priljubljenost": izlusci(r"Priljubljenost:\s*([^\n\r]+)", besedilo),
        "stevilo_slik": izlusci(r"Število slik:\s*(\d+)", besedilo, samo_stevilke=True),
        "stevilo_poti": izlusci(r"Število poti:\s*(\d+)", besedilo, samo_stevilke=True),
        "stevilo_gps_sledi": izlusci(r"Število GPS sledi:\s*(\d+)", besedilo, samo_stevilke=True),
        "vpisna_knjiga": izlusci(r"Vpisna knjiga:\s*(\d+)", besedilo, samo_stevilke=True),
        "povezava": odgovor.url,
    })

    # Ker tabela vsebuje 3 enake povezave na pot, vzamemo vsako tretjo
    vse_povezave = soup.select("td a[href^='/izlet/']")
    izbrane_poti = vse_povezave[::3]

    for a in izbrane_poti:
        poti.append({
            "gora_id": gora_id, 
            "povezava_poti": f"https://www.hribi.net{a['href']}"
        })

    print(f"ID {gora_id}: {ime_gore} (najdenih poti: {len(izbrane_poti)})")

with open(OUT_HRIBI, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=hribi[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(hribi)

with open(OUT_POTI, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["gora_id", "povezava_poti"], delimiter=";")
    writer.writeheader()
    writer.writerows(poti)