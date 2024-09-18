from jinja2 import Environment,FileSystemLoader
import jdatetime
import pdfkit
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("template.html")
output = template.render()
with open(r"templates/newtemplate.html",mode='w',encoding='utf-8') as tm:
    tm.write(output)

wkhtmltopdf =r""
file = r"templates/newtemplate.html"
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
pdfkit.from_file(file,output_path="facture.pdf",configuration = config)
    