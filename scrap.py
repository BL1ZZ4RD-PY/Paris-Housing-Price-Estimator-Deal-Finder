import re
import pandas as pd
from playwright.sync_api import sync_playwright


def ajout_prix(card, liste_prix):
    prix = card.locator('div.encoded-lnk').inner_text().strip(" ")
    prix = re.sub(r"\s+", "", prix)
    motif_prix = r"[-+]?\d+(?:\.\d+)?"
    prix_texte = re.findall(motif_prix, prix)
    if prix_texte:
        liste_prix.append(float(prix_texte[0]))
    else:
        liste_prix.append(None)


def ajout_surface(card, liste_surface):
    motif_surface = r"[-+]?\d+(?:[.,]\d+)?(?=\s*(?:m2|m²))"
    surface = card.locator('a.hover\\:no-underline').first.inner_text()
    surface_texte = re.findall(motif_surface, surface)
    if surface_texte:
        liste_surface.append(int(surface_texte[0]))
    else:
        liste_surface.append(None)


def ajout_arrondissement(card, liste_arrondissement):
    motif_arrondissement = r"(?<=(?:Paris ))\s*[-+]?\d+(?:[.,]\d+)?"
    arrondissement = card.locator('a.hover\\:no-underline').first.inner_text()
    arrondissement_texte = re.findall(motif_arrondissement, arrondissement)
    if arrondissement_texte:
        liste_arrondissement.append(int(arrondissement_texte[0]))
    else:
        liste_arrondissement.append(None)

def run_scraping():
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36')
        page = context.new_page()
    
        try:

            liste_prix = []
            liste_surface = []
            liste_arrondissement = []
            page.goto(
                "https://www.paruvendu.fr/immobilier/recherche/location/appartement/paris-75/?rechpv=1&tt=5&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&lo=75&ddlFiltres=nofilter&prestige=0",
                wait_until='networkidle'
                )
            parent_block = page.locator("p.text-sm").all()
            card = parent_block[-1].first.inner_text()
            motif_card = r"(?<=(?:sur ))\s*[-+]?\d+(?:[.,]\d+)?"
            page_text = re.findall(motif_card, card)
            nombre_pages = int(float(page_text[0])//29)+1

            for i in range(1, nombre_pages+1):
                print(f'Analyse de la page {i}')
                page.goto(
                    f"https://www.paruvendu.fr/immobilier/recherche/location/appartement/paris-75/?rechpv=1&tt=5&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&lo=75&ddlFiltres=nofilter&prestige=0&p={i}",
                    wait_until='networkidle'
                )

                parent_block = page.locator("div.blocAnnonce").all()

                for card in parent_block:
                    ajout_prix(card, liste_prix)
                    ajout_surface(card, liste_surface)
                    ajout_arrondissement(card, liste_arrondissement)

            df = pd.DataFrame({"Prix" : liste_prix, "Surface" : liste_surface, "Arrondissement" : liste_arrondissement})
            df.to_csv('Data_Loyer.csv', index=False)

        except Exception as e:
            print(f"Exception {e}")

        finally:
            print('Fin du scraping')
            browser.close()
        return 'Data_Loyer.csv'
    
if __name__ == '__main__':
    run_scraping()
    