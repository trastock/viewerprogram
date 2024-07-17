from tabulate import tabulate
import pdfkit
#path_to_wkhtml = '/bin/wkhtmltopdf'
#/home/emil/privata_proj/viewerprogram/src/make_pdf/style.css

def make_pdf(table, header, competition_name, city, date, document_type, 
             relay_title, logopic, sponsorpic, pdf_path, time = "",
             sort_by = 0,
             path_to_wkhtml =r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"):
    
    before_table = ("<img class=logopic src=\"" + logopic + 
                    "\"> <img class=sponsorpic src=\"" + 
                    sponsorpic + "\"> <h1>" + competition_name  + 
                    " " + document_type + "&nbsp;</h1> <h2 class=citydate>" + 
                    city + " " + date + " " + time + "</h2> <h2>" + relay_title + 
                    "</h2> <figure class=\"table\">")
    after_table = "</figure> <p>&nbsp;</p> <p>&nbsp;</p>"
    
    table = sorted(table, key=lambda k: float(k[sort_by]))
    
    html_table = tabulate(table, tablefmt='html', headers=header).__str__()
    html_table = html_table.replace("style=\"text-align: right;\"", "")
    
    ingoing_string = before_table + html_table + after_table
    ingoing_string = ingoing_string.replace("Å", "&Aring")
    ingoing_string = ingoing_string.replace("å", "&aring")
    ingoing_string = ingoing_string.replace("Ä", "&Auml")
    ingoing_string = ingoing_string.replace("ä", "&auml")
    ingoing_string = ingoing_string.replace("Ö", "&Ouml")
    ingoing_string = ingoing_string.replace("ö", "&ouml")

    config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtml)
    
    pdfkit.from_string(ingoing_string, output_path = pdf_path, 
                       configuration = config, css = r"src\make_pdf\style.css", 
                       options = {"enable-local-file-access": ""})