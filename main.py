import errno
import os
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfReader, PdfWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject, ContentStream
import MyPdfFileWriter

def createDir():
    dirName = 'Output - ' + datetime.now().strftime('%Y-%m-%d__%H.%M.%S')
    try:
        # Create target Directory
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
    return dirName

def set_need_appearances_writer(writer: PdfWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
            })

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        #del writer._root_object["/AcroForm"]['NeedAppearances']

        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

def modifyPdf(templatePaths, outputPath, fieldDict):

    for templatePath in templatePaths:
        reader = PdfReader(open(templatePath, "rb"))
        writer = MyPdfFileWriter(PdfFileWriter())
        set_need_appearances_writer(writer)

        fields = list(reader.get_fields().keys())

        print(fields)
        fieldDict = {
            'grundstueck.strasse': 'wichtigeStrasse',
            'grundstueck.hausnummer': 'wichtigeHausnummer',
            'grundstueck.plz': 'WichtigerPLZ',
            'grundstueck.ort': 'wichtigerOrt',
            'grundstueck.ortsteil': 'wichtigerOrtsteil',
        }

        for pageNum in range(reader.numPages):
            pageObj = reader.pages[pageNum]
            writer.addPage(pageObj)
            writer.updatePageFormFieldValues(pageObj, fieldDict)
            # writer.updatePageFormFieldValues(pageObj, fieldDict)

            # writer.update_page_form_field_values(
            #     writer.pages[pageNum], fieldDict
            #         )

        # write "output" to PyPDF2-output.pdf
        with open(os.path.join(outputPath, templatePath.replace("bauantragsformulare - original/", "")), "wb") as output_stream:
            writer.write(output_stream)

if __name__ == "__main__":
    pdfTemplateFiles = [
        "bauantragsformulare - original/01.1 Bauantrag-2.pdf",
        #"bauantragsformulare - original/02.1 Baubeschreibung.pdf",
        #"bauantragsformulare - original/03.2 Betriebsbeschreibung Gewerbliche Anlagen.pdf",
        #"bauantragsformulare - original/04.5 Erkl??rung zum Brandschutznachweis.pdf",
        #"bauantragsformulare - original/08.1 Erkl??rung Tragwerksplaner.pdf",
        #"bauantragsformulare - original/08.5 Erkl??rung zum Standsicherheitsnachweis.pdf",
        #"bauantragsformulare - original/08.6 Erkl??rung zum Brandschutznachweis.pdf",
        #"bauantragsformulare - original/08.7 Erkl??rung zum Schallschutz und Ersch??tterungsschutz.pdf"
    ]

    path =  createDir()
    modifyPdf(pdfTemplateFiles, path, {})