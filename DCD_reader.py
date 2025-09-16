from enum import Enum
import numpy as np
from struct import unpack
from os.path import getsize



class BitType(Enum):
    BIT_32 = 1
    BIT_64 = 2

class DCDReader:

    def __init__(self, superpose):
        self.__first_frame = None
        self.__latom_pdb = None
        self.__PDBdane = None
        self.__superpose = superpose

        
    
    

    def CzytajPDB(self, nazwaplikuPDB):
        self.__nazwaplikuPDB = nazwaplikuPDB
        self.plikPDB = open(self.__nazwaplikuPDB, 'r')
        __PDBdane = []
        l_atoms = 0
        for line in self.plikPDB:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    __PDBdane.append([x, y, z])
                    l_atoms+=1
                except ValueError:
                    continue  
        self.__PDBdane = np.array(__PDBdane)
        self.__latom_pdb = l_atoms

    def ZwrocPDB(self):
        if self.__PDBdane is None:
            self.__PDBdane()
        return self.__PDBdane


    def PDBliczbaAtomow(self):
        return self.__latom_pdb 


    def CzytajDCD(self, nazwaplikuDCD):
        self.__nazwaplikuDCD = nazwaplikuDCD
        self.__plikDCD = open(self.__nazwaplikuDCD, 'rb')
        bit_type = BitType.BIT_32
        endian = None
        charmm = False

        # Odczytaj dwa inty, aby przetestować format nagłówka
        czysty_nagłówek = self.__plikDCD.read(8)
        val1, val2 = unpack('ii', czysty_nagłówek)
        dcd_magic = unpack('i', b'CORD')[0]

        # Sprawdź, czy to 64-bitowe CHARMM
        if val1 + val2 == 84:
            bit_type = BitType.BIT_64
            endian = '='  
        elif val1 == 84 and val2 == dcd_magic:
            endian = '='  # natywne endianness
        else:
            # Spróbuj odczytu jako big-endian
            try:
                be_val1, be_val2 = unpack('>ii', czysty_nagłówek)
                if be_val1 + be_val2 == 84:
                    bit_type = BitType.BIT_64
                    endian = '>'
                elif be_val1 == 84 and be_val2 == dcd_magic:
                    endian = '>'
            except Exception:
                pass

            # Jeśli big-endian nie pasuje, spróbuj little-endian
            if endian is None:
                le_val1, le_val2 = unpack('<ii', czysty_nagłówek)
                if le_val1 + le_val2 == 84:
                    bit_type = BitType.BIT_64
                    endian = '<'
                elif le_val1 == 84 and le_val2 == dcd_magic:
                    endian = '<'

        # Jeśli nadal nie wiemy, co to za endian, przerwij
        if endian is None:
            raise IOError("Could not discern the endianness in DCD header")

        # Jeżeli to 64-bitowy CHARMM, sprawdź magic
        if bit_type == BitType.BIT_64:
            cord_spr = unpack(endian + 'I', self.__plikDCD.read(4))[0]
            if cord_spr != dcd_magic:
                raise IOError("No magic number CORD for CHARMM")

        # Czytaj nagłówek (80 bajtów)
        nagłówek = self.__plikDCD.read(80)
        # Na końcu headera znajduje się flaga CHARMM (ostatni int)
        if unpack(endian + 'i', nagłówek[-4:])[0] != 0:
            charmm = True

        # Rozpakuj nagłówek zależnie od flagi CHARMM
        if charmm:
            fields = unpack(endian + '9i f 10i', nagłówek)
        else:
            raise IOError("DCD file is not compliant with CHARMM")

        self.__lramek = fields[0]
        self.__first_ts = fields[1]
        self.__framefreq = fields[2]
        self.__n_fixed = fields[8]

        

        self._timestep = fields[9]
        self.__unitcell = fields[10] == 1

        # Sprawdzenie końca bloku
        blk_end = unpack(endian + 'i', self.__plikDCD.read(4))[0]
        if blk_end != 84:
            raise IOError("Failed to read the header")

        # Czytaj rozmiar kolejnego bloku
        rozmiar_następnego_bloku = unpack(endian + 'i', self.__plikDCD.read(4))[0]
        if (rozmiar_następnego_bloku - 4) % 80 != 0:
            raise IOError("Wrong size of REMARKS block")

        brak_uwag = rozmiar_następnego_bloku == 84

        # Przeczytaj REMARKS
        _ = unpack(endian + 'i', self.__plikDCD.read(4))[0]  # Rozmiar REMARK
        self.__tytułDCD = self.__plikDCD.read(80)

        if not brak_uwag:
            self.__uwagi = self.__plikDCD.read(80)

        _ = unpack(endian + 'i', self.__plikDCD.read(4))[0]  # Koniec REMARK

        # Sprawdź poprawność separatora
        if unpack(endian + 'i', self.__plikDCD.read(4))[0] != 4:
            raise IOError("Wreong separator before the number of atoms")

        self.__latom = unpack(endian + 'i', self.__plikDCD.read(4))[0]

        # Sprawdź zakończenie sekcji atomów
        if unpack(endian + 'i', self.__plikDCD.read(4))[0] != 4:
            raise IOError("Failed to read the number of atoms")

        # Inicjalizacja typów danych i rozmiarów ramek
        self._Bittype = bit_type
        self._endian = endian
        self.__l_float = (self.__latom + 2) * 3

        if bit_type == BitType.BIT_64:
            self.__typ_elem = np.float64
            self.__rozmiar_elem = 8
            self.__rozmiar_markera_rekordu = 8
            self.__bajty_na_ramkę = 56 + self.__l_float * 8 if self.__unitcell else self.__l_float * 8
        else:
            self.__typ_elem = np.float32
            self.__rozmiar_elem = 4
            self.__rozmiar_markera_rekordu = 4
            self.__bajty_na_ramkę = 56 + self.__l_float * 4 if self.__unitcell else self.__l_float * 4

        self.__ifix_block = None
        if self.__n_fixed > 0:
            elem_type = np.int32
            rozmiar_elem = 4
            self.__ifix_block = np.frombuffer(
                self.__plikDCD.read(self.__n_fixed * rozmiar_elem), dtype=elem_type
            )



        # Oblicz pozycję pierwszej ramki
        self.__pierwszy_bajt = self.__plikDCD.tell()
        rozmiar_pliku = getsize(self.__nazwaplikuDCD)
        liczba_ramek = (rozmiar_pliku - self.__pierwszy_bajt) // self.__bajty_na_ramkę

        if liczba_ramek != self.__lramek:
            self.__lramek = liczba_ramek
        

        self.__plikDCD.seek(self.__pierwszy_bajt)
    
    def FrameNumber(self):
        return self.__lramek

    def DCDliczbaAtomow(self):
        return self.__latom


    def get__DCDframe(self, idx):
        if self.__first_frame is None and idx != 0 and self.__ifix_block is not None:
            self.__first_frame = self.get__DCDframe(0)
        if idx > 0:
            self.__plikDCD.seek(self.__pierwszy_bajt + self.__bajty_na_ramkę * idx)

        l_floats = self.__l_float + (14 if self.__unitcell else 0)
        l_atoms = self.__latom

        # Wczytaj dane jako float32 lub float64 w zależności od bit_type
        data = self.__plikDCD.read(self.__rozmiar_elem * l_floats)
        data = np.frombuffer(data, dtype=self.__typ_elem)

        if len(data) < l_floats:
            raise Exception("File is corrupted or incomplete frame")

        frame = []
        iter_offset = 14 if self.__unitcell else 0

        frame = np.empty((l_atoms, 3), dtype=self.__typ_elem)

        iter_offset = 14 if self.__unitcell else 0

        for i in range(l_atoms):
            if self.__ifix_block is  None or self.__ifix_block[i] == 0:
                frame[i] = [
                    data[1 + iter_offset + i],
                    data[l_atoms + 3 + iter_offset + i],
                    data[2 * l_atoms + 5 + iter_offset + i]
                ]
            else:
                frame[i] = self.__first_frame[i] 


      
        if self.__superpose == 1:
            frame = self.__Superpozycja(frame)
        

        return np.array(frame)




        
    

    def __Superpozycja(self, frame):
        traj_dane = np.asarray(frame, dtype=float)
        ref = self.__PDBdane

        # centroid referencyjny
        ref_centrum = np.mean(ref, axis=0)
        ref_przes = ref - ref_centrum

        # centroid ramki
        ramka_centrum = np.mean(traj_dane, axis=0)
        ramka_przes = traj_dane - ramka_centrum

        # algorytm Kabscha – obliczenie macierzy rotacji
        kowariancja = np.dot(ref_przes.T, ramka_przes)
        u, _, vt = np.linalg.svd(kowariancja)
        rotacja = np.dot(u, vt)

        # korekta znaku, jeśli wyznacznik < 0 (odbicie)
        if np.linalg.det(rotacja) < 0.0:
            u[:, -1] *= -1
            rotacja = np.dot(u, vt)

        # zastosowanie rotacji i przesunięcia
        return np.dot(ramka_przes, rotacja.T) + ref_centrum





    
    
    









