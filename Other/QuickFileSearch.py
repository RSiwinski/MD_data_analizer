import customtkinter as ctk

def QuickFileSearch(input_entry, filetype):
    filename=ctk.filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("Plik {}".format(filetype), filetype)
        ]
    )
    input_entry.delete(0,ctk.END)
    input_entry.insert(0,filename)
