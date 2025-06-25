import time
from unittest import result
import pandas as pd
import codecs
import re
def extract_tot_value(tot_str):
    if pd.isna(tot_str):
        return 0
    match = re.search(r'\d+', str(tot_str))
    return int(match.group()) if match else 0

def main():
    try:
        from .src.client import update_data, data_setup
        from .src import make_pdf
    except:
        from src.client import update_data, data_setup
        from src import make_pdf

    s = data_setup()
    if s is None:
        return

    outdata = {}
    df_shot = pd.DataFrame()

    try:
        while True:
            updated = update_data(s, outdata)
            if updated is not None:
                outdata = updated

                # === Bygg name_df från _NAME när data finns ===
                name_df = pd.DataFrame(outdata.get("_NAME", []))
                team_df = pd.DataFrame(outdata.get("_TEAM", []))
                totl_df = pd.DataFrame(outdata.get("_TOTL", []))
                snat_df = pd.DataFrame(outdata.get("_SNAT", []))
                #print(outdata["_TOTL"])
                if not name_df.empty:
                    try:
                        name_df = name_df[[2, 5]]
                        name_df.columns = ["Bana", "Namn"]
                        team_df = team_df[[2, 5]]
                        team_df.columns = ["Bana", "Förening"]
                        snat_df = snat_df[[2, 5]]
                        snat_df.columns = ["Bana", "Klass"]
                        #subt_df = subt_df[[2, 18, 21]]
                        #subt_df = subt_df.drop_duplicates()
                        #subt_df.columns = ["Bana", "serie 1", "serie 2"]
                        #subt_df = subt_df.T
                        #subt_df.columns = subt_df.columns.str.strip()
                        totl_df = totl_df[[2, 6]]
                        totl_df.columns = ["Bana", "Tot"]
                        totl_df = totl_df.drop_duplicates()
                        name_df = pd.merge(name_df, team_df, on="Bana", how="outer")
                        name_df = pd.merge(name_df, snat_df, on="Bana", how="outer")
                        #print(name_df)
                        def decode_name(name):
                            try:
                                return codecs.decode(name, 'unicode_escape')
                            except:
                                return name

                        name_df["Namn"] = name_df["Namn"].apply(decode_name)
                        name_df["Förening"] = name_df["Förening"].apply(decode_name)
                        name_df["Klass"] = name_df["Klass"].apply(decode_name)
                        name_df = name_df.drop_duplicates()
                        #print(repr(name_df["Namn"].iloc[3]))
                    except Exception as e:
                        print("Kunde inte bygga name_df:", e)
                        name_df = pd.DataFrame(columns=["Bana", "Namn"])  # tom men korrekt

                # === Bearbeta nya skott ===
                new_shots = outdata.get("_SHOT", [])
                if new_shots:
                    df_new = pd.DataFrame(new_shots)
                    df_new.columns = list(range(df_new.shape[1]))
                    df_new = df_new.rename(columns={2: "Bana"})

                    if not name_df.empty:
                        df_new = pd.merge(df_new, name_df, on="Bana", how="left")

                    df_shot = pd.concat([df_shot, df_new], ignore_index=True)
                    df_shot = df_shot.drop_duplicates(ignore_index=True)
                    outdata["_SHOT"].clear()
                    
                    # Steg 1: Slå ihop båda dataframes på 'Bana'
                    # Se till att subt_df["Bana"] är numerisk så att merge fungerar korrekt
                    #print("Test")
                    
                    #print("Kolumner i subt_df:", subt_df.columns.tolist())
                    #print("Förhandsvisning av subt_df:")
                    #print(subt_df.head())
                    subt_df = pd.DataFrame(outdata.get("_TOTL", []))
                    
                    if not subt_df.empty:
                        subt_df = subt_df.drop_duplicates(subset=[2], keep="last")
        
                    available_cols = subt_df.columns

                    bana_col = subt_df[2] if 2 in available_cols else pd.Series([None] * len(subt_df))
                    serie1_col = subt_df[18] if 18 in available_cols else pd.Series([0] * len(subt_df))
                    serie2_col = subt_df[21] if 21 in available_cols else pd.Series([0] * len(subt_df))
                    serie3_col = subt_df[24] if 24 in available_cols else pd.Series([0] * len(subt_df))
                    serie4_col = subt_df[27] if 27 in available_cols else pd.Series([0] * len(subt_df))
                    reserve_col = subt_df[30] if 30 in available_cols else pd.Series([0] * len(subt_df))

                    
                    subt_df = pd.DataFrame({
                    "Bana": bana_col,
                    "Serie 1": serie1_col,
                    "Serie 2": serie2_col,
                    "Serie 3": serie3_col,
                    "Serie 4": serie4_col,
                    "Reserve": reserve_col
                    })
                    
                    subt_df = subt_df.dropna(subset=["Bana"])
                    
                    subt_df["Bana"] = pd.to_numeric(subt_df["Bana"], errors="coerce")


                    subt_df["Bana"] = subt_df["Bana"].astype(str)
                    name_df["Bana"] = name_df["Bana"].astype(str)
                    merged = pd.merge(subt_df, name_df, on="Bana", how="inner")
                    # Steg 2: Kombinera serie 1 och serie 2 till en lista
                    merged["Serier"] = merged[["Serie 1", "Serie 2", "Serie 3", "Serie 4", "Reserve"]].values.tolist()
                    # Steg 3: Gruppera per Bana, Namn, team och samla ihop alla serier
                    result = (
                        merged.groupby(["Bana", "Namn", "Förening", "Klass"], as_index=False)[
                            ["Serie 1", "Serie 2", "Serie 3", "Serie 4"]
                        ].last()
                    )
                    totl_df = totl_df.drop_duplicates(subset=["Bana"], keep="last")  # eller "first" beroende på vad du vill
                    result = pd.merge(result, totl_df, on="Bana", how="right")


                    result["Tot_clean"] = result["Tot"].apply(extract_tot_value)
                    result = result.sort_values(by=["Klass", "Tot_clean"], ascending=[True, False])

                    result = result.fillna(0)

                    # Visa resultat per klass
                    for klass, grupp in result.groupby("Klass", sort=False):
                        print(f"\n=== Klass: {klass} ===")
                        print(grupp.drop(columns=["Tot_clean"]).to_string(index=False))
                    
                    result = result.drop(columns=["Tot_clean"], errors="ignore")
                    with open("resultat_per_klass.txt", "w", encoding="utf-8") as f:
                        for klass, grupp in result.groupby("Klass"):
                            f.write(f"=== Klass: {klass} ===\n")
                            grupp.to_string(f, index=False)
                            f.write("\n\n")                    # Exempel: visa resultat per klass
                    #print(result)
                    
                    #print(subt_df)
                    #print(name_df)
                    #print(f"Totalt {len(df_shot)} unika _SHOT-rader nu.")
                    df_shot.to_csv("shot_data.csv", index=False)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nAvslutar loop på Ctrl+C")
        df_shot.to_csv("shot_data.csv", index=False)
        print("Sparade _SHOT till shot_data.csv")
        s.close()

if __name__ == "__main__":
    main()
