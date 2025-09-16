import Other.Shared as ots
import FirstModule as fm
from Other.fill_textbox import fill_textbox
import Other.Elements as oe
def wjl():

    if ots.PDBdata == []:
        return
    if ots.PDBdict["W/J/L"] == "":
        ots.PDBdict["W/J/L"] = fm.hetatoms(ots.PDBdata)
    fill_textbox("W/J/L")
    oe.del_button.pack_forget()