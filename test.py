import errno
import os
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject, ContentStream

def filecreation(list, filename):
    mydir = os.path.join(
        os.getcwd(),
        "Output - " + datetime.now().strftime('%Y-%m-%d__%H:%M.%S'))
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # This was not a "directory exist" error..
    with open(os.path.join(mydir, filename), 'w') as d:
        d.writelines(list)

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


def modifyPdf(templatePath, outputfile):

    reader = PdfReader(open(templatePath, "rb"))
    writer = PdfWriter()
    set_need_appearances_writer(writer)

    page = reader.pages[0]
    fields = list(reader.get_fields().keys())

    print (page)

    content_object = page["/Contents"].getObject()
    content = ContentStream(content_object, reader)

    writer.add_page(page)

    writer.update_page_form_field_values(
        writer.pages[0], {
                fields[19]: TextStringObject("xyz")
                }
            )

    # write "output" to PyPDF2-output.pdf
    with open(outputfile, "wb") as output_stream:
        writer.write(output_stream)

if __name__ == "__main__":
    pdf_template = "bauantragsformulare - original/01.1 Bauantrag-2.pdf"
    #pdf_template = "test.pdf"
    pdf_output = "output.pdf"

    modifyPdf(pdf_template, pdf_output)
    # filecreation(["test", "test test"], pdf_output)