import Other.Shared as ost
import Other.Elements as oe

def Del_graph_button(title,multi=False):
    GDC = ost.Graph_data_classes[str(oe.Currently_Displayed)]
    idx = GDC.graph_banners.index(title)
    if multi:
        del GDC.graphs[idx:idx+4]
        del GDC.graph_data[idx:idx+4]
        del GDC.graph_banners[idx:idx+4]
    else:
        GDC.graphs.pop(idx)
        GDC.graph_data.pop(idx)
        GDC.graph_banners.pop(idx)
    if multi:
        oe.dcd_classes[oe.Currently_Displayed].dict["MapFrame"] = None
    elem = oe.dcd_classes[oe.Currently_Displayed].dict['grafy'].pop(idx)
    elem.destroy()
    canv = oe.dcd_classes[oe.Currently_Displayed].dict['canvas']
    canv.update_idletasks()
    canv.configure(scrollregion=canv.bbox("all"))

