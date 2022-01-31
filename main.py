from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from tkinter import *
from tkinter import ttk

TEXT_BOX_WIDTH = 40
W_HEIGHT = 450
W_WIDTH = 600
START_FILES = 5

# TODO: Make sure that we have popups for errors and such (replace print statements)
# def popup(message):

def read_pdf(path : str) -> PdfFileReader:
    try:
        pdf_file = open(path, "rb")
    except:
        print(f"{path} is not an existing PDF")
        return None
    return PdfFileReader(pdf_file)

def extract_metadata(path : str):
    pdf_file = read_pdf(path)
    if pdf_file != None:
        return pdf_file.getDocumentInfo()

def process_page_range(page_range : str) -> list:
    start_to_end_nums = page_range.replace(" ", "").split("-")
    return [int(start_to_end_nums[0]), int(start_to_end_nums[1])]

# pages[n] must take the form "start-end"
# TODO: None proofing required
def merge_pdfs(pdf_paths : list[str], pages : list[str], pdf_name : str, author_name : str = "André A. Munduruca"):
    page_num_list = []
    pdf_list = []

    for path in pdf_paths:
        pdf_list.append(read_pdf(path))

    for numbers in pages:
        page_num_list.append(process_page_range(numbers))
    
    pdf_pages = []
    new_pdf = PdfFileWriter()

    try:
        output_file = open(pdf_name, "wb")
    except:
        print("New File Location is invalid.")
        return
    
    for i in range(len(pdf_list)):
        start_num = page_num_list[i][0] - 1
        end_num = page_num_list[i][1]
        for j in range(start_num, end_num):
            new_pdf.addPage(pdf_list[i].getPage(j))
    
    new_pdf.addMetadata({"author": author_name, "title": pdf_name.removesuffix(".pdf"), "producer": "PyPDF2", "creator": "CremFuelled's PDF Editor"})
    new_pdf.write(output_file)
    output_file.close()
    
class PDF_info(ttk.Frame):
    def __init__(self, super_frame):
        ttk.Frame.__init__(self, super_frame)

        self.pages = StringVar()
        self.filepath = StringVar()

        self.file_label = ttk.Label(self, text="File:")
        self.file_label.grid(row=0, column=1, sticky=(W, ))

        self.file_entry = ttk.Entry(self, width=TEXT_BOX_WIDTH, textvariable=self.filepath)
        self.file_entry.grid(row=0, column=2, sticky=(W, E))

        self.page_label = ttk.Label(self, text="Pages:")
        self.page_label.grid(row=0, column=3, sticky=(W, E))

        self.page_entry = ttk.Entry(self, width=TEXT_BOX_WIDTH, textvariable=self.pages)
        self.page_entry.grid(row=0, column=4, sticky=(E, ))

    def get_info(self):
        return (self.file_entry.get(), self.page_entry.get())
    

class PDF_merger(ttk.Frame):


    def merge(self):
        filepathArray = []
        pagesArray = []

        new_file = self.file_entry.get()

        for info in file_list:
            if info != None:
                infoTuple = info.get_info()
                if (infoTuple[0] != "" or infoTuple[1] != ""):
                    filepathArray.append(infoTuple[0])
                    pagesArray.append(infoTuple[1])
                elif (infoTuple[0] == "" and infoTuple[1] != "") or (infoTuple[0] != "" and infoTuple[1] == ""):
                    print("Make sure both file and pages are blank or properly filled")
                    return
        
        merge_pdfs(filepathArray, pagesArray, new_file)
        print("Merge Successful")


    def __init__(self, super_frame):
        ttk.Frame.__init__(self, super_frame)

        self.file_label = ttk.Label(self, text="New File Path:")
        self.file_label.grid(row=0, column=1, sticky=(W, ))

        self.filepath = StringVar()

        self.file_entry = ttk.Entry(self, width=TEXT_BOX_WIDTH, textvariable=self.filepath)
        self.file_entry.grid(row=0, column=2, sticky=(W, E))
        
        self.button = ttk.Button(self, text="Merge!", command=self.merge)
        self.button.grid(row=0, column=3, sticky=(E, ))

root = Tk()
root.title("CremFuelled's PDF Merger")
root.geometry(f"{W_WIDTH}x{W_HEIGHT}")

main_frame = ttk.Frame(root, padding="3 3 3 3")
main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

file_list = []

temp_label = ttk.Label(main_frame, text="Here will be TABS")
temp_label.grid(row=0, column=0)

for num_rows in range(1, START_FILES+2):
    temp = PDF_info(main_frame)
    temp.grid(column=0, row=num_rows, sticky=(W, E))
    file_list.append(temp)

merger = PDF_merger(main_frame)
merger.grid(column=0, row=num_rows, sticky=(W, E, S))
num_rows += 1

# TODO: Add way to change amount of files
# TODO: Add way to modify title & author name.

root.mainloop()