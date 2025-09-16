import Other.Shared as ost
import customtkinter as ctk
import Other.Elements as oe
from Other.select_atom import select_atom

def createLEArrays():

    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    def filtr(num,mode=None):
        if num in range(0,2):
            if mode ==1:
                return 0
            return num+1
        if num in range(2,5):
            if mode ==1:
                return 1
            return num-1
        else:
            if mode ==1:
                return 2
            return num-4

    for i in range(3):
        cc["AtomLEFrames"].append(ctk.CTkFrame(master=cc['OptionsFrameScroll'],fg_color="transparent"))
        Banner = ctk.CTkLabel(master=cc["AtomLEFrames"][i],text="\tAtom_name\tRes_name\tAlt_loc\tChain_id\tRes_seq_num\tInsert_code")
        Banner.pack(padx=10,pady=5,anchor="w")

    for i in range(9):
        cc["Innerframes"].append(ctk.CTkFrame(master=cc["AtomLEFrames"][filtr(i,1)],fg_color="transparent"))
        cc["AtomLabels"].append(ctk.CTkLabel(master=cc["Innerframes"][i],text="{}:\t{:<10}\t\t{:<10}\t\t{:<8}\t{:<10}\t{:<14}\t\t{:<12}\t".format(filtr(i),"-","-","-","-","-","-")))
        cc['AtomButtons'].append([ctk.CTkButton(master=cc['Innerframes'][i],text="Search",command=lambda v=i:select_atom(variant=v))])
        cc['AtomLabels'][i].pack(padx=(10,5),pady=5,side="left")  
        cc['AtomButtons'][i][0].pack(padx=(50,5),pady=5,side="right")
        cc['Innerframes'][i].pack(fill="x",expand=True,padx=0,pady=5)