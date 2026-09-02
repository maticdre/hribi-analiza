import csv
import re
import time
import requests
from bs4 import BeautifulSoup

IN_FILE = "../podatki/raw_poti.csv"
OUT_FILE = "../podatki/processed_poti.csv"

def izlusci(vzorec, besedilo, samo_stevilke=False):
    ujemanje = re.search(vzorec, besedilo)
    if ujemanje:
        vrednost = ujemanje.group(1).strip()
        if samo_stevilke:
            return re.sub(r"\D", "", vrednost)
        return vrednost
    return ""

zbrane_poti = []

with open(IN_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for vrstica in reader:
        url = vrstica.get("povezava_poti")
        if not url:
            continue
        
        pot_id = url.split("/")[-1]

        try:
            odgovor = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            print(f"Napaka pri povezavi na pot {pot_id}")
            continue

        if odgovor.status_code != 200:
            continue

        odgovor.encoding = "utf-8"
        soup = BeautifulSoup(odgovor.text, "html.parser")
        besedilo = soup.get_text()

        zbrane_poti.append({
            "gora_id": vrstica["gora_id"],
            "pot_id": pot_id,
            "izhodisce": izlusci(r"Izhodišče:\s*([^\n\r]+)", besedilo),
            "sirina_dolzina": izlusci(r"Širina/Dolžina:\s*([^\n\r]+)", besedilo),
            "cilj": izlusci(r"Cilj:\s*([^\n\r]+)", besedilo),
            "ime_poti": izlusci(r"Ime poti:\s*([^\n\r]+)", besedilo),
            "cas_hoje": izlusci(r"Čas hoje:\s*([^\n\r]+)", besedilo),
            "dolzina_km": izlusci(r"Dolžina poti:\s*([^\n\r]+)", besedilo),
            "zahtevnost": izlusci(r"Zahtevnost:\s*([^\n\r]+)", besedilo),
            "ferata": izlusci(r"Ferata:\s*([^V\n\r]+)", besedilo),
            "visinska_razlika_m": izlusci(r"Višinska razlika:\s*(\d+)\s*m", besedilo, samo_stevilke=True),
            "visinska_razlika_po_poti_m": izlusci(r"Višinska razlika po poti:\s*(\d+)\s*m", besedilo, samo_stevilke=True),
            "zemljevid": izlusci(r"Zemljevid:\s*([^\n\r]+)", besedilo),
            "oprema_poletje": izlusci(r"Priporočena oprema \(poletje\):\s*([^\n\r]+)", besedilo),
            "oprema_zima": izlusci(r"Priporočena oprema \(zima\):\s*([^\n\r]+)", besedilo),
            "ogledi": izlusci(r"Ogledov:\s*([\d\.]+)", besedilo, samo_stevilke=True),
            "stevilo_slik": izlusci(r"Število slik:\s*(\d+)", besedilo, samo_stevilke=True),
            "stevilo_komentarjev": izlusci(r"Število komentarjev:\s*(\d+)", besedilo, samo_stevilke=True),
            "povezava": url
        })

        print(f"Zajeta pot ID {pot_id}")
        time.sleep(1)

if zbrane_poti:
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=zbrane_poti[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(zbrane_poti)