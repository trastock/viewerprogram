from src import make_pdf



import pandas as pd

# Läs filen (separator = tabbar)
df = pd.read_csv("resultatlista.csv", sep=";", encoding="latin1")

# Fyll tomma celler med tomma strängar (för säkerhet)
df.fillna("", inplace=True)


table = df.values.tolist()       # list of rows
header = df.columns.tolist()     # list of column names

make_pdf(
    table=table,
    header=header,
    competition_name="Dubbeltest Juli 2025",
    city="Nyköpings Skyttegille",
    date="2025-07-12",
    document_type="Resultatlista",
    relay_title="Ställningsfinal",
    logopic="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s",
    sponsorpic="https://static.unpr.io/userfiles/WnRFVFhxaUVHY1l6QWVEcUtQUkliQT09/images/pirat_reklam_logotype_hemsidan.png?size=800&q=100",
    pdf_path="C:\\Users\\emila\\OneDrive - Linköpings universitet\\Documents\\Dubbeltest Nyköping 2025 juli\\Resultat\\Ställningsfinal.pdf",
    time="16:30",
    sort_by=0,
    path_to_wkhtml=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
)
