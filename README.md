import asyncio
from collections import defaultdict
import json
import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
def czysc(txt):
    if not txt:
        return ""
    txt = re.sub(r"\[.*?\]", "", txt).replace("\n", " ").strip()
    for o, z in {
        "Å": "A",
        "å": "a",
        "Ä": "A",
        "ä": "a",
        "Ö": "O",
        "ö": "o",
        "É": "E",
        "é": "e",
    }.items():
        txt = txt.replace(o, z)
    return re.sub(r"\s+", " ", txt).strip()

def unifikuj_typ(klasa, sekcja, caly_wiersz):
    k = f"{klasa} {sekcja} {caly_wiersz}".lower()
    reguly = {
        "Okret podwodny": ["submarine", "projekt a17", "projekt a19", "projekt a26"],
        "Fregata": ["frigate", "11540", "neustrashimy", "type 31", "pohjanmaa"],
        "Korweta": ["corvette", "steregushchiy", "buyan", "karakurt", "20380", "21631", "22800", "visby", "goteborg",
                    "stockholm", "gavle", "gävle", "sundsvall"],
        "Kuter rakietowy / Patrolowiec": ["missile boat", "fast attack craft", "tarantul", "hamina", "rauma", "patrol",
                                          "orkan", "660m", "parchim", "1331m", "raptor", "03160", "grachonok", "21980",
                                          "tapper", "altair"],
        "Niszczyciel min / Stawiacz min": ["mine", "sweeper", "layer", "kormoran", "hameenmaa", "pansio", "207",
                                           "mamry", "goplo", "koster", "sturko", "sparo", "vastervik"],
        "Okret desantowy": ["landing", "jehu", "jurmo", "u-700", "u-600", "g class", "775", "zubr", "serna", "11770"]
    }

    for typ, slowa in reguly.items():
        if any(x in k for x in slowa):
            return typ
    return "inne"
async def pobierz_dane():
    strony = {
        "POLSKA": "https://en.wikipedia.org/wiki/List_of_ships_of_the_Polish_Navy#Active_fleet",
        "SZWECJA": "https://en.wikipedia.org/wiki/List_of_active_Swedish_Navy_ships",
        "FINLANDIA": "https://en.wikipedia.org/wiki/List_of_active_Finnish_Navy_ships",
        "ROSJA": "https://en.wikipedia.org/wiki/List_of_active_Russian_Navy_ships",
    }
    okrety_lista = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        for kraj, url in strony.items():
            print(f"Pobieranie danych dla: {kraj}...")
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_selector("table.wikitable")
                soup = BeautifulSoup(await page.content(), "lxml")
            except Exception as e:
                print(f"Błąd ładowania {kraj}: {e}")
                continue

            for tab in soup.find_all("table", class_="wikitable"):
                prev = tab.find_previous(["h2", "h3"])
                nazwa_sekcji = ((prev.find("span").text if prev.find("span") else prev.text) if prev else "")

                if any(x in nazwa_sekcji.lower() for x in ["auxiliary", "training", "tug", "historical", "museum"]):
                    continue
                # Zmienna do zapamiętywania klasy dla wierszy z rowspan (np. Gävle class)
                ostatnia_klasa = ""

                for wiersz in tab.find_all("tr"):
                    if wiersz.find("th") and not wiersz.find("td"):
                        continue

                    cala_linia = wiersz.get_text(" ").lower()

                    if any(x in cala_linia for x in ["total", "sub-total", "decommissioned", "museum ship"]):
                        continue
                    if kraj == "ROSJA" and "baltic" not in cala_linia and "bf" not in cala_linia:
                        continue

                    komorki = wiersz.find_all(["td", "th"])
                    if not komorki:
                        continue

                    lista_okretow = []

                    # 1. Sprawdzamy, czy wiersz ma pełny zestaw kolumn, czy jest "obcięty" przez rowspan
                    # Jeśli ma mało kolumn, a jesteśmy w Szwecji/Polsce/Finlandii, to znaczy że dziedziczy klasę z góry
                    ma_pelne_kolumny = len(komorki) >= 4 or (kraj == "ROSJA" and len(komorki) >= 3)

                    if ma_pelne_kolumny:
                        klasa = czysc(komorki[0].get_text())
                        ostatnia_klasa = klasa  # Zapamiętaj na wypadek kolejnego wiersza ze scaleniem
                    else:
                        klasa = ostatnia_klasa  # Użyj klasy zapamiętanej z wiersza wyżej

                    # 2. Wyciąganie nazw okrętów uwzględniając strukturę
                    if kraj == "ROSJA":
                        projekt = czysc(komorki[1].get_text())
                        nazwa = czysc(komorki[2].get_text())
                        lista_okretow.append(
                            f"Proj. {projekt} {klasa} ({nazwa})" if nazwa else f"Proj. {projekt} {klasa}")

                    elif kraj == "SZWECJA" and wiersz.find("li"):
                        # Dla Visby, gdzie okręty są w liście <li>
                        for li in wiersz.find_all("li"):
                            nazwa_li = czysc(li.get_text())
                            if len(nazwa_li) > 1:
                                lista_okretow.append(f"{klasa} ({nazwa_li})")

                    else:
                        # Logika dla wierszy pojedynczych oraz przesuniętych przez rowspan (np. Gävle / Sundsvall)
                        # Jeśli wiersz jest obcięty przez rowspan, nazwa okrętu będzie w komórce o indeksie 0 lub 1
                        if not ma_pelne_kolumny:
                            nazwa_okretu = czysc(komorki[0].get_text())
                        else:
                            nazwa_okretu = czysc(
                                komorki[2].get_text() if len(komorki) >= 3 and (
                                        " active " in czysc(komorki[1].get_text()).lower() or
                                        klasa == czysc(komorki[1].get_text()) or kraj != "SZWECJA"
                                ) else komorki[1].get_text()
                            )

                        if nazwa_okretu and not any(
                                x in nazwa_okretu.lower() for x in ["active", "built", "entered", "—"]):
                            lista_okretow.append(f"{klasa} ({nazwa_okretu})")
                        elif klasa:
                            lista_okretow.append(klasa)

                    # 3. Przypisywanie typu bojowego i zapis
                    for okret in lista_okretow:
                        if len(okret) < 3 or okret.startswith("—"):
                            continue

                        typ_bojowy = unifikuj_typ(klasa, nazwa_sekcji, cala_linia)
                        if typ_bojowy == "Pomocniczy / Logistyka":
                            continue

                        okrety_lista.append({
                            "kraj": kraj,
                            "okret": okret,
                            "typ": typ_bojowy,
                            "url": url
                        })

        await browser.close()

    podsumowanie = defaultdict(lambda: defaultdict(int))
    for o in okrety_lista:
        podsumowanie[o["kraj"]][o["typ"]] += 1

    with open("wyniki.json", "w", encoding="utf-8") as f:
        json.dump({"podsumowanie": podsumowanie, "okrety": okrety_lista}, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(pobierz_dane())
