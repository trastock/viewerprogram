import time
import pandas as pd
import codecs
import re

def extract_tot_value(tot_str):
    if pd.isna(tot_str):
        return 0
    match = re.search(r'\d+', str(tot_str))
    return int(match.group()) if match else 0

def decode_name(name):
    try:
        return codecs.decode(name, 'unicode_escape')
    except:
        return name

def get_data(s, outdata, df_shot, latest_tot_dict):
    from src.client import update_data
    import pandas as pd

    updated = update_data(s, outdata)
    if updated is None:
        return outdata, df_shot, latest_tot_dict

    outdata = updated

    name_df = pd.DataFrame(outdata.get("_NAME", []))
    team_df = pd.DataFrame(outdata.get("_TEAM", []))
    totl_df = pd.DataFrame(outdata.get("_TOTL", []))
    snat_df = pd.DataFrame(outdata.get("_SNAT", []))

    if not name_df.empty:
        try:
            name_df = name_df[[2, 5]]
            name_df.columns = ["Bana", "Namn"]
            team_df = team_df[[2, 5]]
            team_df.columns = ["Bana", "Förening"]
            if not snat_df.empty and 2 in snat_df.columns and 5 in snat_df.columns:
                snat_df = snat_df[[2, 5]]
                snat_df.columns = ["Bana", "Klass"]
            else:
                snat_df = pd.DataFrame(columns=["Bana", "Klass"])

            if 2 in totl_df.columns and 6 in totl_df.columns:
                totl_df = totl_df[[2, 6]]
                totl_df.columns = ["Bana", "Tot"]
            else:
                totl_df = pd.DataFrame(columns=["Bana", "Tot"])

            totl_df = totl_df.drop_duplicates()
            name_df = pd.merge(name_df, team_df, on="Bana", how="outer")
            name_df = pd.merge(name_df, snat_df, on="Bana", how="outer")
            name_df["Namn"] = name_df["Namn"].apply(decode_name)
            name_df["Förening"] = name_df["Förening"].apply(decode_name)
            name_df["Klass"] = name_df["Klass"].apply(decode_name)
            name_df = name_df.drop_duplicates()
        except Exception as e:
            print("Kunde inte bygga name_df:", e)
            name_df = pd.DataFrame(columns=["Bana", "Namn"])

    new_shots = outdata.get("_SHOT", [])
    if new_shots:
        df_new = pd.DataFrame(new_shots)
        df_new.columns = list(range(df_new.shape[1]))

        # Kontrollera att kolumn 2 finns, annars avbryt tidigt
        if 2 not in df_new.columns:
            print("⚠️ Saknas kolumn 2 i df_new, hoppar över nya skott")
            return outdata, df_shot, latest_tot_dict

        df_new = df_new.rename(columns={2: "Bana"})

        if not name_df.empty:
            df_new = pd.merge(df_new, name_df, on="Bana", how="left")

        df_new["Bana"] = df_new["Bana"].astype(str)

        # Sätt Typ - default till "Prov"
        df_new["Typ"] = "Prov"
        if not totl_df.empty:
            totl_df = totl_df.drop_duplicates(subset=["Bana"], keep="last")
            for _, row in totl_df.iterrows():
                bana = str(row["Bana"])
                ny_tot = extract_tot_value(row["Tot"])
                gammal_tot = latest_tot_dict.get(bana, 0)

                mask = df_new["Bana"] == bana
                if mask.any():
                    try:
                        # Kolla kolumn 10 finns först
                        if 10 in df_new.columns:
                            df_new.loc[mask, "Typ"] = df_new.loc[mask][10].apply(
                                lambda x: "Match" if ny_tot > gammal_tot and pd.to_numeric(x, errors="coerce") > 0 else "Prov"
                            )
                    except Exception as e:
                        print(f"Kunde inte sätta 'Typ' för bana {bana}: {e}")
                latest_tot_dict[bana] = ny_tot

        # Säkerställ att alla förväntade kolumner finns, annars sätt defaultvärden
        expected_cols = {2: "", 10: 0, 11: 0, 14: 0, 15: 0}
        for col, default in expected_cols.items():
            if col not in df_new.columns:
                df_new[col] = default

        # "_hash" verkar användas, lägg till kolumn med default om den saknas
        if "_hash" not in df_new.columns:
            df_new["_hash"] = ""

        # Filtrera och byt namn på kolumner
        df_filtered = df_new[[2, 10, 11, 14, 15, "Bana", "Namn", "Förening", "Klass", "Typ", "_hash"]].copy()
        df_filtered.columns = ["Bana", "integer", "decimal", "x", "y", "Bana_str", "Namn", "Förening", "Klass", "Typ", "_hash"]

        # Om du inte behöver Bana_str kan du ta bort den
        df_filtered = df_filtered.drop(columns=["Bana_str"])

        # Lägg till i df_shot och spara
        df_shot = pd.concat([df_shot, df_filtered], ignore_index=True)
        df_shot.to_parquet("shot_data.parquet", index=False)

        # Töm _SHOT i outdata efter behandling
        outdata["_SHOT"].clear()

    return outdata, df_shot, latest_tot_dict




def skriv_ut_resultat_med_diff(parquet_path="shot_data.parquet", serie_struktur=None):
    if serie_struktur is None:
        serie_struktur = {"Serie 1": 5, "Serie 2": 5, "Serie 3": 2}

    try:
        df = pd.read_parquet(parquet_path)
    except FileNotFoundError:
        print(f"Filen '{parquet_path}' hittades inte.")
        return

    df["Bana"] = df["Bana"].astype(str)
    df["integer"] = pd.to_numeric(df["integer"], errors="coerce").fillna(0).astype(int)
    df["decimal"] = pd.to_numeric(df["decimal"], errors="coerce").fillna(0).astype(int)
    df["Poäng"] = df["integer"] + df["decimal"] / 10

    # Gruppnyckel per skytt
    gruppnyckel = ["Bana", "Namn", "Förening", "Klass"]
    resultat_lista = []

    for namn, grupp in df.groupby(gruppnyckel):
        bana, skyttnamn, förening, klass = namn
        skott = grupp.sort_index().reset_index(drop=True)

        start = 0
        totalsumma = 0
        serier = {}

        for serienamn, antal in serie_struktur.items():
            serie_skott = skott.iloc[start:start+antal]
            start += antal
            summa = serie_skott["Poäng"].sum()
            totalsumma += summa
            serier[serienamn] = {
                "poänglista": serie_skott["Poäng"].tolist(),
                "summa": summa
            }

        resultat_lista.append({
            "Namn": skyttnamn,
            "Förening": förening,
            "Klass": klass,
            "Totalt": round(totalsumma, 1),
            "Serier": serier
        })

    # Sortera efter totalpoäng
    resultat_lista = sorted(resultat_lista, key=lambda x: -x["Totalt"])
    ledarpoäng = resultat_lista[0]["Totalt"] if resultat_lista else 0

    print("\n================ RESULTATLISTA ================\n")
    for i, skytt in enumerate(resultat_lista, start=1):
        diff = skytt["Totalt"] - ledarpoäng
        print(f"{i:>2}. {skytt['Namn']} | {skytt['Förening']} | {skytt['Klass']} | Totalt: {skytt['Totalt']:.1f} | Diff: {diff:+.1f}")
        for serienamn, serie in skytt["Serier"].items():
            poängstr = " ".join(f"{p:.1f}" for p in serie["poänglista"])
            print(f"    {serienamn:<8}: {poängstr:<40} Summa: {serie['summa']:.1f}")
        print()







def main():
    try:
        from src.client import update_data, data_setup
    except ImportError:
        from .src.client import update_data, data_setup

    s = data_setup()
    if s is None:
        return

    outdata = {}
    df_shot = pd.DataFrame()
    latest_tot_dict = {}

    try:
        while True:
            outdata, df_shot, latest_tot_dict = get_data(s, outdata, df_shot, latest_tot_dict)
            skriv_ut_resultat_med_diff("shot_data.parquet", {"Serie 1": 5, "Serie 2": 5, "Serie 3": 2, "Serie 4": 2})
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nAvslutar loop på Ctrl+C")
        df_shot.to_csv("shot_data.csv", index=False)
        print("Sparade _SHOT till shot_data.csv")
        s.close()

if __name__ == "__main__":
    main()
