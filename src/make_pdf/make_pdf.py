from tabulate import tabulate
import pdfkit

def make_pdf(table, header, competition_name, city, date, document_type, 
             relay_title, logopic, sponsorpic, pdf_path, time="",
             sort_by=0,
             path_to_wkhtml=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"):

    table = sorted(table, key=lambda k: float(k[sort_by]) if k[sort_by] != "" else float("inf"))

    # HTML: logotyp och rubriker i separata divar
    before_table = f"""
        <img class="logopic" src="{logopic}">
        <img class="sponsorpic" src="{sponsorpic}">
        <div class="titles">
            <h1>{competition_name} {document_type}&nbsp;</h1>
            <h2 class="citydate">{city} {date} {time}</h2>
            <h2>{relay_title}</h2>
        </div>
        <figure class="table">
    """

    after_table = "</figure><p>&nbsp;</p><p>&nbsp;</p>"

    html_table = tabulate(table, tablefmt='html', headers=header).__str__()
    html_table = html_table.replace('style="text-align: right;"', "")

    # Ersätt specialtecken
    replacements = {
        "Å": "&Aring;", "å": "&aring;",
        "Ä": "&Auml;", "ä": "&auml;",
        "Ö": "&Ouml;", "ö": "&ouml;",
        "Ü": "&Uuml;", "ü": "&uuml;",
    }

    for char, html_entity in replacements.items():
        html_table = html_table.replace(char, html_entity)
        before_table = before_table.replace(char, html_entity)

    full_html = before_table + html_table + after_table

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtml)

    pdfkit.from_string(
        full_html,
        output_path=pdf_path,
        configuration=config,
        css=r"src\make_pdf\style.css",
        options={"enable-local-file-access": ""}
    )
