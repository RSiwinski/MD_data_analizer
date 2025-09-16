import customtkinter as ctk
import Other.Elements as oe
from Other.QuickFileSearch import QuickFileSearch 

def Outappend(mode):
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    outframe_inner = ctk.CTkFrame(master=cc['outframe'],fg_color="transparent")
    outentry = ctk.CTkEntry(master=outframe_inner,width=500,placeholder_text="Simulation output file (.out)")
    if mode == "plus":
        outappend = ctk.CTkButton(master=outframe_inner,text="✚",width=40,command=lambda: Outappend("minus"))
    else:
        outappend = ctk.CTkButton(master=outframe_inner,text="➖",width=40,command=outframe_inner.destroy)
    out_search = ctk.CTkButton(master=outframe_inner,text="Search",command=lambda: QuickFileSearch(outentry, ".out"),width=109)
    outentry.pack(padx=0,pady=5,side="left")
    out_search.pack(padx=(10,0),pady=5,side="left")
    outappend.pack(padx=10,side="left",pady=5)
    outframe_inner.pack(pady=5,anchor="w")