#PDB  Reader
import re
import numpy as np
import math
from matplotlib.figure import Figure
import Gr
from HelperLib import Chull
import Other.Shared as ost
from DCD_reader import DCDReader
import matplotlib.ticker as ticker
from Other.quick_popup import quick_popup

# Nie czyta D:\Pliki_DCD\2__pLoxA_5ir5
# D:\Pliki_DCD\1__5kqm brak pdb

#D:\Pliki_DCD\4__MDM2:
# Atomy w pdb: 1449
# Atomy w dcd: 1449
# Num ramek w dcd: 500

#D:\Pliki_DCD\3__15LOX1_PEBP1complex_test
# Atomy w pdb: 99344
# Atomy w dcd: 99344
# Num ramek w dcd: 219



def RMSF(DCDobj: DCDReader,indexes:list,dcdfiles:list):
    num_atoms = DCDobj.PDBliczbaAtomow()
    l_indexes = len(indexes)
    avg_coords = []
    total_frames = 0
    sum_coords = [[0.0,0.0,0.0] for _ in range(l_indexes)]
    # suma coord
    for file in dcdfiles:
        DCDobj.CzytajDCD(file)
        for frame in range(DCDobj.FrameNumber()):
            total_frames +=1
            try:
                ramka = DCDobj.get__DCDframe(frame)
                ramka = [ramka[i] for i in indexes]
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            for i in range(l_indexes):
                if not ost.Pause.is_set():
                    ost.Pause.wait()
                x, y, z = ramka[i]
                sum_x, sum_y, sum_z = sum_coords[i]
                sum_coords[i] = [sum_x + x, sum_y + y, sum_z + z]
            print("Done1")
    #avg position
    for i in range(l_indexes):
        if not ost.Pause.is_set():
            ost.Pause.wait()
        sum_x, sum_y, sum_z = sum_coords[i]
        avg_coords.append([
            sum_x / total_frames,
            sum_y / total_frames,
            sum_z / total_frames
        ])

    sum_sq_fluq = [0.0] * l_indexes

    for file_data in dcdfiles:
        DCDobj.CzytajDCD(file_data)  
        for frame in range(DCDobj.FrameNumber()):
            try:
                ramka = DCDobj.get__DCDframe(frame)
                ramka = [ramka[i] for i in indexes]  
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            for i in range(l_indexes):
                if not ost.Pause.is_set():
                    ost.Pause.wait()
                x, y, z = ramka[i]
                avg_x, avg_y, avg_z = avg_coords[i]
                fluct = (x - avg_x) ** 2 + (y - avg_y) ** 2 + (z - avg_z) ** 2
                sum_sq_fluq[i] += fluct
            

    rmsf = [(val / total_frames) ** 0.5 for val in sum_sq_fluq]
    
    title="(RMSF) Root Mean Square Fluctuation"
    return [CreateFigure(
        x=np.arange(0,len(rmsf)),
        y=rmsf,
        
        xlabel="Residue Index",
        ylabel="RMSF (Å)"),(np.arange(0,len(rmsf)),rmsf),title]




def RMSD(DCDobj: DCDReader, dcdfiles: list):
    ref = []
    ref = DCDobj.ZwrocPDB()
    wynik=[]
    N = DCDobj.PDBliczbaAtomow()
    final_frame_count = 0
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        num_frames = DCDobj.FrameNumber()
        final_frame_count+=num_frames
        for frame in range(num_frames):
            if not ost.Pause.is_set():
                ost.Pause.wait()
                print("Paused")
            try:
                ramka = DCDobj.get__DCDframe(frame)
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            suma=0
            for i in range(N):              
                suma += (ramka[i][0]-ref[i][0])**2+(ramka[i][1]-ref[i][1])**2+(ramka[i][2]-ref[i][2])**2
            final = math.sqrt(suma/N)
            wynik.append(final)
    title="(RMSD) Root Mean Square Deviation"
    return [CreateFigure(
        x=np.arange(0,final_frame_count),
        y=wynik,
        xlabel="Frame Index",
        ylabel="RMSD (Å)"
    ),(np.arange(0,final_frame_count),wynik),title]

def Volume(DCDobj: DCDReader,indexes,dcdfiles):

    volumes = []
    final_frame_count=0
    
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        num_frames = DCDobj.FrameNumber()

        final_frame_count+=num_frames
        for frame in range(num_frames):
            if not ost.Pause.is_set():
                print("Paused")
                ost.Pause.wait()
            print(str(frame))
            try:
                ramka = DCDobj.get__DCDframe(frame)
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            if indexes is not None:
                ramka = [v for i, v in enumerate(ramka) if i not in set(indexes)]
            volumes.append(Chull(ramka).objetosc())

    print("DONE")
    title="Volume"
    return [CreateFigure(
        x=np.arange(0,final_frame_count),
        #x=np.arange(0,final_frame_count),
        y=volumes,
        xlabel="Frame Index",
        ylabel="Volume (Å³)"
        ),(np.arange(0,final_frame_count),volumes),title]
        


def energia_vdW(epsilon,sigma,r):
    return 4*epsilon*(math.pow(sigma/r,12)-math.pow(sigma/r,6))

def getCharges(path):
    charges=[]
    with open(path,mode="r") as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                if len(line)<=79:
                    return False
                else:
                    charge = line[79:81]
                    if line == "  ":
                        charges.append("0")
                    else:
                        charges.append(charge[1]+charge[0])
    if all(x == "" for x in charges):
        charges = False
    else:
        charges = [int(x) for x in charges]
    return charges


def BetatoRMSF(path,indexes:list):
    result = []
    idx = 0
    with open(path,mode="r") as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                if idx in indexes:
                    rmsf=math.sqrt((3*float(line[60:66].strip()))/(8*math.pow(math.pi,2)))
                    result.append(rmsf)
                idx+=1
    title = 1
    graf = None
    dims = None
    if not np.all(np.array(result) == 0):
        graf = CreateFigure(
        x=np.arange(0,len(result),1),
        y=result,
        
        xlabel="RMSF (Å)",
        ylabel="Amino Acid",
        title="(RMSF) Root Mean Square Fluctuation for atoms in a .pdb file",
        dims = (np.arange(0,len(result),1),result)
    )
      
    return [graf,dims,title]

def Energia(DCDobj : DCDReader,outfiles,args,dcdfiles, pdbfile):
    #energia_elektrostatyczna = 8.9875e9 * (q1 * q2) / (r*1e-10)
    #energia_van_der_waalsa = 4e((s/r)**12-(s/r)**6) s = (si+sj)/2 e = math.sqrt(e1*e2)
    # 8.9875e9wartość stałej Coulomba 1/4pie0 e0 8.854187817x10**-12 F/m (farad na metr)
    # 1.602e-19 to wartość ładunku elementarnego w kulombach
    #*1e-10 przeliczenie z angsztremów na metry
    Plots = []

    
    if len(outfiles) == 0:
        e = 1.602e-19
        frames_count=0
        charges = getCharges(pdbfile)
        if charges == False:
            return False
        for dcdfile in dcdfiles:
            file = DCDobj.CzytajDCD(dcdfile)
            num_frames = DCDobj.FrameNumber()
            num_atoms = DCDobj.PDBliczbaAtomow()
            frames_count+=num_frames
            Noout = []
            for frame in range(num_frames):
                if not ost.Pause.is_set():
                    ost.Pause.wait()
                try:
                    ramka = DCDobj.get__DCDframe(frame)
                except:
                    quick_popup("File is corrupted or incomplete frame")
                    return None
                energia_całkowita=0
                for i in range(num_atoms):
                    for j in range(i+1, num_atoms):
                        energia_całkowita+= 8.9875e9 * (charges[i]*e * charges[j]*e) / (np.linalg.norm(ramka[i]-ramka[j])*1e-10)
                Noout.append(energia_całkowita)
        title="Electrostatic Energy"
        Plots.append([CreateFigure(
        x=frames_count,
        y=Noout,
        ylabel="Energy (J)",
        xlabel="Frame Index"
        ),(frames_count,Noout),title])
        
    else:
        
        ELE=[]
        POT=[]
        KIN=[]
        VAN=[]
        for outfile in outfiles:
            with open(outfile,mode="r") as file:
                for line in file:
                    if line.startswith("ENERGY:"):
                        split = line.split()
                        if args[0] == 1:
                            POT.append(float(split[13]))
                        if args[1] == 1:
                            KIN.append(float(split[10]))
                        if args[2] == 1:
                            ELE.append(float(split[6]))
                        if args[3] == 1:
                            VAN.append(float(split[7])) 
        if args[0] == 1:
            title="Potential Energy"
            Plots.append([
                CreateFigure(
                    x=np.arange(0,len(POT),1),
                    y=POT,
                    ylabel="Energy (J)",
                    xlabel="Frame Index"
                ),
                (np.arange(0,len(POT),1),POT),
                title
            ])
        if args[1] == 1:
            title="Kinetic Energy"
            Plots.append([
                CreateFigure(
                    x=np.arange(0,len(KIN),1),
                    y=KIN,
                    ylabel="Energy (J)",
                    xlabel="Frame Index"
                ),
                (np.arange(0,len(KIN),1),KIN),
                title
            ])
        if args[2] == 1:
            title="Electrostatic Energy"
            Plots.append([
                CreateFigure(
                    x=np.arange(0,len(ELE),1),
                    y=ELE,
                    ylabel="Energy (J)",
                    xlabel="Frame Index"
                ),
                (np.arange(0,len(ELE),1),ELE),
                title
            ])
        if args[3] == 1:
            title="Van der Waals Energy"
            Plots.append([
                    CreateFigure(
                    x=np.arange(0,len(VAN),1),
                    y=VAN,
                    ylabel="Energy (J)",
                    xlabel="Framre Index"
                ),
                (np.arange(0,len(VAN),1),VAN),
                title
            ])


    return Plots




def Gr_ab(pdbfile,DCDobj : DCDReader,params,atom_groups,dcdfiles):

    r_values, g_r = Gr.GR(pdbfile=pdbfile,DCDobj=DCDobj,s1=atom_groups["A"],
                          s2=atom_groups["B"],nbins=params[1],r_max=params[0],dcdfiles=dcdfiles)

    title="Radial distribution function | r_max: {} | r_bins: {}".format(params[1],params[0])
    return [CreateFigure(
        x=r_values,
        y=g_r,
        xlabel="Distance (Å)",
        ylabel="G(r)"
    ),(r_values,g_r),title]





def Distance(DCDobj: DCDReader, atom1_index, atom2_index, atoms, dcdfiles):
    final_frame_count=0
    
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        num_frames = DCDobj.FrameNumber()
        final_frame_count+=num_frames
        distances = []
        for frame in range(num_frames):
            if not ost.Pause.is_set():
                ost.Pause.wait()
            try:
                ramka = DCDobj.get__DCDframe(frame)
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            x = ramka[atom2_index][0]-ramka[atom1_index][0]
            y = ramka[atom2_index][1]-ramka[atom1_index][1]
            z = ramka[atom2_index][2]-ramka[atom1_index][2]
            distance=math.sqrt(x**2+y**2+z**2)
            distances.append(distance)


    title="Distance between atoms [{} - id:{}] i [{} - id:{}]".format(atoms[0],atom1_index+1,atoms[1],atom2_index+1)  
    return [CreateFigure(
        x=np.arange(len(distances)),
        y=distances,
        xlabel="Frame Index",
        ylabel="Distance (Å)",
        disable = True
    ),(np.arange(0,final_frame_count),distances),title]

def Angle(DCDobj : DCDReader, atom1_index, atom2_index, atom3_index, atoms,dcdfiles):
    betas=[]
    final_frame_count=0
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        num_frames=DCDobj.FrameNumber()
        final_frame_count+=num_frames
        for frame in range(num_frames):
            if not ost.Pause.is_set():
                ost.Pause.wait()
            try:
                ramka = DCDobj.get__DCDframe(frame)
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            a, b, c = np.array(ramka[atom1_index]), np.array(ramka[atom2_index]), np.array(ramka[atom3_index])
            v1 = a - b
            v2 = c - b
            v1 /= np.linalg.norm(v1)
            v2 /= np.linalg.norm(v2)
            cos = np.dot(v1, v2)
            cos = np.clip(cos,-1,1)
            angle = np.degrees(np.arccos(cos))
            betas.append(angle)

    title="Angle between atoms [{} - id:{}], [{} - id:{}], [{} - id:{}]".format(atoms[0],atom1_index+1,atoms[1],atom2_index+1,atoms[2],atom3_index+1)
    return [CreateFigure(
        x=np.arange(0,final_frame_count),
        y=betas,
        xlabel="Frame Index",
        ylabel="Angle (degrees)"
    ),(np.arange(0,final_frame_count),betas),title]

def Dihedral_Angle(DCDobj : DCDReader, atom1_index, atom2_index, atom3_index,atom4_index,atoms,dcdfiles):
    angles=[]
    final_frame_count=0
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        num_frames= DCDobj.FrameNumber()
        final_frame_count+=num_frames
        angles = []
        for frame in range(num_frames):
            if not ost.Pause.is_set():
                ost.Pause.wait()
            try:
                ramka = DCDobj.get__DCDframe(frame)
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            a, b, c, d = np.array(ramka[atom1_index]), np.array(ramka[atom2_index]), np.array(ramka[atom3_index]), np.array(ramka[atom4_index]) 
            b1, b2, b3 = b-a,c-b,d-c
            n1 = np.cross(b1,b2)
            n2 = np.cross(b2,b3)
            dot_prod = np.dot(n1,n2)
            len_n1 = np.linalg.norm(n1)
            len_n2 = np.linalg.norm(n2)
            cos = dot_prod/(len_n1*len_n2)
            angle = np.degrees(np.arccos(cos))
            angles.append(angle)

    
    title = "Dihedral angle between atoms [{} - id:{}] i [{} - id:{}] i [{} - id:{}] i [{} - id:{}]".format(
        atoms[0], atom1_index+1,
        atoms[1], atom2_index+1,
        atoms[2], atom3_index+1,
        atoms[3], atom4_index+1
    )

    return [CreateFigure(
        x=np.arange(0,final_frame_count),
        y=angles,
        xlabel="Frame Index",
        ylabel="Angle (degrees)"
    ),(np.arange(0,final_frame_count),angles),title]

def getIndex(path,atom):
    index=-1
    Found = False
    with open(path,mode="r") as file:
        for line in file:
            if atom[0]==line[12:16].strip() and atom[1]==line[22:26].strip():
                Found = True
                break
            else:
                index+=1
    if Found == False:
        index = Found
    return index

import ast
def Singular_map(dcdpath : str, pdbpath: str, idxFrame: int, superpose: int, cmap: str, val: str):
    DCDobj = DCDReader(superpose)
    DCDobj.CzytajDCD(dcdpath)
    if superpose == 1:
        DCDobj.CzytajPDB(pdbpath)
    NumFrames = DCDobj.FrameNumber()
    if idxFrame > NumFrames:
        idx = NumFrames - 1
    if idxFrame < 1:
        idx = 0
    else:
        idx = idxFrame - 1
    try:
        frame = DCDobj.get__DCDframe(idx) 
    except:
        quick_popup("File is corrupted or incomplete frame")
        return None
    Frame = Euclidean_dist(frame)

    val = val.strip()
    type = "empty"

    if val == "":
        type = "float"
        val = 0.0
    elif "(" in val: 
        val = ast.literal_eval(val) 
        type = "tuple"
    else:
        type = "float"
        val = float(val)


    
    
    VMIN = 0
    VMAX = 50
    if type == "tuple":
        VMIN = int(val[0])
        VMAX = int(val[1])
        TITLE = "Frame: {}".format(idx+1)
        DRAW = Frame
    else:
        VMAX = 1
        TITLE = "Frame: {} (threshold: {})".format(idx+1,val)
        DRAW = (Frame < val).astype(int)


    FrameImage = [CreateFigure(
        x=None,
        y=DRAW,
        xlabel="Atom Index",
        ylabel="Atom Index",
        ishow=True,
        title=TITLE,
        cmap=cmap,
        vmin=VMIN,
        vmax=VMAX),
        Frame,
        "Frame"
    ]
    return FrameImage



def Euclidean_dist(frame):
    coords = np.array(frame)
    norms = np.sum(coords ** 2, axis=1).reshape(-1,1)
    K = np.dot(coords, coords.T)
    dist_squared = norms + norms.T - 2 * K 
    dist_squared = np.maximum(dist_squared,0)# ponieważ mogą by NaN przy mały wartościach
    dist = np.sqrt(dist_squared)
    return dist



def MapaKontaktow(DCDobj : DCDReader,dcdfiles,threshold):
    
    Natoms = DCDobj.DCDliczbaAtomow()
    Mat = np.zeros((Natoms,Natoms))
    MatSquare = np.zeros((Natoms,Natoms))
    FrameA = np.zeros((Natoms,Natoms))
    FrameB = np.zeros((Natoms,Natoms))
    FrameSum = 0

    # ContactMaps = []
    for dcdfile in dcdfiles:
        DCDobj.CzytajDCD(dcdfile)
        lramek = DCDobj.FrameNumber()
        FrameSum += lramek
        for i in range(lramek):
            if not ost.Pause.is_set():
                ost.Pause.wait()
            try:
                ramka = DCDobj.get__DCDframe(i) 
            except:
                quick_popup("File is corrupted or incomplete frame")
                return None
            contact_map = Euclidean_dist(ramka)

            if i == 0:
                FrameA = contact_map 
            elif i == 1:
                FrameB = contact_map 
            if threshold is not None:
                contact_map = (contact_map < threshold).astype(int)
           
            Mat += contact_map
            MatSquare += contact_map ** 2
            print(i)


    if threshold is None:
        Adraw = FrameA
        Bdraw = FrameB
    else:
        Adraw = (FrameA < threshold).astype(int)
        Bdraw = (FrameB < threshold).astype(int)


    Mean = Mat / FrameSum
    variance = MatSquare / FrameSum - Mean ** 2
    variance = np.maximum(variance,0)
    Std = variance ** 0.5

    if threshold is None:
        MAX = 50
        CMP="viridis"
        MName = "Mean distances (Å)"
        FFrame = "Contact Frame: 1"
        SFrame = "Frame: 2"
    else:
        MAX = 1 
        CMP="gray"
        MName = "Mean distances (Å) - (threshold: {})".format(threshold)
        FFrame = "Contact Frame: 1 (threshold: {})".format(threshold)
        SFrame = "Frame: 2  (threshold: {})".format(threshold)

    MeanImage = [CreateFigure(x=None,y=Mean,xlabel="Atom Index",ylabel="Atom Index",ishow=True,vmin=0,vmax=MAX,cmap=CMP),Mean,MName]

    FrameAImage = [CreateFigure(x=None,y=Adraw,xlabel="Atom Index",ylabel="Atom Index",ishow=True,title=FFrame[8:],vmin=0,vmax=MAX,cmap=CMP),FrameA,FFrame]

    FrameBImage = [CreateFigure(x=None,y=Bdraw,xlabel="Atom Index",ylabel="Atom Index",ishow=True,title=SFrame,vmin=0,vmax=MAX,cmap=CMP),FrameB,SFrame]

    StdImage = [CreateFigure(x=None,y=Std,xlabel="Atom Index",ylabel="Atom Index",ishow=True,vmin=0,vmax=MAX,cmap=CMP),Std,"Root mean square deviation (Å)"]
    

    return [FrameAImage,FrameBImage,MeanImage,StdImage]

    


def readDCD(args,add_args,superpose,pdbfile=None,dcdfiles=None,outfiles=None):
    
    Dist_ind=[]
    Ang_ind=[]
    Dang_ind=[]
    Dist_names=[]
    Ang_names=[]
    Dang_names=[]
    key_mapping={
        "dist":[2,Dist_ind,Dist_names],
        "ang1":[3,Ang_ind,Ang_names],
        "ang2":[4,Dang_ind,Dang_names]
    }
    for key in list(key_mapping.keys()):
        if key in args:
            for i in range(key_mapping[key][0]):
                key_mapping[key][1].append(add_args[key][i][1])
                key_mapping[key][2].append(add_args[key][i][0])

    if len(args) == 1 and args[0] == "energ" and  outfiles != None:
        dcdfiles = None
        pdbfile = None

    DCD_obj = DCDReader(superpose)
    if pdbfile is not None:
        try:
            DCD_obj.CzytajPDB(pdbfile)
        except:
            return 1
    if dcdfiles is not None:
        try:
            for dcdfile in dcdfiles:
                DCD_obj.CzytajDCD(dcdfile)
                if DCD_obj.PDBliczbaAtomow() != DCD_obj.DCDliczbaAtomow():
                    return 3             
        except:
            return 2
    

    wyniki=[]
    # trajectory to dcdfiles
    for arg in args:
        if arg == "rmsd":
            results = RMSD(DCD_obj,dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "rmsf":
            results = RMSF(DCD_obj,add_args["rmsf"],dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "btr":
            results = BetatoRMSF(pdbfile,add_args["btr"])
            if results is not None:
                wyniki.append(results)
        elif arg == "gr":
            results = Gr_ab(pdbfile,DCD_obj,add_args["gr"][0],add_args["gr"][1],dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "vol":
            results = Volume(DCD_obj,add_args["vol"],dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "dist":
            results = Distance(DCD_obj,Dist_ind[0],Dist_ind[1],Dist_names,dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "ang1":
            results = Angle(DCD_obj,Ang_ind[0],Ang_ind[1],Ang_ind[2],Ang_names,dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "ang2":
            results = Dihedral_Angle(DCD_obj,Dang_ind[0],Dang_ind[1],Dang_ind[2],Dang_ind[3],Dang_names,dcdfiles)
            if results is not None:
                wyniki.append(results)
        elif arg == "energ":
            energia=Energia(DCD_obj,outfiles,add_args["energ"],dcdfiles,pdbfile)
            if energia is not None:
                if energia == False:
                    wyniki.append([None,None,2])
                if len(energia) != 0:
                    for elem in energia:
                        wyniki.append(elem)
        elif arg == "mk":
            Mapy = MapaKontaktow(DCD_obj,dcdfiles,add_args["mk"])
            if Mapy is not None:
                for mapa in Mapy:
                    wyniki.append(mapa)

    return wyniki

def CreateFigure(x,y,xlabel,ylabel,ishow=False,title=None,vmin=0,vmax=50,cmap="viridis",disable=False):
    fig = Figure(figsize=(6, 4), dpi=150)
    ax = fig.add_subplot(111)
    if not ishow:
        ax.plot(x,y,color="black", linewidth=1)
        ax.grid()
        if disable:
            formatter = ticker.ScalarFormatter(useOffset=False, useMathText=False)
            formatter.set_scientific(False)
            ax.xaxis.set_major_formatter(formatter)
            ax.yaxis.set_major_formatter(formatter)
    else:
        img = ax.imshow(y, cmap=cmap, origin='lower', aspect='auto',vmin=vmin,vmax=vmax)
        fig.colorbar(img, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    fig.subplots_adjust(left=0.2)
    return fig



