# Analiza slovenskih in tujih gora ter pohodniških poti

Analiza obravnava podatke o gorskih vrhovih in pohodniških poteh, predhodno zajete s spletne strani [hribi.net](https://www.hribi.net/).

Podatki so shranjeni v mapi `podatki/` v dveh datotekah:
- **`hribi.csv`** – vrhovi (ime, država, gorovje, višina, koordinate, priljubljenost, število ogledov ...)
- **`poti.csv`** – pohodniške poti (izhodišče, čas hoje, dolžina, zahtevnost, oprema ...), pri čemer je vsaka pot z vrhom povezana prek stolpca `gora_id`.

## Zagon in uporaba

### 1. Ogled pripravljene analize
Pripravljena analiza z že zajetimi podatki iz mape `podatki/` se nahaja v Jupyter Notebook datoteki:
- **`analiza.ipynb`**

Datoteko lahko odprete in si ogledate celotno analizo skupaj z grafičnimi prikazi.

### 2. Zajem najnovejših podatkov (neobvezno)
Če želite sami ponovno zajeti najnovejše podatke s spletne strani in osvežiti analizo, poženite skripto:

```bash
python main.py