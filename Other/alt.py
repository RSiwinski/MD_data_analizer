
import Other.Shared as ost
import FirstModule as fm
from .fill_textbox import fill_textbox
import Other.Elements as oe

def alt():

    if ost.PDBdata == []:
        return
    if ost.PDBdict["Alt"] == "":
        ost.PDBdict["Alt"], ost.lokacje = fm.alternative_loc(ost.PDBdata)
    fill_textbox("Alt")
    if ost.PDBdict["Alt"] != "Alternative locations:\nLack of alternative locations.":
        oe.del_button.pack(pady=20)