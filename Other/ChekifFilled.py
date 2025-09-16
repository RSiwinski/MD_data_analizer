import Other.Shared as ost
import Other.Elements as oe
from Other.quick_popup import quick_popup
import customtkinter as ctk
import numpy as np
import os

def ChekifFilled(name):
    
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    
    if name not in ["dist","energ","ang1","ang2","gr","vol","mk","rmsf","btr"]:
        return True
      
  
    mapping  = {
        "dist" : (range(0,2),"Odległość"),
        "ang1" : (range(2,5),"Kąt"),
        "ang2" : (range(5,9),"Kąt dwuścienny")
    }

    Filled = True
    if name == "rmsf" or name == "btr":
        path = cc["pdbentry"].get().strip()
        if not os.path.exists(path):
            quick_popup("PDB file does not exist")
            return False
        else:
            if name == "rmsf":
                Dname = "RMSF"
            else: 
                Dname = "BTRMSF"
            index = 0
            result = []
            Anames = cc[Dname].replace(" ","").upper().split(",")
            if Anames == ['']:
                Anames = ["CA"]
            with open(path,"r") as file:
                for line in file:
                    if line.startswith(("ATOM","HETATM")):
                        a_name = line[12:16].strip()
                        if a_name in Anames:
                            result.append(index)
                        index += 1
            if len(result) == 0:
                quick_popup("No matching amino acids found in PDB file")
                return False
            ost.Addargs.update({name:result})
                
    if name == "mk":
        val = None
        if cc['MapaCheck'].get() == 1:
            if cc['MapaThreshold'].get() == "":
                val =  4.5
            else:
                val = float(cc['MapaThreshold'].get())
        ost.Addargs.update({"mk":val})
    if name == "vol":
        if len(cc["AtomDict"]["C"]) == 0 or cc["VolumeAll"].get() == 1:
            idx = None
        else:
            idx = [x[0] for x in cc["AtomDict"]["C"]]
        ost.Addargs.update({"vol":idx})
    if name == "gr":
        GRmax = cc['Gr_rmax_entry'].get()
        GRbin = cc['Gr_binw_entry'].get()
        if not (GRmax.replace('.','',1).isdigit() and GRbin.isdigit()):
            quick_popup("Gr_min/Gr_max/Gr_bin muszą być dodatnimi liczbami całkowitymi")
            return False
        else:
            GRmax = float(GRmax)
            GRbin = int(GRbin)
            if GRmax < 0 or GRbin<0:
                quick_popup("Wartości nie mogą być negatywne")
                return False
            if GRbin <= 0:
                quick_popup("Ilość pojemników musi być większa lub mniejsza niż 0")
                return False
            elif len(cc["AtomDict"]["A"]) == 0 or len(cc["AtomDict"]["B"]) == 0:
                quick_popup("Proszę uzupełnić dane - grupy atomów")
                return False
            else:
                
                ost.Addargs.update({"gr": [[GRmax,GRbin],{
                    "A": [sublist[0] for sublist in cc["AtomDict"]["A"]],
                    "B": [sublist[0] for sublist in cc["AtomDict"]["B"]]
                }]})
                return Filled
    if name in ["dist","ang1","ang2"]:
        Toadd = [] 
        for i in mapping[name][0]:
            text = cc['AtomLabels'][i].cget("text")[2:] 
            if text.replace(" ","") == "------":
                quick_popup("Proszę uzupełnić dane - {}".format(mapping[name][1]))
                Filled = False
                break
            Toadd.append([text[0:4].strip(),cc['AtomButtons'][i][1]])
        if Filled: ost.Addargs.update({str(name):Toadd}) 
    elif name == "energ":
        vals = []
        for widget in cc['outframe'].winfo_children():
            for inner_widget in widget.winfo_children():
                if isinstance(inner_widget,ctk.CTkEntry):
                    ost.Outputfiles.append(inner_widget.get().strip())
        if np.all(np.array(ost.Outputfiles)==""):
            if not(cc["ELE"].get()==1 and cc["pdbentry"].get().strip()==""):
                ost.Outputfiles.clear()
                quick_popup("Proszę uzupełnić plik output (.out) - Energia")
                return False
        else:
            ost.Outputfiles = [out for out in ost.Outputfiles if out != ""]
        for elem in [cc['POTcheck'],cc['KINcheck'],cc['ELEcheck'],cc['VANcheck']]:
            vals.append(elem.get())
        if sum(vals)>0:
            ost.Addargs.update({"energ":vals})
        else: 
            quick_popup("Proszę wybrać wartość do obliczenia - Energia")
    return Filled