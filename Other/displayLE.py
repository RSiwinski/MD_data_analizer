import Other.Shared as ost
import Other.Elements as oe
from Other.createLEArrays import createLEArrays

def displayLE(mode):

    cc = oe.dcd_classes[oe.Currently_Displayed].dict
    if len(cc['AtomLEFrames']) == 0:
        createLEArrays()
    mode_mapping = {
        "dist": (cc['DISTcheck'], 0, 12),
        "ang1": (cc['ANG1check'], 1, 14),
        "ang2": (cc['ANG2check'], 2, 16),
    }
    if mode_mapping[mode][0].get()==1:
        cc['AtomLEFrames'][mode_mapping[mode][1]].grid( row=mode_mapping[mode][2],column=0,sticky="w",padx=0,pady=5)
    else:
        cc['AtomLEFrames'][mode_mapping[mode][1]].grid_forget()