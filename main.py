from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

def read_pdf(path : str) -> PdfFileReader:
    pdf_file : file = open(path, "rb")
    return PdfFileReader(pdf_file)

def extract_metadata(path : str):
    return read_pdf(path).getDocumentInfo()

def process_page_range(page_range : str) -> list:
    start_to_end_nums = page_range.replace(" ", "").split("-")
    return [int(start_to_end_nums[0]), int(start_to_end_nums[1])]

# pages[n] must take the form "start-end"
def merge_pdfs(pdf_paths : list[str], pages : list[str], pdf_name : str, author_name : str = "André A. Munduruca"):
    page_num_list = []
    pdf_list = []

    for path in pdf_paths:
        pdf_list.append(read_pdf(path))

    for numbers in pages:
        page_num_list.append(process_page_range(numbers))
    
    pdf_pages = []
    output_file : file = open(pdf_name, "wb")
    new_pdf = PdfFileWriter()

    for i in range(len(pdf_list)):
        start_num = page_num_list[i][0] - 1
        end_num = page_num_list[i][1]
        for j in range(start_num, end_num):
            new_pdf.addPage(pdf_list[i].getPage(j))
    
    new_pdf.addMetadata({"author": author_name, "title": pdf_name, "producer": "PyPDF2", "creator": "CremFuelled's PDF Editor"})
    new_pdf.write(output_file)
    output_file.close()

while True:
    print("What do you want to do with the pdf?")
    userInput = input().lower()

    if userInput == "merge":
        pdfs = []
        pages = []

        while True:
            print("Enter the path of one of the PDFs you want to merge, make sure to add them in order. When you are finished entering them, type exit.")
            pdf_location = input()
            
            if pdf_location.lower() == "exit":
                break
            else:
                try:
                    open(pdf_location, "r").close()
                except:
                    print("PDF location seems to be invalid, try again.")
                    continue

            print("Enter the pages you want from the document in the format 'start-end'.")
            page_nums = input().replace(" ", "")

            if len(page_nums.split("-")) == 2:
                pdfs.append(pdf_location)
                pages.append(page_nums)
            else: 
                print("Looks like you entered something incorrect, please reenter file path and pages.")


        print("Enter the new PDF's path and name.")
        pdf_new_name = input()

        print("Enter the name of the paper's author.")
        name_of_author = input()

        print("Merging in progress...")
        try:
            if name_of_author != "":
                merge_pdfs(pdfs, pages, pdf_new_name, name_of_author)
            else:
                merge_pdfs(pdfs, pages, pdf_new_name)
        except:
            print("Something went wrong while merging the documents, please try again and enter the info slower")
            continue

        print("Merge Successful!")

    elif userInput == "exit":
        sys.exit(1)

# TODO Finish metadata section.

    elif userInput == "metadata":
        while True:
            print("Please enter the PDF's path. Type exit if necessary.")
            pdf_location = input()

            if pdf_location.lower() == "exit":
                break
            else:
                new_metadata = {}
                old_metadata = DocumentInformation()

                try:
                    old_pdf = read_pdf(pdf_location)
                    old_metadata = old_pdf.getDocumentInfo()
                    new_pdf = PdfFileWriter().cloneDocumentFromReader(read_pdf(pdf_location))
                except:
                    print("Something went wrong opening the file, please reenter the path.")
                    continue
            
                print("Opening file was successful.", end=' ')
                

                while True:
                    print("What metadata attribute would you like to modify?")
                    attribute = input().lower()

                    print(f"What would you like the value of {attribute} to become?")
                    value = input()