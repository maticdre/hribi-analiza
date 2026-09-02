import re


def izlusci(vzorec, besedilo, samo_stevilke=False):
    ujemanje = re.search(vzorec, besedilo)
    if ujemanje:
        vrednost = ujemanje.group(1).strip()
        if samo_stevilke:
            return re.sub(r"\D", "", vrednost)
        return vrednost
    return ""
