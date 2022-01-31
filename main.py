from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from tkinter import *
from tkinter import ttk

TEXT_BOX_WIDTH = 40
W_HEIGHT = 450
W_WIDTH = 600
START_FILES = 5

# TODO: MAKE CODE MORE STABLE

def popup(message):
    smol_window = Toplevel()
    popup_frame = ttk.Frame(smol_window, padding="2 2 2 2")
    popup_frame.grid(row=0, column=0, sticky=(N, S, E, W))

    popup_message = ttk.Label(popup_frame, text=message)
    popup_message.grid(row=0, column=0, sticky=(E, W, N))

    ok_button = ttk.Button(popup_frame, text="Ok", command=smol_window.destroy)
    ok_button.grid(row=1, column=0, sticky=(E, W, S))

    

def read_pdf(path : str) -> PdfFileReader:
    try:
        pdf_file = open(path, "rb")
    except:
        popup(f"{path} is not an existing PDF")
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
        popup("New File Location is invalid.")
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

        author_name = self.author_entry.get()
        new_file = self.file_entry.get()

        for info in file_list:
            if info != None:
                infoTuple = info.get_info()
                if (infoTuple[0] != "" and infoTuple[1] != ""):
                    filepathArray.append(infoTuple[0])
                    pagesArray.append(infoTuple[1])
                elif (infoTuple[0] == "" and infoTuple[1] != "") or (infoTuple[0] != "" and infoTuple[1] == ""):
                    popup("Make sure both file and pages are blank or properly filled")
                    return
        if author_name != "":
            merge_pdfs(filepathArray, pagesArray, new_file, author_name)
        else:
            merge_pdfs(filepathArray, pagesArray, new_file)
        popup("Merge Successful")

    # TODO: FIX THIS IS BROKEN
    def add_files(self, event):
        for i in range(int(self.num_entry.get()) - len(file_list)):
            temp_file = PDF_info(main_frame)
            temp_file.grid(row=num_rows, column=0, sticky=(E, W))
            file_list.append(temp_file)

    def __init__(self, super_frame):
        ttk.Frame.__init__(self, super_frame)

        self.file_label = ttk.Label(self, text="New File Path:")
        self.file_label.grid(row=0, column=1, sticky=(W, ))

        self.filepath = StringVar()

        self.file_entry = ttk.Entry(self, width=TEXT_BOX_WIDTH, textvariable=self.filepath)
        self.file_entry.grid(row=0, column=2, sticky=(W, E))
        
        self.button = ttk.Button(self, text="Merge!", command=self.merge)
        self.button.grid(row=0, column=3, sticky=(E, ))

        self.num_of_files = StringVar()
        self.num_of_files.set(START_FILES)

        self.num_label = ttk.Label(self, text="Number of files:")
        self.num_label.grid(row=1, column=3, sticky=(E, W))

        self.num_entry = ttk.Entry(self, width=5, textvariable=self.num_of_files)
        self.num_entry.grid(row=1, column=4, sticky=(E, ))
        self.num_entry.bind("<Return>", self.add_files)

        self.author_label = ttk.Label(self, text="Author Name:")
        self.author_label.grid(row=1, column=1, sticky=(W, ))

        self.author = StringVar()

        self.author_entry = ttk.Entry(self, width=TEXT_BOX_WIDTH, textvariable=self.author)
        self.author_entry.grid(row=1, column=2, sticky=(E, W))

root = Tk()
root.title("CremFuelled's PDF Merger")
root.geometry(f"{W_WIDTH}x{W_HEIGHT}")

main_frame = ttk.Frame(root, padding="3 3 3 3")
main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

# TODO: TABS
temp_label = ttk.Label(main_frame, text="Here will be TABS")
temp_label.grid(row=0, column=0)

merger = PDF_merger(main_frame)
merger.grid(column=0, row=1, sticky=(W, E, S))

file_list = []


for num_rows in range(2, START_FILES+2):
    temp = PDF_info(main_frame)
    temp.grid(column=0, row=num_rows, sticky=(W, E))
    file_list.append(temp)

num_rows += 1

# TODO: Add way to change amount of files
# TODO: Add way to modify title & author name.

root.mainloop()