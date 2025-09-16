import Other.Elements as oe
import os
import customtkinter as ctk
import Other.OptionSearchPDB as osp
import Other.Autofill as au
from Other.validate_chain_id import validate_chain_id
from Other.quick_popup import quick_popup
import Other.Shared as ots

def select_atom(mode=None,variant=None):
    
    cc = oe.dcd_classes[oe.Currently_Displayed].dict

    pdbfile = cc['pdbentry'].get().strip()
    if not os.path.isfile(pdbfile):
        quick_popup("Please provide a valid PDB file")
        return
    popup = ctk.CTkToplevel()
    if mode == "C":
        popup.title("Select atoms to omit from volume calculation")
    else:
        popup.title("Select atoms for group {}".format(mode))
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    options = osp.OptSearchPDB(pdbfile)
    filters = {
    "name":         (None, slice(12, 16)),    # Atom name
    "res_name":     (None, slice(17,20)),     # Residue name                   
    "res_seq_num":  (None, slice(22, 26)),    # Residue sequence number
    "insert_code":  (None, 26),               # Insertion code
    "alt_loc":      (None, 16),               # Alternate location
    "chain_id":     (None, 21)                # Chain ID
    }
    AFobj=au.AutoFillBox(options["names"],popup,1)
    Name=AFobj.create()
    Name.pack(fill="x",expand=True,padx=10,pady=5)
    AFobj2=au.AutoFillBox(options["res_names"],popup,2)
    Res_name=AFobj2.create()
    Res_name.pack(fill="x",expand=True,padx=10,pady=5)
    RSframe = ctk.CTkFrame(master=popup,fg_color="transparent")
    RSlabel = ctk.CTkLabel(master=RSframe,text="Residue number {}-{}".format(str(options["Res_seq_num"]["min"]),str(options["Res_seq_num"]["max"])))
    RS_entry_var = ctk.StringVar()
    RSentry = ctk.CTkEntry(master=RSframe,textvariable=RS_entry_var)
    RS_entry_var.trace_add("write",lambda *args:validate_chain_id(RS_entry_var,RSentry,options["Res_seq_num"]["min"],options["Res_seq_num"]["max"],*args))
    RSlabel.pack(side="left", padx =(10,0),pady=5)
    RSentry.pack(side="left", padx =(10,0),pady=5)
    RSframe.pack(anchor="w",pady=5)

    CIframe = ctk.CTkFrame(master=popup,fg_color="transparent")
    CIlabel = ctk.CTkLabel(master=CIframe,text="Chain ID")
    CIvar = ctk.StringVar(value=options["chain_id"][0])
    CIChoice = ctk.CTkOptionMenu(master=CIframe,values=options["chain_id"],variable=CIvar)
    CIlabel.pack(side="left", padx =(10,0),pady=5)
    CIChoice.pack(side="left", padx =(10,0),pady=5)
    CIframe.pack(anchor="w",pady=5)

    if len(options["alt_loc"]) > 0:
        ALframe = ctk.CTkFrame(master=popup,fg="transparent")
        ALlabel = ctk.CTkLabel(master=ALframe,text="Alternative Location")
        ALvar=ctk.StringVar(value=options["alt_loc"][0])
        ALChoice = ctk.CTkOptionMenu(master=ALframe,values=options["alt_loc"],variable=ALvar) 
        ALlabel.pack(side="left", padx =(10,0),pady=5)
        ALChoice.pack(side="left", padx =(10,0),pady=5)
        ALframe.pack(anchor="w",pady=5)
    
    if len(options["insert_code"]) > 0:
        ICframe = ctk.CTkFrame(master=popup,fg="transparent")
        IClabel = ctk.CTkLabel(master=ALframe,text="Insert Code")
        ICvar = ctk.StringVar(value=options["insert_code"][0])
        ICChoice = ctk.CTkOptionMenu(master=ALframe,values=options["insert_code"],variable=ICvar) 
        IClabel.pack(side="left", padx =(10,0),pady=5)
        ICChoice.pack(side="left", padx =(10,0),pady=5)
        ICframe.pack(anchor="w",pady=5)

    
    def searchPDB():
        AFtext = AFobj.Entry().get().upper()
        if AFtext == AFobj.suggest().cget("text"):
            filters["name"] = (AFtext,filters["name"][1])
        AFtext2 = AFobj2.Entry().get().upper()
        if AFtext2 == AFobj2.suggest().cget("text"):
            filters["res_name"] = (AFtext2,filters["res_name"][1])
        if RSentry.cget("fg_color") != "red" and RSentry.get() != "":
            filters["res_seq_num"] = (RSentry.get(),filters["res_seq_num"][1])
        filters["chain_id"] = (CIChoice.get(),filters["chain_id"][1])
        if len(options["alt_loc"]) > 0:
            filters["alt_loc"]= (ALChoice.get(),filters["alt_loc"][1])
        if len(options["insert_code"]) > 0:
            filters["insert_code"] = (ICChoice.get(),filters["insert_code"][1])

        wymagane = ["name", "res_seq_num", "res_name"]
        if variant is not None:
            if any(filters[pole][0] is None for pole in wymagane):
                quick_popup("Please fill in all fields")
                return
        elif all(filters[field][0] is None for field in wymagane):
            quick_popup("Please fill in the required fields")
            return

        line_count=0
        added = False
        with open(pdbfile, "r") as file:
            for line in file:
                if line.startswith(("ATOM","HETATM")):
                    # filtrowanie
                    match = True
                    for value in filters.values():
                        if value[0] is None: continue
                        if line[value[1]].strip() != value[0]:
                            match = False
                            break
                            
                    if match:
                        added=True
                        string = "{:<10}\t\t{:<10}\t\t{:<8}\t{:<10}\t{:<14}\t\t{:<12}\t".format(
                                line[12:16].strip(),#name
                                line[17:20].strip(),#res_name
                                "_" if line[16] == " " else line[16],#alt_loc
                                line[21],#chaid_id
                                line[22:26].strip(),#res_seq_num
                                "_" if line[26] == " " else line[26])#insert code
                        if variant is not None:
                            oe.dcd_classes[oe.Currently_Displayed].dict['AtomButtons'][variant].append(line_count)
                            oe.dcd_classes[oe.Currently_Displayed].dict['AtomLabels'][variant].configure(text="{}:\t{}".format(variant+1,string))
                            popup.destroy()
                            return
                        
                        entry = [line_count,string]
                        if entry not in oe.dcd_classes[oe.Currently_Displayed].dict["AtomDict"][mode]:
                            oe.dcd_classes[oe.Currently_Displayed].dict["AtomDict"][mode].append(entry)

                        

                    line_count+=1
        if added:
            if mode == "A":
                cc['Gr_show_atomsA'].configure(state="normal")
            elif mode == "B":
                cc['Gr_show_atomsB'].configure(state="normal")
            else:
                cc['volshow'].configure(state="normal")
        else:
            for key, value in filters.items(): filters[key] = (None,value[1])
            quick_popup("Brak wyników")
            return
        popup.destroy()



    close_button = ctk.CTkButton(popup, text="OK", command=searchPDB)
    close_button.pack(pady=10)

    
    

   
