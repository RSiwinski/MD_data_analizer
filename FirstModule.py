import numpy as np
import Bio 
from Bio.PDB import *
import os
import re
from itertools import takewhile


#entity = PDBList()
#entity.retrieve_pdb_file(pdb_code="1BEH",pdir="D:\Magisterka\plikiPDB",file_format="pdb")


nazwy = {"CYS":"C","ASP":"D","SER":"S","GLN":"Q","LYS":"K","ILE":"I","PRO":"P","THR":"T","PHE":"F","ASN":"N",
         "GLY":"G","HIS":"H","LEU":"L","ARG":"R","TRP":"W","ALA":"A","VSL":"V","GLU":"E","TYR":"Y","MET":"M"}

#chem = [ H, LI, BE, NA, MG, K, CA, RB, SR, CS, BA, FR, RA, SC, TI, V, CR, MN, FE, CO, NI, CU, ZN, Y, ZR, NB, MO,
#        TC, RU, RH, PD, AG, CD, LA, HF, TA, W, RE, OS, IR, PT, AU, HG, O, S, SE, TE, PO, F, CL, BR, I, AT]

# def outputPath(path):
#     #indexTab = [x for x in range(len(path)) if path.startswith("\\",x)]
#     #last = indexTab[len(indexTab)-1]
#     #substring = path[last:]
#     #substring = substring.replace(".pdp","out.pdb")
#     dotIndex = path.find(".")
#     firstList = list(path[:dotIndex])
#     secList = ['o','u','t','.','p','d','b']
#     return "".join(firstList + secList) 

def optionchoice(tab):
    choice = input().upper()
    if choice not in tab:
        print("Opcja nie dostępna")
        choice = optionchoice(tab)
        return choice
    else:
        print("Wybrano: {}".format(choice))
        return choice


def alternative_loc(tab):
    wynik="Alternative locations:\n"
    iter = 0
    indexIter = 0

    locations = []

    for line in tab:
        if len(line[1])>3:
            iter = iter+1

            wynik+="{}:\t{}\t{}\t{}\t{}\t{}\n".format(iter,line[0],line[1],line[2],line[3],line[4])

            if line[1] not in locations:
                locations.append(line[1])
        indexIter = indexIter+1

    if len(locations) == 0:
        wynik+="Lack of alternative locations"

    return wynik, locations

   


def save_new(path,original_path,wybór,tab,locations):
    
    suffixy = {w[-3:] for w in wybór}
    to_skip = [loc for loc in locations if loc[-3:] in suffixy and loc not in wybór]
    
        

    path_split = original_path.split("/")
    saveLocation = path+path_split[len(path_split)-1].split(".")[0]+"out.pdb"
    with open(original_path,"r") as input:
        with open(saveLocation,"w") as output:
            for line in input:
                if len(line)<20:
                    output.write(line)
                    continue
                
                check = line[16:20].strip()    
                # linia z zatwierdzoną alt lokacją - usunięcie alt loc oraz zapis
                if check in wybór:
                    lista = list(line)
                    lista[16] = ' '
                    line = ''.join(lista)
                    output.write(line)
                # pominięcie odrzuconej alt lokacji
                elif check in to_skip:
                    continue
                # linia nie zawierająca alt lokacji - zapis
                else:
                    output.write(line)


    new_tab = []
    for row in tab:
        if row[1] in wybór:
            row[1] = row[1][-3:]
            new_tab.append(row)
        elif row[1] not in to_skip:
            new_tab.append(row)

    locations = [loc for loc in locations if loc not in to_skip and loc not in wybór]
    new_tab = alternative_loc(new_tab)

    return new_tab, locations



         
def read_data(path):
    tab = []
    with open(path,mode="r") as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                tab.append([line[13:16].strip(),line[16:20].strip(),line[21],int(line[22:26].strip()),[float(line[31:38]),float(line[39:46]),float(line[47:54])],line[0]])
    return tab

def missing_data(tab):
    proteinId = tab[0][2]
    wynik = "Protein:"+proteinId+"\n"
    minVal = tab[0][3]
    proteinId = tab[0][2]
    indeks=0
    isPrint = False
    

    for line in range(len(tab)-1):
        #tab[indeks+1][5]== "H" check if HETATM
        if tab[indeks+1][5]== "H" or indeks+1==len(tab)-1:
            if wynik[len(wynik)-3].startswith(":"):
                wynik+="Protein is complete\n"
            break   
        if minVal != tab[indeks+1][3]:
            if tab[indeks+1][3] > minVal +1:
                diff = tab[indeks+1][3] - tab[indeks][3]
                if diff == 2:
                    wynik+="Missing amino acid number " + str(minVal+1) + "\n"
                    isPrint = True

                elif diff >2:
                    isPrint = True
                    wynik += "Missing amino acids [" + str(minVal+1) + " - " + str(tab[indeks+1][3]-1)+"]\n"

        minVal = tab[indeks+1][3]
        if tab[indeks][2] != proteinId:
            if isPrint == False:
                wynik+="Protein is complete\n"
            isPrint = False
            proteinId = tab[indeks][2]
            wynik+= "\nProtein:" + proteinId + "\n"

       
      
        indeks = indeks +1
        

    return wynik





#line[13:16].strip(),line[16:20].strip(),line[21],line[23:26].strip(),[float(line[31:38]),float(line[39:46]),float(line[47:54])],line[0]]

def hetatoms(data):
    wynik = ""
    atoms = np.unique(np.array(data,dtype=object)[:,2])
    wynik = "Number of proteins in the file: " +str(len(atoms)) + "\n"
    for atom in atoms:
        wynik+= atom + "\n"

    
    jony = []
    hoh = []
    ligandy = []
    klucze = list(nazwy.keys())

    # alt sprawdzenie czy 4 kolumna len()>2 dla liganda
    # i jon kol 3 == kol 4 
    index = len(data)-1
    while data[index][5] != 'A':
        
        if data[index][1] == "HOH":
            hoh.append([data[index][3],data[index][2]])
        elif data[index][3] != data[index-1][3]:
            if data[index][3]==data[index+1][3]:
                ligandy.append([data[index][3],data[index][2]])
            else:
                jony.append([data[index][3],data[index][2]])
        else:
            ligandy.append([data[index][3],data[index][2]])
        index = index -1 





    hohDict = {}
    ligDict = {}
    jonDict = {}

    for elem in np.unique([row[1] for row in hoh]):
        hohDict[str(elem)] = []
    for elem in np.unique([row[1] for row in ligandy]):
        ligDict[str(elem)] = []
    for elem in np.unique([row[1] for row in jony]):
        jonDict[str(elem)] = []
        
    for line in hoh:
        hohDict[line[1]].append(line[0])
    for line in ligandy:
        ligDict[line[1]].append(line[0])
    for line in jony:
        jonDict[line[1]].append(line[0])

    lh=len(hoh)
    ll=len(ligandy)
    lj=len(jony)
    if lh>1:
        wynik+="\nCrystallographic waters\n"
        wynik += HetHelper(hohDict,False)
    if ll>1:
        wynik+="\nLigands\n"
        wynik += HetHelper(ligDict,True)
    if lj>1:
        wynik+="\nIons\n"
        wynik += HetHelper(jonDict,False)
    if (lj+ll+lh) ==0:
        wynik+="\nLack of Hetero Atoms\n"
    return wynik



def helper(słownik,flaga):
    wynik="------------------------------------------------------------------------\n"
    for key in list(słownik.keys()):
        wynik+="Białko " + key + " - "  ": [Ilość: " + str(len(słownik[key])) + "]\n"
        tab = np.unique(słownik[key].sort(reversed=True))
        toPrint=True
        first = słownik[key][0]
        last = first
        if flaga == "L":
            for i in range(tab):
                if tab[i]!=tab[i+1]:
                    last = tab[i+1]
                    wynik+="[" + str(first) + " - " + str(last) + "]\n"
                else:
                    last=słownik[key][i+1]
        elif flaga == "H":
            print("debug1")
        else:
            print("debug2")

def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(range(start, end + 1)).difference(L))

def HetHelper(słownik,flaga):
    wynik="------------------------------------------------------------------------\n"
    for key in list(słownik.keys()):
        tab = np.unique(słownik[key])
        wynik+="Protein " + key + " - "  ": [Number: " + str(len(słownik[key])) + "]\n"
        
        if flaga:
            for elem in tab:
                wynik+=str(elem)+" x " + str(słownik[key].count(elem))+"\n"
        else:
            #wynik+=str(elem)+"\n"

                
            for i in range(len(tab)-1):
                begin=0
                if tab[i]+1 != tab[i+1]:
                    wynik+= "[" + str(tab[begin]) + " - " + str(tab[i]) + "]\n"
                    begin = i+1
            wynik+= "[" + str(tab[begin]) + " - " + str(tab[len(tab)-1]) + "]\n"


                    
    return wynik
        




#1-4 ATOM
#7-11 atom serial number
#13-16 atom name
#17 alternate location indicator A przed PHE
#18-20 residue name
#22 chain identifier
#23-26 residue seq
#27 code of intersections of residues
#31-38 X
#39-46 Y
#47-54 Z
#55-60 Occupancy
#61-66 Temperature factor
#68-70 footnote number  
