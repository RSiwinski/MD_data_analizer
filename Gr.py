import numpy as np
import Other.Shared as ost
from DCD_reader import DCDReader



def PDBVol(pdbfile):

    with open(pdbfile, "r") as file:
        for line in file:
            if line.startswith("CRYST1"):
                a = float(line[6:15].strip())
                b = float(line[15:24].strip())
                c = float(line[24:33].strip())
                alpha = float(line[33:40].strip())
                beta  = float(line[40:47].strip())
                gamma = float(line[47:54].strip())
                break

    if alpha == beta == gamma == 90.0:
        volume = a * b * c
    else:
        alpha_rad = np.radians(alpha)
        beta_rad = np.radians(beta)
        gamma_rad = np.radians(gamma)
        volume = a * b * c * np.sqrt(
            1 
            - np.cos(alpha_rad)**2 
            - np.cos(beta_rad)**2 
            - np.cos(gamma_rad)**2 
            + 2 * np.cos(alpha_rad) * np.cos(beta_rad) * np.cos(gamma_rad)
        )
    print("Me "+str(volume))
    return volume

def calc_dist(a1, a2):
    return np.linalg.norm(a1-a2)




def GR(pdbfile,DCDobj : DCDReader,s1,s2,r_max,nbins,dcdfiles):
    

    group_a_indices = np.array(s1)
    group_b_indices = np.array(s2)
    Na = len(group_a_indices)
    Nb = len(group_b_indices)

    
    bins = np.linspace(0, r_max, nbins + 1)

    rdf_hist = np.zeros(nbins)#rdf_hist = np.zeros(len(bins) - 1)
    n_frames = 0
    pair_histograms = np.zeros((Na, Nb, nbins))#pair_histograms = np.zeros((Na, Nb, len(bins) - 1))


    volume = PDBVol(pdbfile)


    for dcdfile in dcdfiles:

        DCDobj.CzytajDCD(dcdfile)
        num_frames = DCDobj.FrameNumber()
        
        for frame in range(num_frames):
            
            if not ost.Pause.is_set():
                ost.Pause.wait()

            ramka = DCDobj.get__DCDframe(frame)
            
            for i in range(Na):
                for j in range(Nb):
                    dist = np.linalg.norm(np.array(ramka[group_a_indices[i]]) - np.array(ramka[group_b_indices[j]]))  # |r_i - r_j|
                    if dist <= r_max:
                        hist, _ = np.histogram([dist], bins=bins)  # δ(|ri - rj| - r)
                        pair_histograms[i, j] += hist  # akumulujemy po ramach
            n_frames+=1
            
    # Uśrednienie po ramach: ⟨δ⟩
    pair_histograms /= n_frames

    # Sumowanie po parach (i,j): ∑_i ∑_j ⟨δ(...)⟩
    rdf_hist = np.sum(pair_histograms, axis=(0, 1))

    density_b = Nb / volume#testvolume

    # Środek binów i objętości powłok sferycznych
    r = 0.5 * (bins[1:] + bins[:-1])
    shell_volumes = (4/3) * np.pi * (bins[1:]**3 - bins[:-1]**3)

    # Finalna normalizacja: (1/Na) * (1/(Nb/V)) * ∑_i ∑_j ⟨δ(...)⟩ / ΔV
    rdf = rdf_hist / (Na * density_b * shell_volumes)



    return r, rdf


