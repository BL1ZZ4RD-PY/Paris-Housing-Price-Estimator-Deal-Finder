from scrap import run_scraping
from model import nettoyage_donnees, features_target, model_entrainement, bon_plan

if __name__ == "__main__":
    print("1. Lancement du Web Scraping...")
    fichier = run_scraping()


    if fichier:
        print("\n2. Nettoyage des données...")
        df = nettoyage_donnees(fichier)
        x, y = features_target(df)

        print("\n3. Entraînement du modèle Machine Learning...")
        regressor = model_entrainement(x, y, df)

        print("\n4. Export des opportunités sous-évaluées...")
        bon_plan(regressor, x, y, df)

        print("\n Pipeline exécuté avec succès !")