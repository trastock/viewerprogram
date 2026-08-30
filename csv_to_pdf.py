import csv
import os
import src

# ===== Base directory =====

BASE_DIR = "dubbeltestjuli2026"

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# ===== Bilder =====
logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"


# ===== PDF-information =====

competition_name = "Dubbeltest Juli 2026"
city = "Nyköping"
date = "18/7"

# ===== Loopa igenom alla CSV-filer =====

for file in os.listdir(DATA_DIR):

    # Hoppa över filer som inte är csv
    if not file.endswith(".csv"):
        continue

    csv_path = os.path.join(DATA_DIR, file)

    # ===== Hämta info från filnamn =====

    filename = os.path.splitext(file)[0]

    parts = filename.split("_")

    document_type = parts[0]
    relay_title = parts[1]

    # ===== Läs CSV =====

    with open(csv_path, newline='', encoding='utf-8') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')

        rows = list(reader)

    header = rows[0]
    table = rows[1:]

    # ===== PDF-path =====

    pdf_filename = filename + ".pdf"

    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    # ===== Skapa PDF =====
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    src.make_pdf(
        header=header,
        table=table,
        competition_name=competition_name,
        city=city,
        date=date,
        document_type=document_type,
        relay_title=relay_title,
        logopic=logopic,
        sponsorpic=sponsorpic,
        pdf_path=pdf_path
    )

    print(f"Skapade: {pdf_path}")