import Other.Elements as oe
import Other.Shared as ost
import tkinter.filedialog as fd
import os
import numpy as np

def Save_graph(title):
    cc = ost.Graph_data_classes[str(oe.Currently_Displayed)]
    index = cc.graph_banners.index(title)
    
    file_path = ""
    file_path = fd.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("Wszystkie pliki", "*.*")],
        title="Save graph as..."
    )
    if file_path == "":
        return
    base, _ = os.path.splitext(file_path)
    text_path = base + ".dat"
    cc.graphs[index].savefig(file_path, dpi=300, bbox_inches='tight')
    # Dla map
    if title.startswith(tuple(["Frame","Mean","Root","Contact"])):
        np.savetxt(text_path,cc.graph_data[index],fmt="%.6f")
        return
    # 
    text_path = base + ".txt"
    with open(text_path, "w", encoding="utf-8") as file:
        file.write("PDBfile (.pdb)\n")
        file.write(cc.pdbfile+"\n")
        file.write("DCDfile/s (.dcd)\n")
        if len(cc.dcdfiles) == 0:
            file.write("-\n")
        else:
            for dcdfile in cc.dcdfiles:
                file.write(dcdfile+"\n")
        file.write("Outputfile/s (.out)\n")
        if len(cc.outputfiles) == 0:
            file.write("-\n")
        else:
            for outfile in cc.outputfiles:
                file.write(outfile+"\n")
        file.write(cc.graph_banners[index]+"\n")
        file.write("x\t:\ty\n")
        x , y = cc.graph_data[index][0],cc.graph_data[index][1]
        for i in range(len(x)):
            file.write("{}\t:\t{}\n".format(x[i],y[i]))
    