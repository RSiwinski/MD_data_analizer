import Other.Elements as oe
import Other.Shared as ots
import customtkinter as ctk
from Other.Del_graph_button import Del_graph_button
from Other.Save_graph import Save_graph
import Other.Shared as ost

size = -1

def Back():
    global size
    cd = oe.Currently_Displayed
    elems = oe.dcd_classes[cd].dict
    


    if elems["Back_packed"]:
        elems["Back_packed"] = False
        elems["Back_frame"].pack_forget()
        elems["Super_frame"].pack_forget()
        elems["Super_packed"] = False
        elems["Canvas_frame"].pack(fill="both",expand=True,padx=0,pady=0)
        elems["Canvas_packed"] = True
        elems["Back_frame"] = None
        return
    
    tab = [["rmsd",elems['RMSDcheck']],["rmsf",elems['RMSFcheck']],["btr",elems['BTRMSFcheck']],["gr",elems['GRcheck']]
               ,["energ",elems['ENERGYcheck']],["dist",elems['DISTcheck']],["ang1",elems['ANG1check']],["ang2",elems['ANG2check']],
               ["vol",elems['VOLcheck']],["mk",elems['MapaKontaktow']]]


    banners = ots.Graph_data_classes[str(oe.Currently_Displayed)].graph_banners
    elems["Canvas_frame"].pack_forget()
    elems["Canvas_packed"] = False
    


    mapping = {
        "(RMSF) Root Mean Square Fluctuation" : [elems['RMSFcheck'],1,["rmsf",elems['RMSFcheck']]],
        "(RMSD) Root Mean Square Deviation" : [elems['RMSDcheck'],0,["rmsd",elems['RMSDcheck']]],
        "Volume" : [elems['VOLcheck'],5,["vol",elems['VOLcheck']]],
        "(RMSF) Root Mean Square Fluctuation for atoms in a .pdb file" : [elems['BTRMSFcheck'],2,["btr",elems['BTRMSFcheck']]],
        #"Contact Map" : [elems['MapaKontaktow'],18,["mk",elems['MapaKontaktow']]]
    }   

    elems["Back_frame"] = ctk.CTkFrame(master=oe.tabview.tab("DCD Analysis"),fg_color="transparent")
    size = len(banners)

    def handle_deletion(banner, lf):
        global size
        Del_graph_button(banner,multi=True)
        lf.destroy()
        mapping[banner][0].grid(row=mapping[banner][1], column=0, padx=10, pady=5, sticky="w")
        size -= 1
        tab.append(mapping[banner][2])
        ots.Addargs_pass = tab
        if size == 0:
            elems["Back_frame"].destroy()
            elems["Back_frame"] = None
            elems["Back_packed"] = False
            #DO STH
            
            

    banners_list = ["Frame","Mean","Root"]
    for banner in banners:
        if banner.startswith(tuple(banners_list)):
            continue
        label_frame = ctk.CTkFrame(master=elems["Back_frame"],fg_color="gray35",corner_radius=10)

        label = ctk.CTkLabel(master=label_frame,text=banner,fg_color="gray35",anchor="w",justify="left")
        del_button = ctk.CTkButton(master=label_frame,text="Delete",command = lambda banner = banner, lf = label_frame: handle_deletion(banner, lf))
        
        label.pack(side="left",padx=10,pady=5)
        del_button.pack(side="right",padx=5,pady=5)
        if not banner.startswith("Contact"):
            save_button = ctk.CTkButton(master=label_frame,text="Save", command= lambda banner = banner: Save_graph(banner))
            save_button.pack(side="right",padx=5,pady=5)
        label_frame.pack(fill="x",expand=False,padx=5,pady=5)
        if banner in mapping.keys():
            tab.remove(mapping[banner][2])
    ots.Addargs_pass = tab

    elems["DCDframe1"].pack_forget()
    elems["DCDframe2"].pack_forget()

    keys = list(mapping.keys())
    for banner in banners:
        if banner in keys:
            mapping[banner][0].grid_forget()


    


  
    elems["Back_frame"].pack(fill="x",padx=0,pady=0)
    elems["Super_frame"].pack(fill="both",expand=True,padx=0,pady=(5,0))
    elems["Super_packed"] = True



        
    elems["Back_packed"] = True
