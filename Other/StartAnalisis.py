import Other.Shared as ots
import Other.Elements as oe
import customtkinter as ctk
import os
from Other.quick_popup import quick_popup
from Other.Graph_data import Graph_data
from Other.ChekifFilled import ChekifFilled
import SecondModule as sm
from builder import Builder
from Other.DCD_condition import check_array
from Other.Draw import render_results
import queue




def StartAnalisis():
    
    cd = oe.Currently_Displayed
    cc = oe.dcd_classes[cd].dict
    cc["Superpose"] = oe.superpose.get()  
    #, root 
    TABCHECKS=[["rmsd",cc['RMSDcheck']],["rmsf",cc['RMSFcheck']],["btr",cc['BTRMSFcheck']],["gr",cc['GRcheck']]
               ,["energ",cc['ENERGYcheck']],["dist",cc['DISTcheck']],["ang1",cc['ANG1check']],["ang2",cc['ANG2check']],
               ["vol",cc['VOLcheck']],["mk",cc['MapaKontaktow']]]

    ots.Addargs.clear()
    pdbfile = cc['pdbentry'].get().replace("/","\\")

    dcdfiles = []
    for frame in cc['DCDframe2'].winfo_children():
        for innerframe in frame.winfo_children():
            for widget in innerframe.winfo_children():
                if isinstance(widget,ctk.CTkEntry):
                    dcdfiles.append(widget.get().replace("/","\\"))

    if cc["Back_packed"]:
       cc["banner"].pack_forget()
       cc['Back_frame'].pack_forget()
       TABCHECKS = ots.Addargs_pass 

    args = []
    for elem in TABCHECKS:
        if elem[1].get()==1:
            args.append(elem[0])
            if ChekifFilled(elem[0]) == False:
                return
    if len(args) == 0:
        quick_popup("Nie wybrano wartości do obliczenia")
        return

    if not(len(args) == 1 and args[0] == "energ"):

        if check_array(args,ots.Addargs,"pdb"):
            _, pext = os.path.splitext(pdbfile)
            
            if pdbfile == "":
                quick_popup("Proszę uzupełnić dane PDB")
                return
            if pext != ".pdb":
                quick_popup("Niezgodne rozszerzenie pliku PDB")
                return
            if not os.path.isfile(pdbfile):
                quick_popup("Nie ma takiego pliku:\n" + pdbfile)
                return

        if check_array(args,ots.Addargs,"dcd"):
            dcd_exts = [os.path.splitext(f)[1] for f in dcdfiles]
            
            if any(file == "" for file in dcdfiles):    
                quick_popup("Proszę uzupełnić dane DCD")
                return
            if any(ext != ".dcd" for ext in dcd_exts):
                quick_popup("Niezgodne rozszerzenie pliku DCD")
                return
            err_msg = "\n".join(file for file in dcdfiles if not os.path.isfile(file))
            if err_msg:
                quick_popup(f"Nie znaleziono pliku/ów:\n{err_msg}")
                return
        
        dcdfiles = [dcd for dcd in dcdfiles if dcd != ""]
    
    gd = Graph_data(
        pdbfile = pdbfile,
        dcdfiles = dcdfiles,
        outputfiles = ots.Outputfiles,
    )

    dcdtext = "PDBfile:\t{}\n".format(pdbfile) 
    if len(dcdfiles) > 0:
        dcdtext = dcdtext + f"DCDfiles:" +"\n".join(f"\t{dcdfile}" for dcdfile in dcdfiles)
    if len(ots.Outputfiles) > 0:
        dcdtext = dcdtext + f"\nOUTfiles:" + "\n".join(f"\t{outfile}" for outfile in ots.Outputfiles)

    cc["Super_frame"].pack_forget()
    cc["Super_packed"] = False
    
    oe.superpose.pack_forget()
    oe.superpose_packed = False
    
    cc['banner'] = ctk.CTkLabel(master=oe.tabview.tab("DCD Analysis"),text=dcdtext, fg_color="transparent",anchor="w",justify="left")
    cc['banner'].pack(anchor="w",padx=0,pady=(0,10))
    

    
    ots.Loading_frame.pack(expand=True,padx=0,pady=0,fill="both")
    cc["Loading_packed"] = True
    oe.root.update()

    result_queue = queue.Queue()
    
    #TODO for now
    def check_result():
        try: 
        
            wyniki = result_queue.get_nowait()
            
          
            error = False
            if wyniki == 1:
                error = True
                quick_popup("Failed to load the .pdb file")
            elif wyniki == 2:
                error = True
                quick_popup("Failed to load the .dcd file")
            elif wyniki == 3:
                error = True
                quick_popup("The number of atoms in the .pdb and .dcd files does not match.")
            if error:
                cc["Loading_packed"] = False
                cc["banner"].pack_forget()
                ots.Loading_frame.pack_forget()
                cc["Super_packed"] = True
                if cd == oe.Currently_Displayed:
                    cc["Super_frame"].pack(fill="both",expand=True,padx=0,pady=0) 
                return
            error_text = "Simulation no. {}:\n".format(cd)
            for wynik in wyniki[:]:
                if wynik[2] == 1:
                    error_text += "All B-factor values in the .pdb file are equal to zero\n"
                    wyniki.remove(wynik)
                elif wynik[2] == 2:
                    error_text += "Energy was not calculated because the .pdb file does not contain information about electric charges\n"
                    wyniki.remove(wynik)
            

            



            cc["Loading_packed"] = False
            ots.Loading_frame.pack_forget()

            if len(wyniki) == 0 and cc["Canvas_frame"] is None:
                quick_popup(error_text)
                cc["banner"].pack_forget()
                cc["banner"].destroy()
                cc["Super_frame"].pack(fill="both",expand=True,padx=0,pady=0)
                cc["Super_packed"] = True
                oe.superpose.pack(side="right",padx=10,pady=10)   
                return
                

            oe.back_button.pack(side="right",padx=10,pady=10)
            cc["Back_packed"] = False

            
            if cc["Canvas_frame"] == None:
                gd.graphs = [x[0] for x in wyniki]
                gd.graph_data = [x[1] for x in wyniki]
                gd.graph_banners = [x[2] for x in wyniki]
                ots.Graph_data_classes[str(oe.Currently_Displayed)] = gd
                cc["Canvas_frame"] = ctk.CTkFrame(master=oe.tabview.tab("DCD Analysis"),bg_color="transparent")
                cc["Canvas_packed"] = True
                
                cc['canvas'] = ctk.CTkCanvas(master=cc['Canvas_frame'],bg="gray10",highlightthickness=0
                )
                cc['canvas'].pack(side="left", fill="both", expand=True)
                cc['scrollbar'] = ctk.CTkScrollbar(master=cc['Canvas_frame'],orientation="vertical",command=cc['canvas'].yview)
                cc['scrollbar'].pack(side="right", fill="y")
                cc['canvas'].configure(yscrollcommand=cc['scrollbar'].set)
                cc['scrollable_frame'] = ctk.CTkFrame(master=cc['canvas'],fg_color="transparent")
                cc['scrollable_frame_id'] = cc['canvas'].create_window((0, 0), window=cc['scrollable_frame'], anchor="n")
                cc['grafy'] = []
            else:
                ots.Graph_data_classes[str(oe.Currently_Displayed)].graphs +=  [x[0] for x in wyniki]
                ots.Graph_data_classes[str(oe.Currently_Displayed)].graph_data += [x[1] for x in wyniki]
                ots.Graph_data_classes[str(oe.Currently_Displayed)].graph_banners += [x[2] for x in wyniki]
            if cd == oe.Currently_Displayed:
                cc["Canvas_frame"].pack(fill="both",expand=True,padx=0,pady=0) 
        
            render_results(wyniki,cd)
            
        except queue.Empty:
            oe.root.after(100,check_result)
    
    Builder(function=sm.readDCD,result_queue=result_queue,args={
        "pdbfile":pdbfile,
        "dcdfiles":dcdfiles,
        "args":args,
        "add_args":ots.Addargs,
        "outfiles":ots.Outputfiles,
        "superpose":oe.superpose.get()    
    })
    oe.root.after(100,check_result)
    


    return