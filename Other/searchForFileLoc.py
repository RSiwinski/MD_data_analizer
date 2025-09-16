import customtkinter as ctk

def serchForFileLoc(input_entry):
    dirname=ctk.filedialog.askdirectory(parent=input_entry.master)
    input_entry.delete(0,ctk.END)
    input_entry.insert(0,dirname)