import customtkinter as ctk
import Other.Shared as ost
from Other.searchForFileLoc import serchForFileLoc
from Other.remove_loc import remove_loc

def del_loc():
    



    dict = {}

    popup = ctk.CTkToplevel()
    popup.title("Delete Locations")
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    popup.minsize(800,500)
    label1 = ctk.CTkLabel(master=popup, text="Select a location for deletion:", font=("Arial", 14))
    scrollabel_frame = ctk.CTkScrollableFrame(master=popup,fg_color="transparent",border_width=1,border_color="gray")
    innerframe1 = ctk.CTkFrame(master=popup,fg_color="transparent")
    path_entry = ctk.CTkEntry(master=innerframe1,width=400)
    search_button = ctk.CTkButton(master=innerframe1,text="Search",command=lambda: serchForFileLoc(path_entry))
    innerframe2 = ctk.CTkFrame(master=popup,fg_color="transparent")
    delete_button = ctk.CTkButton(master=innerframe2,text="Delete", command=lambda: remove_loc(path_entry.get(),popup))
    cancel_button = ctk.CTkButton(master=innerframe2,text="Cancel",command=popup.destroy) 
    label2 = ctk.CTkLabel(popup,text="Select a save location:", font=("Arial", 14))

    for i, value in enumerate(ost.lokacje):
        option_frame = ctk.CTkFrame(master=scrollabel_frame,fg_color="transparent",border_width=1,border_color="gray")
        check_var = ctk.IntVar(value=0)
        check_mark = ctk.CTkCheckBox(master=option_frame,text="  {}".format(value),variable=check_var,command=lambda v=value: on_select(v))    
        check_mark.pack(fill="x",padx=5,pady=5)
        option_frame.pack(fill="x",padx=5,pady=5)
        dict[value] = check_var

    label1.pack(padx=20, pady=5,anchor="w")
    scrollabel_frame.pack(fill="both",expand=True,padx=20,pady=5)
    label2.pack(padx=20,pady=5,anchor="w")
    path_entry.pack(side=ctk.LEFT,padx=5,pady=5)
    search_button.pack(side=ctk.LEFT,padx=5,pady=5)
    innerframe1.pack(padx=20,pady=5,anchor="w")
    delete_button.pack(side=ctk.LEFT,padx=5,pady=5)
    cancel_button.pack(side=ctk.LEFT,padx=5,pady=5)
    innerframe2.pack(padx=20,pady=5,anchor="w")

    def on_select(value):
        if dict[value].get() == 1:
            suffix = value[-3:]
            for key, var in dict.items():
                if key != value and key.endswith(suffix):
                    var.set(0)
                    if value in ost.alt_choice:
                        ost.alt_choice.remove(key)    
            ost.alt_choice.append(value)
            
        
        