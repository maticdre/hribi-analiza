import csv
import re

IN_FILE = "../podatki/processed_poti.csv"
OUT_FILE = "../podatki/poti.csv"


def loci_ime_visino(besedilo):
    besedilo = besedilo.strip()
    if "(" in besedilo and "m)" in besedilo:
        delci = besedilo.split("(")
        ime = delci[0].strip()
        visina = delci[1].replace("m)", "").replace(" ", "").strip()
        return ime, visina
    return besedilo, ""


def cas_v_minute(cas_str):
    h = re.search(r"(\d+)\s*h", cas_str)
    m = re.search(r"(\d+)\s*min", cas_str)

    ure = int(h.group(1)) if h else 0
    minute = int(m.group(1)) if m else 0
    skupaj = ure * 60 + minute

    return str(skupaj) if skupaj > 0 else ""


ocisceni_podatki = []


with open(IN_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for vrstica in reader:
        izhodisce, izh_visina = loci_ime_visino(vrstica.get("izhodisce", ""))
        cilj, cilj_visina = loci_ime_visino(vrstica.get("cilj", ""))

        koordinate = re.findall(r"([\d,.]+)", vrstica.get("sirina_dolzina", ""))
        sirina = koordinate[0].replace(",", ".") if len(koordinate) > 0 else ""
        dolzina = koordinate[1].replace(",", ".") if len(koordinate) > 1 else ""

        # Določitev stopnje zahtevnosti
        zahtevnost_str = vrstica.get("zahtevnost", "").lower()
        stopnja = (3 if "zelo zahtevna" in zahtevnost_str else
            2 if "zahtevna" in zahtevnost_str else 1 if "lahka" in zahtevnost_str else "")
        oznacena = 1 if "označena" in zahtevnost_str and "neoznačena" not in zahtevnost_str else 0

        # Poenotenje zapisa dolžine v km
        km = re.search(r"([\d,.]+)", vrstica.get("dolzina_km", ""))
        dolzina_km = km.group(1).replace(",", ".") if km else ""

        ocisceni_podatki.append({
            "gora_id": vrstica.get("gora_id", ""),
            "pot_id": vrstica.get("pot_id", ""),
            "izhodisce": izhodisce,
            "izhodisce_visina_m": izh_visina,
            "sirina": sirina,
            "dolzina": dolzina,
            "cilj": cilj,
            "cilj_visina_m": cilj_visina,
            "ime_poti": vrstica.get("ime_poti", ""),
            "cas_hoje_min": cas_v_minute(vrstica.get("cas_hoje", "")),
            "dolzina_km": dolzina_km,
            "zahtevnost": stopnja,
            "oznacena": oznacena,
            "ferata": vrstica.get("ferata", ""),
            "visinska_razlika_m": vrstica.get("visinska_razlika_m", ""),
            "visinska_razlika_po_poti_m": vrstica.get("visinska_razlika_po_poti_m", ""),
            "zemljevid": vrstica.get("zemljevid", ""),
            "oprema_poletje": vrstica.get("oprema_poletje", ""),
            "oprema_zima": vrstica.get("oprema_zima", ""),
            "ogledi": vrstica.get("ogledi", ""),
            "stevilo_slik": vrstica.get("stevilo_slik", ""),
            "stevilo_komentarjev": vrstica.get("stevilo_komentarjev", "")
        })

if ocisceni_podatki:
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ocisceni_podatki[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(ocisceni_podatki)

print("Podatki o poteh so očiščeni.")
