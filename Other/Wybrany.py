import Other.Shared as ots
import Other.Elements as oe
import FirstModule as fm
import os
from Other.quick_popup import quick_popup


def Wybrany():
    ots.PDBdata=""
    ots.PDBdict["Alt"] = ""
    ots.PDBdict["Braki"] = ""
    ots.PDBdict["W/J/L"] = ""

    file = oe.filename_input.get()

    if os.path.isfile(file) == False:
        quick_popup("File does not exist")
        return
    else:
        oe.wybierz_button.configure(fg_color="green")
        oe.del_button.pack_forget()
        ots.filename = file
        ots.PDBdata = fm.read_data(file)