from tabulate import tabulate
import pdfkit
import src


header = ["Tavla", "Namn:", "Klass", "Förening", "S1", "S2", "S3", "S4", "S5", "S6", "TOT", "Anm"]
table = []
row = ["18", 'Emil Ala-Kulju','Herr','Nyköpings Skyttegille', '102.2', '103.1', '104.1' , '105.0', '101.1', '101.2', '611.3', 'DNF']
for i in range(0, 15):
    table.append(row)
competition_name = "Dubbeltest juli 2024"
city = "Nyköping"
date = "20/6"
document_type = "Resultat"
relay_title = "Skjutlag 1"
logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"



src.make_pdf(header=header, table=table, competition_name=competition_name,
             city=city, date=date, document_type=document_type, relay_title=relay_title,
             logopic=logopic, sponsorpic=sponsorpic, pdf_path="test2.pdf"
)

