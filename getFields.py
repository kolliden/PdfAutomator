import errno
import os
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject, ContentStream

def modifyPdf(templatePaths):

    for templatePath in templatePaths:
        reader = PdfReader(open(templatePath, "rb"))
        writer = PdfWriter()

        fields = list(reader.get_fields().keys())
        fields = reader.get_fields()
        # print("\n" + templatePath + ": \n")
        print(fields)

if __name__ == "__main__":
    pdfTemplateFiles = [
        #"bauantragsformulare - original/01.1 Bauantrag-2.pdf",
         "bauantragsformulare - original/02.1 Baubeschreibung.pdf",
        # "bauantragsformulare - original/03.2 Betriebsbeschreibung Gewerbliche Anlagen.pdf",
        # "bauantragsformulare - original/04.5 Erklärung zum Brandschutznachweis.pdf",
        # "bauantragsformulare - original/08.1 Erklärung Tragwerksplaner.pdf",
        # "bauantragsformulare - original/08.5 Erklärung zum Standsicherheitsnachweis.pdf",
        # "bauantragsformulare - original/08.6 Erklärung zum Brandschutznachweis.pdf",
        # "bauantragsformulare - original/08.7 Erklärung zum Schallschutz und Erschütterungsschutz.pdf"
    ]

    # path =  createDir()
    modifyPdf(pdfTemplateFiles)