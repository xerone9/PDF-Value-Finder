import PyPDF2
from PyPDF2 import PdfReader
import os.path
import logging

logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s: %(message)s')

# set location
desktop = os.path.expanduser("~\desktop\\Daily Work\\")


count = 0
value_find = False


total_files = 0
for dirpath, dirnames, filenames in os.walk(desktop):
    if value_find is False:
        for filename in [f for f in filenames if f.endswith(".pdf") or f.endswith(".PDF")]:
            pdf_file = os.path.join(dirpath, filename)
            total_files += 1
print("Total PDF FIles In Selected Location: " + str(total_files) + "\n")


#enter value to search in files
search_text = str(input("Enter Receipt No: "))

# search in files
try:
    for dirpath, dirnames, filenames in os.walk(desktop):
        if value_find is False:
            for filename in [f for f in filenames if f.endswith(".pdf") or f.endswith(".PDF")]:
                pdf_file = os.path.join(dirpath, filename)
                count += 1
                print("searching... " + str(count) + " --> " + str(pdf_file))


                reader = PdfReader(pdf_file)
                pages = reader.numPages
                extracted_text = ""
                for i in range(pages):
                    page = reader.getPage(i)
                    extracted_text += str(page.extract_text())
                    try:
                        for annot in reader.getPage(i)['/Annots']:
                            extracted_text += annot.getObject()['/Contents']
                    except:
                        # there are no annotations on this page
                        pass

                if search_text in extracted_text:
                    print(f'Found "{search_text}" in {pdf_file}')
                    os.startfile(pdf_file)
                    value_find = True
                    break
                else:
                    pass
        else:
            break
    else:
        if value_find is False:
            print(f'"{search_text}" Not Found in {str(count)} no of files')
            input("Press Enter To Exit...")
except PyPDF2.utils.PdfReadError:
    print(f'{pdf_file} is corrupted')
    logging.info(f'{pdf_file} is corrupted')
except Exception as e:
    logging.info(str(e))