import customtkinter as ctk
import Other.Elements as oe

def ShowMapOption():
    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    if cc['MapaKontaktow'].get() == 0 :
        cc['MapaOption'].grid_forget()
        cc['MapaCheck'].grid_forget()
        cc['MapaThreshold'].grid_forget()
    else:
        cc['MapaOption'].grid(row=24, column=0, padx=10, pady=5, sticky="w")
        cc['MapaCheck'].grid(row=0,column=0,sticky="w", padx=(10,0),pady=(0,5))
        cc['MapaThreshold'].grid(row=0,column=1,sticky="w", padx=(10,0),pady=(0,5))
