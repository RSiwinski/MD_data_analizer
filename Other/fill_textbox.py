import customtkinter as ctk
import Other.Elements as oe
import Other.Shared as ost

def fill_textbox(name):
    oe.textbox.delete(1.0,ctk.END)
    oe.textbox.insert(1.0,ost.PDBdict[name])
    oe.textbox.insert(1.0,"FILE: "+oe.filename_input.get()+"\n")