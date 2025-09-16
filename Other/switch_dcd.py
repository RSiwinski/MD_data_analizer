import Other.Elements as oe
import Other.Shared as ost

def switch_dcd(selected_option):

    ost.Pause.clear()
    idx = int(selected_option.split()[2])
    if idx == oe.Currently_Displayed:
        return
    cd = oe.dcd_classes[oe.Currently_Displayed].dict
    if cd["Back_packed"] and cd["Super_packed"]:
        cd["Back_frame"].pack_forget()
        cd["Super_frame"].pack_forget()
    elif cd["Super_packed"]:
        cd["Super_frame"].pack_forget()
    elif cd["Canvas_packed"]:
        cd["Canvas_frame"].pack_forget()
    elif cd["Loading_packed"]:
        ost.Loading_frame.pack_forget()


    oe.back_button.pack_forget()
    if oe.superpose_packed:
        oe.superpose.pack_forget()
        oe.superpose_packed = False

    if cd["banner"] is not None:
        cd["banner"].pack_forget()

    dcd = oe.dcd_classes[idx].dict

    if dcd["Back_packed"]:
        oe.back_button.pack(side="right", padx=10, pady=10)
        dcd["banner"].pack(anchor="w", padx=0, pady=(0, 10))
        dcd["Back_frame"].pack(fill="x", padx=0, pady=0)
        dcd["Super_frame"].pack(expand=True, fill="both", padx=0, pady=0)

    elif dcd["Super_packed"]:
        oe.superpose.pack(side="right", padx=10, pady=10)
        oe.superpose_packed = True
        dcd["Super_frame"].pack(expand=True, fill="both", padx=0, pady=0)

    elif dcd["Canvas_packed"]:
        oe.back_button.pack(side="right", padx=10, pady=10)
        dcd["banner"].pack(anchor="w", padx=0, pady=(0, 10))
        dcd["Canvas_frame"].pack(expand=True, fill="both", padx=0, pady=0)

    elif dcd["Loading_packed"]:
        dcd["banner"].pack(anchor="w", padx=0, pady=(0, 10))
        ost.Loading_frame.pack(expand=True, fill="both", padx=0, pady=0)


    oe.Currently_Displayed = idx
    oe.root.update()
    ost.Pause.set()
