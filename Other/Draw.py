import Other.Elements as oe
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Other.Save_graph import Save_graph
from Other.Del_graph_button import Del_graph_button
import Other.Shared as ost
from SecondModule import Singular_map
from Other.Formatlist import formatlist
from Other.Del_graph_button import Del_graph_button


def render_results(wyniki,cd):
    valsA = {"max": [], "min": []}
    valsB = {"max": [], "min": []}
    Athresold, Bthresold, graf_A, graf_B, FrameASave, FrameBSave, FAText, FBText, CmapA, ClimA, CmapB, ClimB = None, None, None, None, None, None, None, None, None, None, None, None 

    def switchmap(dcdfile,pdbfile, frameidx, index, mode, threshold):
        nonlocal graf_A, graf_B, FrameASave, FrameBSave, FAText, FBText, CmapA, ClimA, CmapB, ClimB, Athresold, Bthresold
        if mode == "A":
            Cmap = CmapA.get()
            if threshold:
                Val = Athresold.get()
            else:
                Val = ClimA.get()
        else:
            Cmap = CmapB.get()
            if threshold:
                Val = Bthresold.get()
            else:
                Val = ClimB.get()
        result = Singular_map(dcdfile, pdbfile, frameidx, cc["Superpose"],Cmap, Val)
        GDC = ost.Graph_data_classes[str(oe.Currently_Displayed)]
        GDC.graphs[index] = result[0]
        GDC.graph_data[index] = result[1]
        if not GDC.graph_banners[index].startswith("Mapa"):
            GDC.graph_banners[index] = result[2]

        top10s(result[1],mode)
        if mode =="A":
            graf_A.destroy()
            graf_A = FigureCanvasTkAgg(result[0],master=cc['MapFrame']).get_tk_widget()
            graf_A.pack(padx=0,pady=5,before=FrameASave, fill="both", expand=True)
            FrameASave.configure(command=lambda:Save_graph(result[2]))
            FAText.configure(state="normal")
            FAText.delete("1.0","end")
            FAText.insert("1.0",formatlist(valsA["min"],valsA["max"],frameidx))
            FAText.configure(state="disabled")
        else:
            graf_B.destroy()
            graf_B = FigureCanvasTkAgg(result[0],master=cc['MapFrame']).get_tk_widget()
            graf_B.pack(padx=0,pady=5,before=FrameBSave, fill="both", expand=True)
            FrameBSave.configure(command=lambda:Save_graph(result[2]))
            FBText.configure(state="normal")
            FBText.delete("1.0","end")
            FBText.insert("1.0",formatlist(valsB["min"],valsB["max"],frameidx)) 
            FBText.configure(state="disabled")
        



    def top10s(matrix,mode):
        n=len(matrix[0])
        pairs=[]
        for i in range(n):
            for j in range(i+1,n):
                pairs.append((i,j,matrix[i][j]))
        pairs_sorted_asc = sorted(pairs, key=lambda x: x[2])
        number = max(1,int(len(pairs_sorted_asc)*0.1))#na wypadek 0
        if "A" == mode:
            valsA["min"] = pairs_sorted_asc[:number]
            valsA["max"] = pairs_sorted_asc[-number:][::-1]#reverse 
        elif "B" == mode:
            valsB["min"] = pairs_sorted_asc[:number]
            valsB["max"] = pairs_sorted_asc[-number:][::-1]
            


    cc = oe.dcd_classes[cd].dict
    offset = len(cc['grafy'])
    i = 0
    length = len(wyniki)
    while i < length:
        if wyniki[i][2].startswith("Contact"):
            cc["MapFrame"] = ctk.CTkFrame(master=cc['scrollable_frame'],fg_color="transparent")
            cc['grafy'].append(cc['MapFrame'])
            if "threshold" in wyniki[i][2]:
                banner_name = "Contact Map (threshold: {})".format(wyniki[i][2].split("threshold: ")[1].strip()[:-1]) 
            else:
                banner_name = "Contact Map"
            map_banner = ctk.CTkLabel(master=cc['MapFrame'],text=banner_name)
            FrameASwitchboard = ctk.CTkFrame(master=cc["MapFrame"],fg_color="transparent")
            #Check
            PDBfile = cc['banner'].cget("text").split(".pdb")[0].split("PDBfile:\t")[1] + ".pdb"
            Split = cc['banner'].cget("text").split("DCDfiles:",1)[1]
            if "OUTfiles:" in Split:
                Split = Split.split("OUTfiles:",1)[0]
            dcdfiles = [line.strip() for line in Split.splitlines() if line.strip()]
            num = len(dcdfiles)
            #
            ACheckBox = ctk.CTkComboBox(master=FrameASwitchboard,values=[str(i) for i in range(num)])
            ACheckBox.set("0")
            FrameAInput = ctk.CTkEntry(master=FrameASwitchboard)
            FrameAInput.insert(0, "1")
            CmapA = ctk.CTkEntry(master=FrameASwitchboard)
            CmapA.insert(0, "viridis")
            if "threshold" not in wyniki[i][2]:
                ClimA = ctk.CTkEntry(master=FrameASwitchboard)
                ClimA.insert(0, "(0,50)")
            else:
                Athresold = ctk.CTkEntry(master=FrameASwitchboard)
                Athresold.insert(0, wyniki[i][2].split("threshold: ")[1].strip()[:-1])
            #
            if "threshold"  in wyniki[i][2]:
                TFthreshold = True
            else:
                TFthreshold = False
            #
            FrameAButton = ctk.CTkButton(master=FrameASwitchboard,text=">",command=lambda i=i:switchmap(dcdfiles[int(ACheckBox.get())],PDBfile,int(FrameAInput.get()),i,"A", threshold=TFthreshold))
            graf_A = FigureCanvasTkAgg(wyniki[i][0],master=cc['MapFrame']).get_tk_widget()
            FrameASave = ctk.CTkButton(master=cc['MapFrame'],text="Save",command=lambda i=i:Save_graph(wyniki[i][2]))
            FrameBSwitchboard = ctk.CTkFrame(master=cc["MapFrame"],fg_color="transparent")
            BCheckBox = ctk.CTkComboBox(master=FrameBSwitchboard,values=[str(i) for i in range(num)])
            BCheckBox.set("0")
            FrameBInput = ctk.CTkEntry(master=FrameBSwitchboard)
            FrameBInput.insert(0, "2")
            CmapB = ctk.CTkEntry(master=FrameBSwitchboard)
            CmapB.insert(0, "viridis")
            if "threshold" not  in wyniki[i][2]:
                ClimB = ctk.CTkEntry(master=FrameBSwitchboard)
                ClimB.insert(0, "(0,50)")
            else:
                Bthresold = ctk.CTkEntry(master=FrameBSwitchboard)
                Bthresold.insert(0, wyniki[i+1][2].split("threshold: ")[1].strip()[:-1])
            #
            FrameBButton = ctk.CTkButton(master=FrameBSwitchboard,text=">",command=lambda i=i+1:switchmap(dcdfiles[int(BCheckBox.get())],PDBfile,int(FrameBInput.get()),i+1,"B",threshold=TFthreshold))
            graf_B = FigureCanvasTkAgg(wyniki[i+1][0],master=cc['MapFrame']).get_tk_widget()
            FrameBSave = ctk.CTkButton(master=cc['MapFrame'],text="Save",command=lambda i=i+1:Save_graph(wyniki[i][2]))
            top10s(wyniki[i][1],"A")
            top10s(wyniki[i+1][1],"B")
            TextFrame = ctk.CTkFrame(master=cc['MapFrame'],fg_color="transparent")
            FAText = ctk.CTkTextbox(master=TextFrame, width=350)
            FAText.insert("1.0", formatlist(valsA["min"],valsA["max"],int(FrameAInput.get())))
            FAText.configure(state="disabled")
            FBText = ctk.CTkTextbox(master=TextFrame, width=350)
            FBText.insert("1.0", formatlist(valsB["min"],valsB["max"],int(FrameBInput.get())))
            FBText.configure(state="disabled")
            MeanBanner = ctk.CTkLabel(master=cc['MapFrame'],text=wyniki[i+2][2])
            MeanGraf = FigureCanvasTkAgg(wyniki[i+2][0],master=cc['MapFrame']).get_tk_widget()
            mean_save = ctk.CTkButton(master=cc['MapFrame'], text="Save", command=lambda i=i: Save_graph(wyniki[i+2][2]))
            STDBanner = ctk.CTkLabel(master=cc['MapFrame'],text=wyniki[i+3][2])
            STDGraf = FigureCanvasTkAgg(wyniki[i+3][0],master=cc['MapFrame']).get_tk_widget()
            StdFrame = ctk.CTkFrame(master=cc['MapFrame'],fg_color="transparent")
            Std_save = ctk.CTkButton(master=StdFrame, text="Save", command=lambda i=i: Save_graph(wyniki[i+3][2]))
            Del_whole = ctk.CTkButton(master=StdFrame, text="Delete", command=lambda:Del_graph_button("Mapa Kontaktów",True))

            map_banner.pack(padx=5,pady=5)
            ACheckBox.pack(side="left",padx=5,pady=5)
            FrameAInput.pack(side="left",padx=5,pady=5)
            CmapA.pack(side="left",padx=5,pady=5)
            if "threshold" not in wyniki[i][2]:
                ClimA.pack(side="left",padx=5,pady=5)
            else:
                Athresold.pack(side="left",padx=5,pady=5)
            FrameAButton.pack(side="left",padx=5,pady=5)
            FrameASwitchboard.pack(fill="x",padx=0,pady=5)
            graf_A.pack(padx=0, pady=5, fill="both", expand=True)
            FrameASave.pack(anchor="w",padx=5,pady=5)
            BCheckBox.pack(side="left",padx=5,pady=5)
            FrameBInput.pack(side="left",padx=5,pady=5)
            CmapB.pack(side="left",padx=5,pady=5)
            if "threshold" not in wyniki[i][2]:
                ClimB.pack(side="left",padx=5,pady=5)
            else:
                Bthresold.pack(side="left",padx=5,pady=5)
            FrameBButton.pack(side="left",padx=5,pady=5)
            FrameBSwitchboard.pack(fill="x",padx=0,pady=5)
            graf_B.pack(padx=0, pady=5, fill="both", expand=True)
            FrameBSave.pack(anchor="w",padx=5,pady=5)
            FAText.pack(side="left",padx=5,pady=5)
            FBText.pack(side="right",padx=5,pady=5)
            TextFrame.pack(fill="x",padx=0,pady=5)
            MeanBanner.pack(padx=0,pady=5)
            MeanGraf.pack(padx=0, pady=5, fill="both", expand=True)
            mean_save.pack(anchor="w",padx=5,pady=5)
            STDBanner.pack(padx=0,pady=5)
            STDGraf.pack(padx=0, pady=5, fill="both", expand=True)
            StdFrame.pack(fill="x",padx=0,pady=5)
            Std_save.pack(side='left',padx=5,pady=5)
            Del_whole.pack(side='right',padx=5,pady=5)

            cc['MapFrame'].grid(row=(offset+i), column=0, pady=5, padx=5, sticky="nsew")
            cc['scrollable_frame'].grid_rowconfigure((offset+i), weight=1)
            
            i+=4
            continue

        graf_frame = ctk.CTkFrame(master=cc['scrollable_frame'], fg_color="transparent")
        cc['grafy'].append(graf_frame)
        graf_banner = ctk.CTkLabel(master=graf_frame, text=wyniki[i][2])

        
        graf = FigureCanvasTkAgg(wyniki[i][0], master=graf_frame).get_tk_widget()

        graf_sd = ctk.CTkFrame(master=graf_frame, fg_color="transparent")
        graf_save = ctk.CTkButton(master=graf_sd, text="Save", command=lambda i=i: Save_graph(wyniki[i][2]))
        graf_del = ctk.CTkButton(master=graf_sd, text="Delete", command=lambda i=i: Del_graph_button(wyniki[i][2]))

        graf_banner.pack(padx=5, pady=5)
        graf.pack(fill="both", expand=True, padx=0, pady=0)
        graf_sd.pack(fill="x", padx=0, pady=(5, 0))
        graf_save.pack(side="left", padx=0, pady=5)
        graf_del.pack(side="right", padx=0, pady=5)

        graf_frame.grid(row=(offset+i), column=0, pady=5, padx=5, sticky="nsew")
        cc['scrollable_frame'].grid_rowconfigure((offset+i), weight=1)
        i+=1

    cc['scrollable_frame'].grid_columnconfigure(0, weight=1)
    def resize_canvas(event):
        cc['canvas'].itemconfig(cc['scrollable_frame_id'], width=event.width)
    def update_scrollregion(event):
        cc['canvas'].config(scrollregion=cc['canvas'].bbox("all"))

    cc['scrollable_frame'].bind("<Configure>", update_scrollregion)
    cc['canvas'].bind("<Configure>", resize_canvas)

    cc['canvas'].update_idletasks()
    width = cc['canvas'].winfo_width()
    cc['canvas'].itemconfig(cc['scrollable_frame_id'], width=width)
    oe.root.bind("<MouseWheel>",lambda event: cc['canvas'].yview_scroll(-int(event.delta/120),"units"))
    

   
