import Other.Shared as ost
import Other.Elements as oe
import FirstModule as fm
from .fill_textbox import fill_textbox

def braki():
    
    if ost.PDBdata == []:
        return
    if ost.PDBdict["Braki"] == "":
        ost.PDBdict["Braki"] = fm.missing_data(ost.PDBdata)
    fill_textbox("Braki")
    oe.del_button.pack_forget()