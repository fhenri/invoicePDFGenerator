from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
import babel.numbers
import json
import os
import pdfkit
import sys

def format_currency_amount(value, currency="USD"):
    pNumber = babel.numbers.format_currency(value, currency, locale='en_US')
    return pNumber

def generate (payload):
    environment = Environment(loader=FileSystemLoader("resources/templates/"))
    environment.filters["format_currency"] = format_currency_amount
    invoice_zoho_template = environment.get_template("invoice.html")
    footer_template = environment.get_template("footer.html")

    invoice_generate_options = {
        'enable-local-file-access': None,
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0.75in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'footer-html': footer_template.filename,
        'no-outline': None
    }

    print('make directory')
    os.makedirs(os.path.join("resources", "out"), exist_ok=True)
    os.makedirs(os.path.join("resources", "pdf"), exist_ok=True)

    invoices = payload['invoices']
    for invoice in invoices:

        invoice_date = invoice['invoice_date']
        pay_term = invoice['pay_term'] if invoice['pay_term'] else 60
        invoice_due_date = (datetime.strptime(invoice_date, '%d-%m-%Y') + timedelta(days = pay_term)).strftime('%d-%m-%Y')

        invoice_filename = f"{invoice['id']}-{invoice['currency']}"
        html_filename = f"resources/out/{invoice_filename}.html"
        with open(html_filename, mode="w", encoding="utf-8") as results:
            # merge the json objects - dictionary unpacking operator
            invoice_data = { 
                **invoice, 
                "invoice_due_date": invoice_due_date 
            }
            results.write(invoice_zoho_template.render(invoice_data))

        pdf_filename = f"resources/pdf/{invoice_filename}.pdf"
        pdfkit.from_file(html_filename, pdf_filename, options=invoice_generate_options)
        os.remove(html_filename);

def main():
    json_filename = sys.argv[1];
    payload = json.load(open(json_filename))
    generate(payload);

if __name__ == "__main__":
    main();
