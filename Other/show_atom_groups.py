import Other.Shared as ots
import Other.Elements as oe
import customtkinter as ctk

def show_atom_group(mode):
    cc = oe.dcd_classes[oe.Currently_Displayed].dict


    if len(cc["AtomDict"][mode]) == 0:
        return 
    def del_elem(to_del,parent):

        cc["AtomDict"][mode].remove(to_del)
        parent.destroy()
        if len(cc["AtomDict"][mode]) == 0:
            if mode == "A":
                cc['Gr_show_atomsA'].configure(state="disabled")
            elif mode == "B":
                cc['Gr_show_atomsB'].configure(state="disabled")
            else:
                cc['volshow'].configure(state="disabled")
            popup.destroy()
        
    
    popup = ctk.CTkToplevel()
    popup.title("Atom group {}".format(mode))
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    Banner = ctk.CTkLabel(master = popup,anchor="w",text="Atom_name\tRes_name\tAlt_loc\tChain_id\tRes_seq_num\tInsert_code",width=600)
    Banner.pack(anchor="w",padx=10,pady=5)
    SF = ctk.CTkScrollableFrame(master=popup)
    SF.pack(fill="both",expand=True)


    for atom in cc["AtomDict"][mode]:
        Atomframe = ctk.CTkFrame(master=SF,fg_color="transparent")
        AtomLabel = ctk.CTkLabel(master=Atomframe, text=atom[1])
        AtomButton = ctk.CTkButton(
            master=Atomframe,
            text="➖",
            command=lambda to_del =atom, parent = Atomframe: del_elem(to_del,parent)
            )
        AtomLabel.pack(side="left",padx=(10,0),pady=5)
        AtomButton.pack(side="left",padx=(10,5),pady=10)
        Atomframe.pack(anchor="w",padx=0,pady=0)