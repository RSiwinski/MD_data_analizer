import customtkinter as ctk
import Other.Elements as oe

    

def AmninoacidNameSelect(root,name):
    ramka = ctk.CTkFrame(master=root,fg_color="transparent")
    label = ctk.CTkLabel(master=ramka,text="Enter amino acid name(s) [CA, ... ]")
    StrVar = ctk.StringVar()
    StrVar.trace_add("write", lambda *_: on_change(StrVar, name))
    entry = ctk.CTkEntry(master=ramka,width=300,textvariable=StrVar)
    label.grid(row=0,column=0,padx=0,pady=5,sticky="w")
    entry.grid(row=0,column=1,padx=10,pady=5,sticky="w")
    return ramka

def on_change(var, name, *args):
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    cc[name]=var.get()



    