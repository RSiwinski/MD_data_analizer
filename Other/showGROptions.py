import Other.Elements as oe

def showGROptions():

    
    cc = oe.dcd_classes[oe.Currently_Displayed].dict

    if cc['GRcheck'].get()==1:
        cc['GRframe'].grid(row=6, column=0, padx=10, pady=5, sticky="w")
    else:
        cc['GRframe'].grid_remove()