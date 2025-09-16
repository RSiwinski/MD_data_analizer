import Other.Elements as oe

def EnergOptions(mode):
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    if mode == 1:
        for ind,widget in enumerate([cc['outframe'],cc['ELEcheck'],cc['VANcheck'],cc['KINcheck'],cc['POTcheck']]):
            widget.grid(row=ind+18,column=0,padx=(40,0),pady=5,sticky="w")
        
    else:
        for widget in [cc['outframe'],cc['ELEcheck'],cc['VANcheck'],cc['KINcheck'],cc['POTcheck']]:
            widget.grid_remove()