from tabulate import tabulate
import pdfkit


header = ["Namn:", "Klass", "Förening", "S1", "S2", "S3", "S4", "S5", "S6", "TOT", "Anm"]

table = [['Emil Ala-Kulju','Herr','Nyköping', '102', '103', '104.1' , '105.0', '101.1', '101.2', '611.3', 'DNF']]

html_table = tabulate(table, tablefmt='html', headers=header).__str__()

competition_name = "Dubbeltest juli 2024"
city = "Nyköping"
date = "20/6"
document_type = "Startlista"
relay_title = "Skjutlag 1"

before_table = " <h1>" + competition_name  + " " + document_type + "&nbsp;</h1> <h2>" + city + " " + date + "</h2> <h2>" + relay_title + "</h2> <figure class=\"table\">"

after_table = "</figure> <img src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s\"> <p>&nbsp;</p> <p>&nbsp;</p>"

#<img src=\"recourses\\logo.jpg\">

#before_table = "<html> <head> <link rel=\"stylesheet\" href=\"style.css\">  </head> <body> <h1>" + competition_name  + " " + document_type + "&nbsp;</h1> <h2>" + city + " " + date + "</h2> <h2>" + relay_title + "</h2> <figure class=\"table\">"

#after_table = "</figure> <p>&nbsp;</p> <p>&nbsp;</p> </body> </html>"

ingoing_string = before_table + html_table + after_table


ingoing_string = ingoing_string.replace("Å", "&Aring")
ingoing_string = ingoing_string.replace("å", "&aring")
ingoing_string = ingoing_string.replace("Ä", "&Auml")
ingoing_string = ingoing_string.replace("ä", "&auml")
ingoing_string = ingoing_string.replace("Ö", "&Ouml")
ingoing_string = ingoing_string.replace("ö", "&ouml")

html_path = "test.html"

# Creating an HTML file 
Func = open(html_path,"w") 
   
# Adding input data to the HTML file 
Func.write(ingoing_string)
              
# Saving the data into the HTML file 
Func.close()


path_to_wkhtml = r'c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtml)

#pdfkit.from_file(html_path, output_path = "test.pdf", configuration = config, css = "style.css")

pdfkit.from_string(ingoing_string, output_path = "test.pdf", configuration = config, css = "style.css", options = {"enable-local-file-access": ""})