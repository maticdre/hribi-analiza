import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKRIPTE = [
    "zajemanjepodatkov/scraper_hribi.py",
    "zajemanjepodatkov/scraper_poti.py",
    "obdelavapodatkov/datacleaning_hribi.py",
    "obdelavapodatkov/datacleaning_poti.py",
]

def poganjalnik():
    for skripta in SKRIPTE:
        polna_pot = os.path.join(BASE_DIR, skripta)
        ime_skripte = os.path.basename(polna_pot)
        mapa_skripte = os.path.dirname(polna_pot)

        rezultat = subprocess.run([sys.executable, polna_pot], cwd=mapa_skripte)

        if rezultat.returncode != 0:
            print(f"\n[Napaka] Skripta {ime_skripte}")
            sys.exit(1)

    print("\nZaključeno!")

if __name__ == "__main__":
    poganjalnik()