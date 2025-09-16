import Other.Shared as ots
from .quick_popup import quick_popup
import os
import Other.Elements as oe
import FirstModule as fm
from Other.fill_textbox import fill_textbox

def remove_loc(path, popup):

    if path == "":
        quick_popup("No save location specified")
        return
    elif os.path.isdir(path) == False:
        quick_popup("Directory does not exist")
        return
    elif len(ots.alt_choice) == 0:
        quick_popup("No item selected")
    tab = oe.filename_input.get().split("/")

   

    
    
    ots.PDBdict["Alt"], ots.lokacje=fm.save_new(path+"/new_",oe.filename_input.get(),ots.alt_choice,ots.PDBdata, ots.lokacje)
    fill_textbox("Alt")

    popup.destroy()