import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def nettoyage_donnees(file="Data_Loyer.csv"):
    df = pd.read_csv(file)
    df = df.dropna(subset=["Prix", "Surface", "Arrondissement"])
    df['Arrondissement'] = df['Arrondissement'].astype(int)
    df['Prix m2'] = df['Prix']/df['Surface']
    df = df[(df["Prix m2"] >= 15 ) & (df["Prix m2"] <= 80 )]
    return df

def features_target(df):
    encoder = OneHotEncoder(handle_unknown="ignore")
    y = df["Prix"]
    x = df[["Surface", "Arrondissement"]]

    transform_x = ColumnTransformer(
        transformers=[('Arrondissement', encoder, ["Arrondissement"])],
        remainder='passthrough')

    X = transform_x.fit_transform(x)
    return X, y

def model_entrainement(x, y, df):
    x, y = features_target(df)
    regressor = RandomForestRegressor(random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    regressor.fit(x_train, y_train)
    score = r2_score(y_test, regressor.predict(x_test))
    mean = mean_absolute_error(y_test, regressor.predict(x_test))
    print(f"Précision : {round(score*100)}%")
    print(f"Marge d'erreur : {round(mean)} €")
    return regressor

def bon_plan(regressor, x, y, df):
    X = regressor.predict(x)
    df['Estimation'] = X
    df["Decote"] = ((df["Prix"] - df["Estimation"]) / df["Estimation"])*100
    df = df[df["Decote"] <= -15]
    df = df.sort_values(by=["Decote"], ascending=True)
    df.to_csv("Appartement_interessant.csv", index=False)
    return 'csv créée'

if "__main__" == __name__:
    df = nettoyage_donnees()
    x, y = features_target(df)
    regressor = model_entrainement(x, y, df)
    print(bon_plan(regressor, x, y, df))








