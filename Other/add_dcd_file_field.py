import customtkinter as ctk
from Other.QuickFileSearch import QuickFileSearch
import Other.Elements as oe

def add_dcd_file_field(master_elem,plus_or_minus):
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    test_frame = ctk.CTkFrame(master=master_elem,fg_color="transparent")
    test_frame.pack(anchor="w")
    new_dcd_file_frame = ctk.CTkFrame(master=test_frame,fg_color="transparent")
    new_dcd_file_entry = ctk.CTkEntry(master=new_dcd_file_frame,width=500)
    new_dcd_file_search = ctk.CTkButton(master=new_dcd_file_frame,text="Select DCD file", command=lambda:QuickFileSearch(new_dcd_file_entry,".dcd"))
    
    new_dcd_file_entry.pack(padx=10,side="left")
    new_dcd_file_search.pack(padx=10,side="left")

    if plus_or_minus == "plus":
        plus_button = ctk.CTkButton(master=new_dcd_file_frame,text="✚",width=40,command=lambda:add_dcd_file_field(cc['DCDframe2'],"minus"))
        plus_button.pack(padx=10,side="left")
    else:
        new_dcd_file_remove = ctk.CTkButton(master=new_dcd_file_frame,text="➖",width=40,command=test_frame.destroy)
        new_dcd_file_remove.pack(padx=10,side="left")
    new_dcd_file_frame.pack(anchor="w",pady=10)
    test_frame.pack(anchor="w")