import Other.Elements as oe
import customtkinter as ctk


def showVolumeOptions():
    cd = oe.dcd_classes[oe.Currently_Displayed].dict
    if cd['VOLcheck'].get() == 1:
        cd['VolumeAll'].grid(row=8,column=0,padx=(40,0),pady=5,sticky="w")
        cd['VolumeSome'].grid(row=9,column=0,padx=(40,0),pady=5,sticky="w")
        if cd['VolumeSome'].get()==1:
            cd['VolumeSelect'].grid(row=8,column=0,padx=(40,0),pady=5,sticky="w")

    else:
        cd['VolumeAll'].grid_forget()
        cd['VolumeSome'].grid_forget()
        cd['VolumeSelect'].grid_forget()

def SelectAll():
    cd = oe.dcd_classes[oe.Currently_Displayed].dict
    if cd['VolumeAll'].get() == 0:
        cd['VolumeAll'].configure(variable=ctk.IntVar(value=1))
    else:
        cd['VolumeSome'].configure(variable=ctk.IntVar(value=0))
        cd['VolumeSelect'].grid_forget()

def SelectSome():
    cd = oe.dcd_classes[oe.Currently_Displayed].dict
    if cd['VolumeSome'].get() == 0:
        cd['VolumeSome'].configure(variable=ctk.IntVar(value=1)) 
    else:
        cd['VolumeAll'].configure(variable=ctk.IntVar(value=0))
        cd['VolumeSelect'].grid(row=9,column=0,padx=(40,0),pady=5,sticky="w")