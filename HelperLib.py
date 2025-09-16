import numpy as np
import matplotlib.pyplot as plt


class Chull:
    def __init__(self, dane):
        
        self.punkty = [dane[i].tolist() for i in range(len(dane))]
        self.plaszcz = {}
        self.plaszcz_indeks = 0
        self.objetosc_otoczki = 0.0
        self.__startowy_ostroscian()
        self.__oblicz_otoczke()
        self.__oblicz_objetosc()

    def __print_init_trihedron(self):#testing
        print("\n")
        for ind, plaszcz in enumerate(self.plaszcz.values()):
            print(ind)
            for koord in plaszcz["koordynaty"]:
                print(koord)


    def __ekstrema(self):
        min_pX = min(self.punkty, key=lambda p: p[0])
        max_pX = max(self.punkty, key=lambda p: p[0])
        min_pY = min(self.punkty, key=lambda p: p[1])
        max_pY = max(self.punkty, key=lambda p: p[1])
        min_pZ = min(self.punkty, key=lambda p: p[2])
        max_pZ = max(self.punkty, key=lambda p: p[2])
        return (max_pX,min_pX,max_pY,min_pY,max_pZ,min_pZ)

    def __dyst_2pkt(self,p,q):
        suma = (p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2
        return suma ** 0.5
    
    def __startowa_linia(self,ekstr):
        rekord = 0
        linia = None
        for i in range(6):
            for j in range(i+1,6):
                dyst =  self.__dyst_2pkt(ekstr[i],ekstr[j])
                if dyst > rekord:
                    rekord = dyst
                    linia = [ekstr[i],ekstr[j]]
        return linia

    def __dyst_linia_pkt(self,linia,pkt):
        pkt = np.array(pkt)
        dyst = np.linalg.norm(np.cross(linia[0]-linia[1],linia[0]-pkt)
                                )/np.linalg.norm(linia[1]-linia[0])
        return dyst
        

    def __startowy_pkt_trojkata(self,linia):
        rekord = 0
        poszukiwany = None
        #baza = [punkt for punkt in self.punkty if punkt not in linia]
        baza = [p for p in self.punkty if not any(np.array_equal(p, x) for x in linia)]
        linia = [np.array(linia[0]), np.array(linia[1])]
        for pkt in baza:
            dyst = self.__dyst_linia_pkt(linia,pkt)
            if dyst > rekord:
                rekord = dyst
                poszukiwany = pkt
        return poszukiwany
    
    def __dyst_pkt_plaszcz(self, pkt, tr):
        pkt, a, b, c = np.array(pkt),np.array(tr[0]),np.array(tr[1]),np.array(tr[2])
        ab = b - a
        ac = c - a
        n = np.cross(ab,ac)
        dyst = abs(np.dot(pkt-a,n))/np.linalg.norm(n)
        return dyst

    def __startowy_pkt_ostroscianu(self,trojkat):
        rekord = 0
        poszukiwany = None
        #baza = [punkt for punkt in self.punkty if punkt not in trojkat]
        baza = [p for p in self.punkty if not any(np.array_equal(p, x) for x in trojkat)]
        for pkt in baza:
            dyst = self.__dyst_pkt_plaszcz(pkt,trojkat)
            if dyst > rekord:
                rekord = dyst
                poszukiwany = pkt
        return poszukiwany
    
    def __dodaj_plaszcz(self,koordynaty):
        a, b, c = np.array(koordynaty[0]), np.array(koordynaty[1]), np.array(koordynaty[2]) 
        pkt1 = a-b
        pkt2 = b-c
        wektor = np.cross(pkt1,pkt2)
        dlugosc = (wektor[0]**2+wektor[1]**2+wektor[2]**2)**0.5
        wektor = np.array([wektor[0]/dlugosc,wektor[1]/dlugosc,wektor[2]/dlugosc])
        self.plaszcz[self.plaszcz_indeks] = {
            "koordynaty" : [
                koordynaty[0],
                koordynaty[1],
                koordynaty[2]
            ],#koordynaty
            "widoczne" : set(),#widoczne dla niej punkty,
            "krawedzie" : (
                (tuple(koordynaty[0]), tuple(koordynaty[1])),
                (tuple(koordynaty[1]), tuple(koordynaty[2])),
                (tuple(koordynaty[2]), tuple(koordynaty[0]))
            ),#krawędzie plaszczyzny
            "norma": wektor,#norma
            "indeks": self.plaszcz_indeks

        }
        self.plaszcz_indeks += 1
        return self.plaszcz[self.plaszcz_indeks-1]

    def __popraw_norme(self,wew_pkt,plaszcz):
        for pkt in wew_pkt:
            dyst = np.dot(plaszcz["norma"],np.subtract(pkt,plaszcz["koordynaty"][0]))
            if dyst !=0 and dyst>10**-10:
                plaszcz["norma"] = -plaszcz["norma"]
    
    def __dystans(self, pkt, plaszcz):
        return np.dot(plaszcz["norma"], np.subtract(pkt, plaszcz["koordynaty"][0]))

    def __oblicz_widoczne(self,punkty,plaszcz):
        for pkt in punkty:
            dyst = self.__dystans(pkt, plaszcz)
            if dyst > 10**(-10):
                plaszcz["widoczne"].add(tuple(pkt))

    def __startowy_ostroscian(self):
        ekstrema = self.__ekstrema()
        linia = self.__startowa_linia(ekstrema)
        pkt_trojkata = self.__startowy_pkt_trojkata(linia)
        pkt_ostroscianu = self.__startowy_pkt_ostroscianu([linia[0],linia[1],pkt_trojkata])


        self.__dodaj_plaszcz([linia[0],linia[1],pkt_trojkata])
        self.__dodaj_plaszcz([linia[0],linia[1],pkt_ostroscianu])
        self.__dodaj_plaszcz([linia[0],pkt_ostroscianu,pkt_trojkata])
        self.__dodaj_plaszcz([linia[1],pkt_trojkata,pkt_ostroscianu])


        self.mozliwe_wew_pkt = [linia[0],linia[1],pkt_trojkata,pkt_ostroscianu]

        for plaszcz in self.plaszcz.values():
            self.__popraw_norme(self.mozliwe_wew_pkt,plaszcz)
            self.__oblicz_widoczne(self.punkty,plaszcz)
    
    def __spr_krawedz(self, krawedz_org, krawedzie):
        for krawedz in krawedzie:
            if (krawedz_org[0] == krawedz[0] and krawedz_org[1] == krawedz[1]) or (
                krawedz_org[0] == krawedz[1] and krawedz_org[1] == krawedz[0]):
                return True
        return False
    
    def __spr_plaszcz(self, plaszcz_org, plaszcz):
        pkty_plaszcz_org = {tuple(pkty) for pkty in plaszcz_org}
        pkty_plaszcz = {tuple(pkty) for pkty in plaszcz}
        return pkty_plaszcz == pkty_plaszcz_org
    
    def __sasiednia_plaszcz(self, plaszcz_org , krawedz):
        for plaszcz in self.plaszcz.values():
            if not self.__spr_plaszcz(plaszcz_org["koordynaty"],plaszcz["koordynaty"]) and self.__spr_krawedz(krawedz,plaszcz["krawedzie"]):
                return plaszcz
        return None
    
    def __sprawdz_sasiada(self, odwiedzone, sasiad):
        indeksy = []
        for plaszcz in odwiedzone:
            indeksy.append(plaszcz["indeks"])
        if sasiad["indeks"] in indeksy:
            return True
        else:
            return False

    def __oblicz_horyzony(self, odwiedzone, plaszcz, pkt, zbior_krawedzi):
        if self.__dystans(pkt,plaszcz) > 10**-10:
            odwiedzone.append(plaszcz)
            krawedzie = plaszcz["krawedzie"]
            for krawedz in krawedzie:
                sasiad = self.__sasiednia_plaszcz(plaszcz, krawedz)
                if not self.__sprawdz_sasiada(odwiedzone, sasiad):
                    wynik = self.__oblicz_horyzony(odwiedzone, sasiad, pkt, zbior_krawedzi)
                    if wynik == 0:
                        zbior_krawedzi.add(krawedz)
            return 1
        else:
            return 0

     

    def __oblicz_otoczke(self):
        Koniec = False
        lista_slownikowa = list(self.plaszcz.values())
        while not Koniec:
            Koniec = True
            for plaszcz in lista_slownikowa:
                if len(plaszcz["widoczne"]) > 0:
                    Koniec = False
                    rekord = 0
                    poszukiwany = None
                    for pkt in  plaszcz["widoczne"]:
                        dyst = self.__dystans(pkt,plaszcz)
                        if dyst > rekord:
                            rekord = dyst
                            poszukiwany = pkt
                    zbior_krawedzi = set()
                    odwiedzone = []
                    self.__oblicz_horyzony(odwiedzone, plaszcz, poszukiwany, zbior_krawedzi)
                    stop = 1
                    for plaszcz in odwiedzone:
                        del self.plaszcz[plaszcz["indeks"]]
                        lista_slownikowa.remove(plaszcz)

                        

                    widoczne = set()
                    for plaszcz in odwiedzone:
                        widoczne = widoczne.union(plaszcz["widoczne"])
                    
                    for krawedz in zbior_krawedzi:
                        plaszcz = self.__dodaj_plaszcz([krawedz[0],krawedz[1],poszukiwany])
                        lista_slownikowa.append(self.plaszcz[self.plaszcz_indeks-1])
                        self.__popraw_norme(self.mozliwe_wew_pkt, plaszcz)
                        self.__oblicz_widoczne(widoczne, plaszcz)
                    
    def __oblicz_objetosc(self):
        sciany = np.array(np.array([item["koordynaty"] for item in self.plaszcz.values()]))
        srodek_ciezkosci = np.mean(sciany.reshape(-1,3), axis=0)
        calkowita_objetosc = 0.0
        for sciana in sciany:
            ostroscian = np.vstack([sciana,srodek_ciezkosci])
            a = ostroscian[1] - ostroscian[0]
            b = ostroscian[2] - ostroscian[0]
            c = ostroscian[3] - ostroscian[0]
            calkowita_objetosc += np.abs(np.dot(a,np.cross(b,c))) / 6.0
        self.objetosc_otoczki = calkowita_objetosc
    
    def objetosc(self):
        return self.objetosc_otoczki
    
    def ilosc(self):
        return len(self.plaszcz)
    

