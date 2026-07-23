import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_predict

def nettoyage_donnees(file="Data_Loyer.csv"):
    df = pd.read_csv(file)
    df = df.dropna(subset=["Prix", "Surface", "Arrondissement", "Pieces", "DPE"])
    df['Arrondissement'] = df['Arrondissement'].astype(int)
    df['Pieces'] = df['Pieces'].astype(int)
    df['DPE'] = df['DPE'].astype(int)
    df['Prix m2'] = df['Prix']/df['Surface']
    df = df[df["Prix"] <= 3000]
    df = df[(df["Prix m2"] >= 15 ) & (df["Prix m2"] <= 80 )]
    df["Surface par pieces"] = df["Surface"]/df["Pieces"]
    return df

def model_entrainement(df):
    encoder = OneHotEncoder(handle_unknown="ignore")
    y = np.log1p(df["Prix"])
    x = df[["Surface", "Arrondissement", "Pieces", "DPE", "Surface par pieces"]]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    preprocessor = ColumnTransformer(
        transformers=[('cat', encoder, ["Arrondissement"])],
        remainder='passthrough')

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', RandomForestRegressor(n_estimators=100, max_depth=12, random_state=0))
                     ])

    model.fit(x_train, y_train)

    return model, x, y

def bon_plan(model, x, y, df):
    df = df.copy()
    y_pred_log = cross_val_predict(model, x, y, cv=5)
    df['Estimation'] = np.expm1(y_pred_log)
    print(mean_absolute_error(df['Prix'], df['Estimation']))
    print(r2_score(df['Prix'], df['Estimation']))
    df["Decote"] = ((df["Prix"] - df["Estimation"]) / df["Estimation"])*100
    df = df[df["Decote"] <= -15]
    df = df.sort_values(by=["Decote"], ascending=True)
    df.to_csv("Appartement_interessant.csv", index=False)

    return 'csv créée'

if "__main__" == __name__:
    df = nettoyage_donnees()
    model, x, y = model_entrainement(df)
    print(bon_plan(model, x, y, df))
