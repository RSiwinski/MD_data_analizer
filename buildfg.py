import customtkinter as ctk
import Other.Elements as oe
from Other.file_input_press import file_input_press
from Other.braki import braki
from Other.SearchForFile import SearchForFile
from Other.Wybrany import Wybrany
from Other.wjl import wjl
from Other.alt import alt
from Other.del_loc import del_loc
from buildbg import buildbg
from CTkListbox import *
from Other.switch_dcd import switch_dcd
from Other.Back import Back





def buildfg(root):
    
    
    oe.tabview = ctk.CTkTabview(master=root,fg_color="transparent",border_width=1)

    oe.tabview.add("PDB Analysis")
    oe.tabview.add("DCD Analysis")




    oe.switcher_frame = ctk.CTkFrame(master=oe.tabview.tab("DCD Analysis"), fg_color="transparent")
    oe.new_sym = ctk.CTkButton(master=oe.switcher_frame,text="New Simulation", command = buildbg)
    oe.switcher = ctk.CTkComboBox(master=oe.switcher_frame,values=["Simulation no. 0"],command= lambda value:
                                  switch_dcd(value))
    
    oe.back_button = ctk.CTkButton(master=oe.switcher_frame,text="Back",command=Back)
    
    oe.superpose = ctk.CTkCheckBox(master=oe.switcher_frame,text="Superpose()")
    oe.switcher_frame.pack(fill="x",pady=0,padx=5)
    oe.switcher.pack(side="left",padx=(10,0),pady=10)
    oe.new_sym.pack(side="left",padx=10,pady=10)
    oe.superpose.pack(side="right",padx=10,pady=10)   

    oe.tabview._segmented_button.grid(row=1, column=0, sticky="w")

    oe.tabview.pack(padx=5,pady=5,fill="both",expand=True)

    oe.label = ctk.CTkLabel(master=oe.tabview.tab("PDB Analysis"), text="Select .pdb file:",font=("Arial",20))
    oe.label.grid(column=0,row=0,pady=10,padx=5,sticky="w")

    oe.filename_input = ctk.CTkEntry(master=oe.tabview.tab("PDB Analysis"),width=400)
    oe.filename_input.bind("<KeyRelease>",file_input_press)

    oe.f=ctk.CTkFrame(master=oe.tabview.tab("PDB Analysis"))

    oe.szukaj_button = ctk.CTkButton(master=oe.f,text="Search",command=SearchForFile,width=109)
    oe.wybierz_button = ctk.CTkButton(master=oe.f,text="Select",command=Wybrany,width=109,fg_color="red")

    oe.f.grid(column=1,row=1,sticky="w")

    oe.filename_input.grid(column=0,row=1,padx=(5,10),sticky="w")

    oe.szukaj_button.pack(side="left",padx=(0,5))
    oe.wybierz_button.pack(side="left",padx=(5,0))

    oe.frame = ctk.CTkFrame(master=oe.tabview.tab("PDB Analysis"),fg_color="transparent")
    oe.textbox = ctk.CTkTextbox(master=oe.tabview.tab("PDB Analysis"))

    oe.braki_button = ctk.CTkButton(master=oe.frame,text="Gaps",width=150,height=35,command=braki)
    oe.wjl_buttton = ctk.CTkButton(master=oe.frame, text="CW/I/L",width=150,height=35, command=wjl)
    oe.alt_button = ctk.CTkButton(master=oe.frame, text="Alternative",width=150,height=35, command=alt)
    oe.del_button = ctk.CTkButton(master=oe.frame,text="Select Alt Locations",width=150,height=35, command=del_loc)

    oe.braki_button.pack(pady=20)
    oe.wjl_buttton.pack(pady=20) 
    oe.alt_button.pack(pady=20) 

    oe.textbox.grid(columnspan=2,column=0,row=2,pady=(5,5),padx=(5,5),sticky="nswe")
    oe.frame.grid(column=2,row=2)
    
    oe.tabview.tab("PDB Analysis").rowconfigure(2,weight=1)
    oe.tabview.tab("PDB Analysis").columnconfigure(1,weight=1)



