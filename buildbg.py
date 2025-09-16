import customtkinter as ctk
import Other.Elements as oe
import Other.Shared as ost
from Other.QuickFileSearch import QuickFileSearch
from Other.StartAnalisis import StartAnalisis
from Other.add_dcd_file_field import add_dcd_file_field
from Other.displayLE import displayLE
from Other.select_atom import select_atom
from Other.Outappend import Outappend
from Other.show_atom_groups import show_atom_group
from Other.showGROptions import showGROptions
from Other.EnergOptions import EnergOptions
from Other.showVolumeOptions import showVolumeOptions, SelectAll, SelectSome
from Other.DCD_UI_CLASS import dcd_ui_class
import Other.Shared as ots
from Other.MapOptionShow import ShowMapOption 
from Other.AminoacidNameSelect import AmninoacidNameSelect

def buildbg():
    ost.Pause.clear()

    prev = None
    cc = dcd_ui_class()
    oe.dcd_classes.append(cc)
    cd = cc.dict 
    cd['Super_frame'] = ctk.CTkFrame(master=oe.tabview.tab("DCD Analysis"),fg_color="transparent")
    if oe.Currently_Displayed != None:
        prev = oe.Currently_Displayed
    if len(oe.dcd_classes) > 1:
        new_option = "Simulation no. {}".format((len(oe.dcd_classes)-1))
        oe.switcher.configure(values=(oe.switcher.cget("values")+[new_option]))
        oe.switcher.set(new_option)
    oe.Currently_Displayed = 0 if len(oe.dcd_classes) == 0 else len(oe.dcd_classes) - 1

    
    

    
    

    cd['DCDframe1'] = ctk.CTkFrame(master=cd['Super_frame'],fg_color="transparent")
    cd['pdbentry'] = ctk.CTkEntry(master=cd['DCDframe1'],width=500)
    cd['pdb_sbutton'] = ctk.CTkButton(master=cd['DCDframe1'],text="Select PDB file",command=lambda:QuickFileSearch(cd['pdbentry'], ".pdb"))

    cd['DCDframe2'] = ctk.CTkFrame(master=cd['Super_frame'],fg_color="transparent")

    
    cd['analisis_button'] = ctk.CTkButton(master=cd['Super_frame'],text="Analyse",command=StartAnalisis)
    

    cd['pdbentry'].pack(side="left",padx=10,pady=10)
    cd['pdb_sbutton'].pack(side="left",padx=10,pady=10)
    cd['DCDframe1'].pack(padx=5,pady=10,anchor="w")
   

    
    add_dcd_file_field(cd['DCDframe2'],"plus")
   

    cd['DCDframe2'].pack(padx=5,pady=(0,10),anchor="w")

    cd['analisis_button'].pack(padx=15,pady=(0,10),anchor="w")

    cd['OptionsFrameScroll'] = ctk.CTkScrollableFrame(master=cd['Super_frame'],fg_color="transparent")
    cd['OptionsFrameScroll'].pack(fill="both",expand=True)

    cd['outframe'] = ctk.CTkFrame(master=cd['OptionsFrameScroll'],fg_color="transparent")

    cd['RMSDcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Root Mean Square Deviation (RMSD)")
    rmsfOptions = AmninoacidNameSelect(cd['OptionsFrameScroll'],"RMSF")
    cd['RMSFcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Root Mean Square Fluctuation (RMSF)",command=lambda:(
        rmsfOptions.grid(row=2,column=0,padx=40,pady=5,sticky="w")
        if cd['RMSFcheck'].get() else rmsfOptions.grid_forget()))
    brmsfOptions = AmninoacidNameSelect(cd['OptionsFrameScroll'],"BTRMSF")
    cd['BTRMSFcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'], text="Beta to RMSF",command=lambda:(
        brmsfOptions.grid(row=4,column=0,padx=40,pady=5,sticky="w")
        if cd['BTRMSFcheck'].get() else brmsfOptions.grid_forget()))
    cd['DISTcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Distance between atoms",command=lambda:displayLE("dist"))
    cd['ANG1check'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Angle between atoms",command=lambda:displayLE("ang1"))
    cd['ANG2check'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Dihedral angle between atoms",command=lambda:displayLE("ang2"))
    cd['GRcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],command=showGROptions,text="Radial distribution function")
    cd['VOLcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Volume",command=showVolumeOptions)
    cd['ENERGYcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Energy",command=lambda:EnergOptions(cd['ENERGYcheck'].get()))
    cd['MapaKontaktow'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Contact Map",command=ShowMapOption)
    
    cd['MapaOption'] = ctk.CTkFrame(master=cd['OptionsFrameScroll'],fg_color="transparent")
    cd['MapaCheck'] = ctk.CTkCheckBox(master=cd['MapaOption'],text="Create a Contact Map with a given  threshold")
    cd['MapaThreshold'] = ctk.CTkEntry(master=cd['MapaOption'],placeholder_text="4.5")
    
    cd['ELEcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Electrostatic energy")
    cd['VANcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Van der Waals energy")
    cd['KINcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Kinetic energy")
    cd['POTcheck'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Potential energy")

    cd['VolumeAll'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Volume of all atoms", variable=ctk.IntVar(value=1), command=SelectAll)
    cd['VolumeSome'] = ctk.CTkCheckBox(master=cd['OptionsFrameScroll'],text="Select atoms to omit from volume calculation", command=SelectSome)
    cd['VolumeSelect'] = ctk.CTkFrame(master=cd['OptionsFrameScroll'],fg_color="transparent")
    cd['volshow'] = ctk.CTkButton(master=cd['VolumeSelect'],state="disabled",text="Show atoms to be omitted", command=lambda:show_atom_group("C"))
    volselect = ctk.CTkButton(master=cd['VolumeSelect'],text="Select", command=lambda:select_atom(mode="C"))

    cd['GRframe'] = ctk.CTkFrame(master=cd['OptionsFrameScroll'],fg_color="transparent")

    cd['Gr_rframe'] = ctk.CTkFrame(master=cd['GRframe'],fg_color="transparent")
    cd['Gr_rmax_label'] = ctk.CTkLabel(master=cd['Gr_rframe'],text="Max radius (Å)")
    cd['Gr_rmax_entry'] = ctk.CTkEntry(master=cd['Gr_rframe'],placeholder_text="10.0")
    cd['Gr_binw_label'] = ctk.CTkLabel(master=cd['Gr_rframe'],text="Nbins")
    cd['Gr_binw_entry'] = ctk.CTkEntry(master=cd['Gr_rframe'],placeholder_text="100")

    cd['Gr_atom_select_frame'] = ctk.CTkFrame(master=cd['GRframe'],fg_color="transparent")
    cd['Gr_show_atomsA'] = ctk.CTkButton(master=cd['Gr_atom_select_frame'],state="disabled",text="Show atoms from group A", command=lambda:show_atom_group("A"))
    cd['GR_select_atomsA'] = ctk.CTkButton(master=cd['Gr_atom_select_frame'],text="Select", command=lambda:select_atom(mode="A"))
    cd['Gr_show_atomsB'] = ctk.CTkButton(master=cd['Gr_atom_select_frame'],state="disabled",text="Show atoms from group B", command=lambda:show_atom_group("B"))
    cd['GR_select_atomsB'] = ctk.CTkButton(master=cd['Gr_atom_select_frame'],text="Select", command=lambda:select_atom(mode="B"))

    
    cd['Gr_rmax_label'].pack(side="left", padx=(10,0),pady=5)
    cd['Gr_rmax_entry'].pack(side="left", padx=(10,0),pady=5)
    cd['Gr_binw_label'].pack(side="left", padx=(20,0),pady=5)
    cd['Gr_binw_entry'].pack(side="left", padx=(10,0),pady=5)
    cd['Gr_rframe'].pack(anchor="w",padx=0,pady=10)
    cd['Gr_show_atomsA'].pack(side="left",padx=(10,0),pady=5)
    cd['GR_select_atomsA'].pack(side="left",padx=(10,0),pady=5)
    cd['volshow'].pack(side="left",padx=(10,0),pady=5)
    volselect.pack(side="left",padx=(10,0),pady=5)

    cd['Gr_show_atomsB'].pack(side="left",padx=(101,0),pady=5)
    cd['GR_select_atomsB'].pack(side="left",padx=(10,0),pady=5)
    cd['Gr_atom_select_frame'].pack(anchor="w",padx=0,pady=10)

    cd['RMSDcheck'].grid(row=0, column=0, padx=10, pady=5, sticky="w")
    cd['RMSFcheck'].grid(row=1, column=0, padx=10, pady=5, sticky="w")
    cd['BTRMSFcheck'].grid(row=3, column=0, padx=10, pady=5, sticky="w")
    cd['GRcheck'].grid(row=5, column=0, padx=10, pady=5, sticky="w")
    cd['VOLcheck'].grid(row=7, column=0, padx=10, pady=5, sticky="w")
    cd['DISTcheck'].grid(row=11, column=0, padx=10, pady=5, sticky="w")
    cd['ANG1check'].grid(row=13, column=0, padx=10, pady=5, sticky="w")
    cd['ANG2check'].grid(row=15, column=0, padx=10, pady=5, sticky="w")
    cd['ENERGYcheck'].grid(row=17, column=0, padx=10, pady=5, sticky="w")
    cd['MapaKontaktow'].grid(row=23, column=0, padx=10, pady=5, sticky="w")
    cd['MapaThreshold'].grid(row=24,column=0,padx=10,pady=5,sticky="w")
    Outappend("plus")
    

    if prev == None:
        cd['Super_frame'].pack(fill="both",expand=True)
        cd["Super_packed"] = True
    else:
        oe.back_button.pack_forget()
        if oe.dcd_classes[prev].dict['Back_packed']:
            oe.dcd_classes[prev].dict['banner'].pack_forget()
            oe.dcd_classes[prev].dict['Back_frame'].pack_forget()
            oe.dcd_classes[prev].dict['Super_frame'].pack_forget()
        elif oe.dcd_classes[prev].dict['Super_packed']:
            oe.dcd_classes[prev].dict['Super_frame'].pack_forget()
        elif oe.dcd_classes[prev].dict['Canvas_packed']:
            oe.dcd_classes[prev].dict['banner'].pack_forget()
            oe.dcd_classes[prev].dict['Canvas_frame'].pack_forget()
        elif oe.dcd_classes[prev].dict['Loading_packed']:
            oe.dcd_classes[prev].dict['banner'].pack_forget()
            ots.Loading_frame.pack_forget()
        if not oe.superpose_packed:
            oe.superpose.pack(side="right",padx=10,pady=10)  
            oe.superpose_packed = True
        cd['Super_frame'].pack(fill="both",expand=True)
        cd["Super_packed"] = True
    oe.root.update()
    ost.Pause.set()
    





