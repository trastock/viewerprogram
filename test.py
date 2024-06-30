from tabulate import tabulate
import pdfkit


header = ["Tavla", "Namn:", "Klass", "Förening", "S1", "S2", "S3", "S4", "S5", "S6", "TOT", "Anm"]
table = []
row = ["18", 'Emil Ala-Kulju','Herr','Nyköpings Skyttegille', '102.2', '103.1', '104.1' , '105.0', '101.1', '101.2', '611.3', 'DNF']
for i in range(0, 20):
    table.append(row)

html_table = tabulate(table, tablefmt='html', headers=header).__str__()
html_table = html_table.replace("style=\"text-align: right;\"", "")


competition_name = "Dubbeltest juli 2024"
city = "Nyköping"
date = "20/6"
document_type = "Resultat"
relay_title = "Skjutlag 1"
logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"

before_table = "<img class=logopic src=\"" + logopic + "\"> <img class=sponsorpic src=\"" + sponsorpic + "\"> <h1>" + competition_name  + " " + document_type + "&nbsp;</h1> <h2 class=citydate>" + city + " " + date + "</h2> <h2>" + relay_title + "</h2> <figure class=\"table\">"

after_table = "</figure> <p>&nbsp;</p> <p>&nbsp;</p>"

#<img src=\"recourses\\logo.jpg\">

before_table2 = "<html> <head> <link rel=\"stylesheet\" href=\"style.css\">  </head> <body> <img class=logopic src=\"" + logopic + "\"> <img class=sponsorpic src=\"" + sponsorpic + "\"> <h1>" + competition_name  + " " + document_type + "&nbsp;</h1> <h2 class=citydate>" + city + " " + date + "</h2> <h2 class=relaytitle>" + relay_title + "</h2> <figure class=\"table\">"

after_table2 = "</figure> <p>&nbsp;</p> <p>&nbsp;</p> </body> </html>"

ingoing_string = before_table + html_table + after_table


ingoing_string = ingoing_string.replace("Å", "&Aring")
ingoing_string = ingoing_string.replace("å", "&aring")
ingoing_string = ingoing_string.replace("Ä", "&Auml")
ingoing_string = ingoing_string.replace("ä", "&auml")
ingoing_string = ingoing_string.replace("Ö", "&Ouml")
ingoing_string = ingoing_string.replace("ö", "&ouml")

ingoing_string2 = before_table2 + html_table + after_table2


ingoing_string2 = ingoing_string2.replace("Å", "&Aring")
ingoing_string2 = ingoing_string2.replace("å", "&aring")
ingoing_string2 = ingoing_string2.replace("Ä", "&Auml")
ingoing_string2 = ingoing_string2.replace("ä", "&auml")
ingoing_string2 = ingoing_string2.replace("Ö", "&Ouml")
ingoing_string2 = ingoing_string2.replace("ö", "&ouml")



html_path = "test.html"

# Creating an HTML file 
Func = open(html_path,"w") 
   
# Adding input data to the HTML file 
Func.write(ingoing_string2)
              
# Saving the data into the HTML file 
Func.close()


path_to_wkhtml = r'c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtml)

#pdfkit.from_file(html_path, output_path = "test.pdf", configuration = config, css = "style.css", options = {"enable-local-file-access": ""})

pdfkit.from_string(ingoing_string, output_path = "test.pdf", configuration = config, css = "style.css", options = {"enable-local-file-access": ""})