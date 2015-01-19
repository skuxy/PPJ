#!/usr/bin/env python
import sys
from time import sleep
import copy
import math

class Tip():
    def __init__(self, tip, jeNiz, jeKonst, parametri):
        self.tip = tip
        self.jeNiz = jeNiz
        self.jeKonst = jeKonst
        self.parametri = parametri
        
    def implicitnoINT(self):
        if((self.tip == "INT" or self.tip == "CHAR") and (self.jeNiz == False)):
            return True
        else:
            return False
    

class podatakTablica():
    def __init__(self, ime, tip):
        self.ime = ime
        self.tip = tip
        
class Tablica():
    def __init__(self, prethodni):
        self.lista = []
        self.prethodni = prethodni
        
    def dodaj_u_tablicu(self, ime, tip):
        podatak = podatakTablica(ime, tip)
        self.lista.append(podatak)

class Cvor():
    def __init__(self, ime, razina, prethodni):
        self.naziv = ime
        self.listaDjece = []
        self.razina = razina
        self.tip = None
        self.tipovi = []
        self.l_izraz = None
        self.tablica = None
        self.imena = []
        self.ime = None
        self.ntip = None
        self.br_elem = None
        self.prethodni = prethodni



def brojPraznih(niz):
    brojpraznih = 0
    while(niz[brojpraznih] == " "):
        brojpraznih += 1
    return brojpraznih

def ispisStabla(korijen, praznina):
    #f.write(' '*praznina + korijen.naziv + '\n')
    for dijete in korijen.listaDjece:
        ispisStabla(dijete, praznina+1)

def okINT(broj):
    if(broj > -2147483648 and broj < 2147483647):
        return True
    return False

def jeChar(znak):
    
    if(len(znak) == 3):
        znak = znak[1]
    val = ""
    if(znak[0] == '\\'):
        if(len(znak) == 2):
            pom = znak[1]
        
            if(pom == "t"):
                val = "\t"
            elif(pom == "n"):
                val = "\n"
            elif(pom == "0"):
                val = "\0"
            elif(pom == "'"):
                val = "\'"
            elif(pom == '"'):
                val = '"'
            elif(pom == "\\"):
                val = "\\"
            else:
                return False
        else:
            return False
    else:
        if(znak == "\"" or znak == "'"):
            return False
        val = znak[0]
    
    val = ord(val)
    if(val >= 0 and val <= 255):
        return True
    else:
        return False

def jeString(niz):
    
    provjera = True
    i = 0
    while(i < len(niz)):
        if(niz[i] == '\\'):
            if(i+1 == len(niz)):
                return False
            else:
                provjera = jeChar(niz[i] + niz[i+1])
                i += 2
        else:
            provjera = jeChar(niz[i])
        i += 1
    
    return provjera


def provjeriDeklarirano(tablica, idn):
    while True:
        ##print tablica.lista
        for zapis in tablica.lista:
            
            ##print zapis.tip.tip
            ##print zapis.ime
            ##print zapis.tip.parametri
            ##print idn
            if(zapis.ime == idn):
                return True
            
        if(tablica.prethodni != None):
            ##print 'ikad'
            tablica = tablica.prethodni
        else:
            return False
        
def deklariranoGlobalno(tablica, ime, tip):
    while(tablica.prethodni != None):
        tablica = tablica.prethodni
    
    pronaden = ""    
    for zapis in tablica.lista:
        if(zapis.ime == ime):
            pronaden = zapis
            break
    
    if pronaden == "":
        return 0
    else:
        if(pronaden.tip.tip == tip.tip):
            for i in range(0, len(pronaden.tip.parametri)):
                if(pronaden.tip.parametri[i] != tip.parametri[i]):
                    return -1
            return 1
        else:
            return -1
        
def pretvorbaDopustena(iz, u):
    ##print iz.tip
    ##print u.tip
    ##print 'fdsfsdfsdfs'
    if(iz.tip == None or u.tip == None):
        return False
    if(iz.tip == "VOID" and u.tip == "VOID"):
        return True
    if(u.tip == "INT"):
        if((iz.tip == "INT" or iz.tip == "CHAR") and iz.jeNiz == u.jeNiz): # and iz.parametri == 0):
            return True
            """if(iz.parametri == 0 and u.parametri == 0):
                return True
            if((iz.parametri == 0 and u.parametri != 0) or (iz.parametri != 0 and u.parametri == 0)):
                return False
            if(len(iz.parametri) != len(u.parametri)):
                return False
            for i in range(0, len(iz.parametri)):
                if(iz.parametri[i].tip != u.parametri[i].tip):
                    return False
            return True"""
        else:
            return False
    elif(u.tip == "CHAR"):
        if(iz.tip == "CHAR"):
            return True
        else:
            return False
        
def provjeriCast(iz, u):
    if(iz.tip == "INT" and u.tip == "CHAR"):
        return True or pretvorbaDopustena(iz, u)
    else:
        return False or pretvorbaDopustena(iz, u)
    
def nadiFunkciju(cvor):
    pom = copy.copy(cvor)
    while(pom.naziv != "<definicija_funkcije>"):
        pom = pom.prethodni
      
    pom = pom.listaDjece[0]
    ###print pretvorbaDopustena(cvor.tip, pom.tip)
    return pretvorbaDopustena(cvor.tip, pom.tip)
    
def nadiString(cvor):
    while(cvor.naziv[0:3] != "NIZ"):
        cvor = cvor.listaDjece[0]
    
    ime = cvor.naziv.split(" ")
    ime = ime[2]
    return ime
 
def ispisiGresku(cvor):
    ispis = ""
    ispis += cvor.naziv + " ::="
    
    for i in range(0, len(cvor.listaDjece)):
        if(cvor.listaDjece[i].naziv[0:1] == '<'):
            ispis += " " + cvor.listaDjece[i].naziv
        else:
            pom = cvor.listaDjece[i].naziv.split(" ")
            dodaj = pom[0] + '(' + pom[1] + ',' + pom[2] + ')'
            ispis += " " + dodaj
            
    #print ispis
    sys.exit(0)
    
def provjeriMain(cvor):
    for zapis in cvor.tablica.lista:
        if(zapis.ime == "main"):
            if(zapis.tip.tip == "INT"):
                if(zapis.tip.parametri[0].tip == "VOID"):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    return False

def vratiIdentifikator(tablica, idn):
    while tablica != None or tablica.prethodni != None:
        for zapis in tablica.lista:
            if zapis.ime == idn:
                return zapis.tip
        tablica = tablica.prethodni
    
    return None
        
def sveDeklarirane(tablica):
    for zapis in listaDeklariranihFunkcija:
        for pod in tablica.lista:
            if(zapis.ime != pod.ime):
                return False
            else:
                if(zapis.tip.tip != pod.tip.tip):
                    return False
                if(zapis.tip.jeNiz != pod.tip.jeNiz):
                    return False
                if(zapis.tip.jeKonst != pod.tip.jeKonst):
                    return False
                for i in range(0, len(zapis.tip.parametri)):
                    if(zapis.tip.parametri[i] != pod.tip.parametri[i]):
                        return False
    return True
        
def pronadiPetlju(cvor):
    while(cvor.prethodni == None):
        if(cvor.naziv == "<naredba_petlje>"):
            return True
        cvor = cvor.prethodni
    return False

def provjeriPozvano(cvor):
    pom = copy.copy(cvor)
    while cvor.naziv != '<postfiks_izraz>':
        if(cvor.naziv == '<cast_izraz>' and len(cvor.listaDjece) == 4):
            cvor = cvor.listaDjece[3]
        else:
            cvor = cvor.listaDjece[0]
        
    if(pom.tip.parametri[0].tip == "VOID"):
        if(len(cvor.listaDjece) != 3):
            return False
        else:
            return True
    else:
        if(len(cvor.listaDjece) != 4):
            return False
        else:
            return True
        
def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def vratiVrijednost(dijete):
    imaMinus = False
    oduzimanje = False
    operacijaOR = False
    operacijaAND = False
    operacijaXILI = False
    jePozivPolja = False
    jeFunkcija = False
    indeks = None
    jestFunkcija = []
    argumentiPoziva = []
    listaBrojeva = []
    
    while dijete.naziv != "<primarni_izraz>":
        if(dijete.naziv == "<unarni_izraz>" and len(dijete.listaDjece) == 2):
            imaMinus = True
            dijete = dijete.listaDjece[1]
        elif((dijete.naziv == "<aditivni_izraz>" and len(dijete.listaDjece) == 3) or (dijete.naziv == "<bin_ili_izraz>" and len(dijete.listaDjece) == 3) or (dijete.naziv == "<bin_i_izraz>" and len(dijete.listaDjece) == 3) or (dijete.naziv == "<bin_xili_izraz>" and len(dijete.listaDjece) == 3)):
            novi = vratiVr(dijete.listaDjece[2])
            pom = dijete.listaDjece[2]
            
            pomFlag = True
            if(dijete.listaDjece[2].tip.parametri != 0 ):
                jestFunkcija.append(True)
                pomFlag = False
                
                if dijete.listaDjece[2].tip.parametri[0].tip != "VOID":
                    tmp = dijete.listaDjece[2]
                    while tmp.naziv != "<postfiks_izraz>":
                        tmp = tmp.listaDjece[0]
                
                    #print 'BLALBALBALBALB'
                    #print dijete.listaDjece[2].tip.parametri[0].tip
                    #print '----'
                    vr = vratiVr(tmp.listaDjece[2])
                    #print 'BLALBALBALBALB'
                    #print vr
                    argumentiPoziva.append(vr)
            else:
                jestFunkcija.append(False)
            
            while pom.naziv != "<postfiks_izraz>":
                pom = pom.listaDjece[0]
            
            if(len(pom.listaDjece) == 4 and pomFlag):
                ind = vratiVr(pom.listaDjece[2])
                listaBrojeva.append(novi + ind)
            else:
                listaBrojeva.append(novi)
            tmp = dijete.listaDjece[1]
            if(tmp.naziv[0:5] == "MINUS"):
                oduzimanje = True
            elif(tmp.naziv[0:10] == "OP_BIN_ILI"):
                operacijaOR = True
            elif(tmp.naziv[0:8] == "OP_BIN_I"):
                operacijaAND = True
            elif(tmp.naziv[0:11] == "OP_BIN_XILI"):
                operacijaXILI = True
            dijete = dijete.listaDjece[0]
        elif((dijete.naziv == "<postfiks_izraz>" and len(dijete.listaDjece) == 4 and dijete.listaDjece[1].naziv[0:9] == "L_ZAGRADA")):
            srediArgumente(dijete.listaDjece[2])
            dijete = dijete.listaDjece[0]
        elif((dijete.naziv == "<postfiks_izraz>" and len(dijete.listaDjece) == 4 and dijete.listaDjece[1].naziv[0:13] == "L_UGL_ZAGRADA")):
            jePozivPolja = True
            indeks = vratiVr(dijete.listaDjece[2])
            
            dijete = dijete.listaDjece[0]
        else:
            dijete = dijete.listaDjece[0]
        
    dijete = dijete.listaDjece[0]
    imena = dijete.naziv.split(" ")
    #print imena
    
    if(len(listaBrojeva) > 0):
        #print '++++++++++++++'
        #print 'tuuuuuuuuuuuuuuuuu'
        #print argumentiPoziva
        #print dijete.prethodni.naziv
        #print dijete.prethodni.tip.parametri
        #print listaBrojeva
        
        jeRekurzija = False
        
        posebnoZbrajanje = False
        if(dijete.prethodni.tip.parametri != 0):
            jestFunkcija.append(True)
        else:
            jestFunkcija.append(False)
            
        if(jePozivPolja):
            listaBrojeva.append(imena[2] + indeks)
        else:
            listaBrojeva.append(imena[2])
        duzina = len(listaBrojeva)
        for i in range(0, duzina):
            Treba = True
            provjeri = listaBrojeva[duzina-i-1]
            if(dijete.tablica != None and len(dijete.tablica.lista) > 0):
                for j in range(0, len(dijete.tablica.lista)):
                    if(dijete.tablica.lista[j].ime == provjeri):
                        ispis.write("\tLOAD R" + str(i) + ", (R7 + " + str((i+1)*4) + ")\n")
                        Treba = False
                        break
            if Treba:
                if isNumber(provjeri):
                    ispis.write("\tMOVE %D " + listaBrojeva[duzina-i-1] + ", R" + str(i) + '\n')
                elif(jestFunkcija[duzina-i-1]):
                    if(i == 0):
                        ispis.write("\tCALL F_" + listaBrojeva[duzina-i-1].upper() + '\n')
                        ispis.write("\tADD R7, 4, R7\n")
                    elif(len(argumentiPoziva) == 0):
                        jeRekurzija = True
                        ispis.write("\tCALL F_" + listaBrojeva[duzina-i-1].upper() + '\n')
                        ispis.write("\tMOVE %D " + listaBrojeva[duzina-i-2] + ", R" + str(i-1) + '\n')
                        ispis.write("\tADD R0, R6, R6\n") 
                    else:
                        ispis.write("\t PUSH R6\n")
                        ispis.write("\t POP R2\n")
                        ispis.write("\tMOVE %D " + argumentiPoziva[duzina-i-1] + ", R0" + '\n')
                        ispis.write("\t PUSH R0\n")
                        ispis.write("\tCALL F_" + listaBrojeva[duzina-i-1].upper() + '\n')
                        ispis.write("\tADD R7, 4, R7\n")
                        posebnoZbrajanje = True
                else:
                    ispis.write("\tLOAD R" + str(i) + ", (G_" + listaBrojeva[duzina-i-1].upper() + ")\n")
        
        operacija = ""
        if(oduzimanje):
            operacija = "SUB"
        elif(operacijaOR):
            operacija = "OR"
        elif(operacijaAND):
            operacija = "AND"
        elif(operacijaXILI):
            operacija = "XOR"
        else:
            operacija = "ADD"
        
        if(not jeRekurzija):    
            if(duzina > 2):
                i = 0
                while(i<duzina):
                    if i == 0:
                        ispis.write("\t" + operacija + " R" + str(i) + ", R" + str(i+1) + ", R6\n")
                        i += 2
                    else:
                        ispis.write("\t" + operacija + " R6, R" + str(i) + ", R6\n")
                        i += 1
            else:
                if posebnoZbrajanje:
                    ispis.write("\t ADD R6, R2, R6\n")
                else:
                    ispis.write("\t" + operacija)
                    for i in range(0, duzina):
                        if(i == 0):
                            ispis.write(" R" + str(i))
                        else:
                            ispis.write(", R" + str(i))
                
                    ispis.write(", R6\n")
    elif jePozivPolja:
        ime = imena[2].upper()
        ispis.write("\t LOAD R6, (G_" + ime + indeks + ")\n")
    elif(imena[0] == "BROJ"):
        ime = imena[2]
        
        broj = long(ime)
        if(broj > math.pow(2, 20)):
            #ispis.write("\nG_B DW %D " + ime + '\n')
            lista_var.append("B")
            lista_vri.append(ime)
            ispis.write("\tLOAD R6, (G_B)\n")
        else:    
            if(not imaMinus):
                ispis.write("\tMOVE %D " + ime + ", R6\n")
            else:
                ispis.write("\tMOVE %D " + "-" + ime + ", R6\n")
            return int(ime)
    elif(imena[0] == "IDN"):
        #print '-------+'
        ##print dijete.prethodni.tip.tip
        ##print dijete.prethodni.tip.parametri[0].tip
        
        if(dijete.prethodni.tip.parametri != 0):
            ime = imena[2].upper()
            ispis.write("\t CALL F_" + ime + '\n')
        else:
            ime = imena[2].upper()
            if ime in deklariraneGlobalno:
                ponavljanje = deklariraneGlobalno[ime]
                if(ponavljanje > 0):
                    ispis.write("\t LOAD R6, (G_" + ime + str(ponavljanje) + ")\n")
                else:
                    ispis.write("\t LOAD R6, (G_" + ime + ")\n")
            else:
                ispis.write("\t LOAD R6, (G_" + ime + ")\n")

def srediArgumente(dijete):
    while dijete.naziv != "<primarni_izraz>":
        dijete = dijete.listaDjece[0]
        
    dijete = dijete.listaDjece[0]
    imena = dijete.naziv.split(" ")
    if imena[0] == "BROJ":
        ime = imena[2]
        ispis.write("\tMOVE %D " + ime + ', R0' + '\n')
        ispis.write("\tPUSH R0" + '\n')
        
def vratiVr(dijete):
    imaMinus = False
    #print dijete.naziv
    while dijete.naziv != "<primarni_izraz>":
        if(dijete.naziv == "<unarni_izraz>" and len(dijete.listaDjece) == 2):
            imaMinus = True
            dijete = dijete.listaDjece[1]
        elif(dijete.naziv == "<cast_izraz>" and len(dijete.listaDjece) == 4):
            dijete = dijete.listaDjece[3]
        else:
            dijete = dijete.listaDjece[0]
        
    dijete = dijete.listaDjece[0]
    imena = dijete.naziv.split(" ")
    
    if(imena[0] == "BROJ"):
        ime = imena[2]
        #print ime
        #print imaMinus
        #print '+++++'
        if imaMinus:
            return "-" + ime
        else:
            return ime
    elif(imena[0] == "IDN"):
        return imena[2].upper()
    elif(imena[0] == "ZNAK"):
        ime = ord(imena[2][1:2])
        return str(ime)
#---------------- -------------------------------------------------------

def primarni_izraz(cvor):
    ##print 'primarni_izraz'
    dijete = cvor.listaDjece[0]
    ##print dijete.naziv
    
    if(dijete.naziv[0:3] == "IDN"):
        #???????????
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        dijete.tablica = cvor.tablica
        if(provjeriDeklarirano(dijete.tablica, ime)):
            #????
            cvor.tip = vratiIdentifikator(dijete.tablica, ime)
            #print cvor.tip.tip
            #print cvor.tip.parametri
            #print '---------'
            if(cvor.tip == None):
                for fun in listaDefiniranihFunkcija:
                    if fun.ime == ime:
                        cvor.tip = fun.tip
            ##print 'weeeeee'
            ##print cvor.tip.tip
            ##print cvor.tip.parametri
            cvor.l_izraz = 1 #GREKA
        else:
            ispisiGresku(cvor)
    elif(dijete.naziv[0:4] == "BROJ"):
        broj = dijete.naziv.split(" ")
        broj = int(broj[2])
        
        if(okINT(broj)):
            cvor.tip = Tip("INT", False, False, 0)
            cvor.l_izraz = 0
        else:
            ispisiGresku(cvor)
        
    elif(dijete.naziv[0:4] == "ZNAK"):
        znak = dijete.naziv.split(" ")
        znak = znak[2]
        
        if(jeChar(znak)):
            cvor.tip = Tip("CHAR", False, False, 0)
            cvor.l_izraz = 0
            ##print 'vr1'
        else:
            ispisiGresku(cvor)
        
    elif(dijete.naziv[0:11] == "NIZ_ZNAKOVA"):
        ##print 'BLALALALALLALALALLA'
        niz = dijete.naziv.split(" ")
        niz = niz[2]
        niz = niz[1:len(niz)-2]
        
        if(jeString(niz)):
            cvor.tip = Tip("STRING", True, True, 0)
            cvor.l_izraz = 0
        else:
            ispisiGresku(cvor)
        
    elif(dijete.naziv[0:9] == "L_ZAGRADA"):
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[0] = dijete
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    return cvor
        
def postfiks_izraz(cvor):
    ##print 'postfiks_izraz'
    dijete = cvor.listaDjece[0]
    ##print len(cvor.listaDjece)
    
    if(dijete.naziv == "<primarni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = primarni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        ###print dijete.tip.tip
        
    elif(dijete.naziv == "<postfiks_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = postfiks_izraz(dijete)
        cvor.listaDjece[0] = dijete
        dijete = cvor.listaDjece[1]
        
        if(dijete.naziv[0:13] == "L_UGL_ZAGRADA"):
            #??? 2. korak
            dijete = cvor.listaDjece[0]
            if(dijete.tip.jeNiz != True):
                ispisiGresku(cvor)
            dijete.tip = Tip(dijete.tip.tip, True, dijete.tip.jeKonst, 0)
            cvor.listaDjece[0] = dijete
            
            #3. korak
            dijete = cvor.listaDjece[2]
            dijete.tablica = cvor.tablica
            dijete = izraz(dijete)
            cvor.listaDjece[2] = dijete
            
            #4. korak
            if(dijete.tip.implicitnoINT()):
                #???
                dijete = cvor.listaDjece[0]
                cvor.tip = Tip(dijete.tip.tip, False, dijete.tip.jeKonst, 0)
                if(dijete.tip.jeKonst == True):
                    cvor.l_izraz = 0
                else:
                    cvor.l_izraz = 1
            else:
                ispisiGresku(cvor)
                
        elif(dijete.naziv[0:9] == "L_ZAGRADA" and len(cvor.listaDjece) == 3):
            #??????????? mozda treba nekako rjesit da je funkcija
            dijete = cvor.listaDjece[0]
            #cvor.tip = Tip(dijete.tip.tip, False, False, 0) #???????????
            #cvor.tip = Tip(dijete.tip.tip, dijete.tip.jeNiz, dijete.tip.JeKonst, dijete.tip.parametri)
            if(dijete.tip.parametri[0].tip != "VOID"):
                ispisiGresku(cvor)
            cvor.tip = dijete.tip
            cvor.l_izraz = 0
        elif(dijete.naziv[0:9] == "L_ZAGRADA" and len(cvor.listaDjece) == 4):
            dijete = cvor.listaDjece[2]
            dijete.tablica = cvor.tablica
            dijete = lista_argumenata(dijete)
            cvor.listaDjece[2] = dijete
            #mora provjeriti paramtetre bla bal
            dijete2 = cvor.listaDjece[0]
            
            """for x in cvor.listaDjece:
                ##print '---'
                ##print x.naziv"""
            
            ##print dijete.tipovi
            if(len(dijete.tipovi) > len(dijete2.tip.parametri)):
                ispisiGresku(cvor)
                
            for i in range(0, len(dijete.tipovi)):
                if(not(pretvorbaDopustena(dijete.tipovi[i], dijete2.tip.parametri[i]))):
                    ispisiGresku(cvor)
                #provjeriti da li su implicitno isti kao argumenti
            cvor.tip = Tip(dijete2.tip.tip, dijete2.tip.jeNiz, dijete2.tip.jeKonst, dijete2.tip.parametri)
            cvor.l_izraz = 0
                
        elif(dijete.naziv == "OP_INC" or dijete.naziv == "OP_DEC"):
            #???????
            dijete = cvor.listaDjece[0]
            dijete.l_izraz = 1 #????
            if(not(dijete.tip.implicitnoINT())):
                ispisiGresku(cvor)
            
            cvor.tip = Tip("INT", False, False, 0)
            cvor.l_izraz = 0
            
    return cvor

def lista_argumenata(cvor):
    ##print 'lista_argumenata'
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        cvor.tipovi.append(dijete.tip)
    elif(dijete.naziv == "<lista_argumenata>"):
        dijete.tablica = cvor.tablica
        dijete = lista_argumenata(dijete)
        cvor.listaDjece[0] = dijete
        dijete2 = cvor.listaDjece[2]
        dijete2.tablica = cvor.tablica
        dijete2 = izraz_pridruzivanja(dijete2)
        dijete2 = cvor.listaDjece[2]
        
        for tip in dijete.tipovi:
            cvor.tipovi.append(tip)
        
        ##print cvor.tipovi
        cvor.tipovi.append(dijete2.tip)
        ##print '#####################'
        ##print cvor.tipovi
        
    return cvor
        
def unarni_izraz(cvor):
    ##print 'unarni_izraz'
    dijete = cvor.listaDjece[0]
    ##print dijete.naziv
    
    if(dijete.naziv == "<postfiks_izraz>"):
        dijete.tablica = cvor.tablica   
        dijete = postfiks_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv[0:6] == "OP_INC" or dijete.naziv[0:6] == "OP_DEC"):
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = unarni_izraz(dijete)
        dijete.l_izraz = 1 #? 2.korak
        cvor.listaDjece[1] = dijete
        
        #????
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        
    elif(dijete.naziv == "<unarni_operator>"):
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = cast_izraz(dijete)
        cvor.listaDjece[1] = dijete
        
        #2.korak ????
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
    
    return cvor
        
def cast_izraz(cvor):
    ##print 'cast_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<unarni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = unarni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv[0:9] == "L_ZAGRADA"):
        
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = ime_tipa(dijete)
        cvor.listaDjece[1] = dijete
        
        dijete2 = cvor.listaDjece[3]
        dijete2.tablica = cvor.tablica
        dijete2 = cast_izraz(dijete2)
        cvor.listaDjece[3] = dijete2
        
        #??? provjeriti castanje po pravilima
        ##print dijete.tip.tip
        ##print dijete.tip.jeNiz
        ##print dijete.tip.jeKonst
        ##print dijete2.tip.tip
        ##print dijete2.tip.jeNiz
        ##print dijete2.tip.jeKonst
        ##print '+++++++++++++++'
        if(not(provjeriCast(dijete2.tip, dijete.tip))):
            ##print 'tu'
            ispisiGresku(cvor) #valjda?
        
        #cvor.tip = dijete.tip
        cvor.tip = Tip(dijete.tip.tip, dijete.tip.jeNiz, dijete.tip.jeKonst, dijete2.tip.parametri)
        cvor.l_izraz = 0 
        
    return cvor

def ime_tipa(cvor):
    ##print 'ime_tipa'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<specifikator_tipa>"):
        dijete.tablica = cvor.tablica
        dijete = specifikator_tipa(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
    elif(dijete.naziv[0:8] == "KR_CONST"):
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = specifikator_tipa(dijete)
        cvor.listaDjece[1] = dijete
        
        if(dijete.tip.tip != "VOID"):
            cvor.tip = Tip(dijete.tip.tip, False, True, 0)
        else:
            ispisiGresku(cvor)
    return cvor

def specifikator_tipa(cvor):
    ##print 'specifikator_tipa'
    dijete = cvor.listaDjece[0]
    ime = dijete.naziv.split(" ")
    ime = ime[0]
    
    if(ime == "KR_VOID"):
        cvor.tip = Tip("VOID", False, False, 0)
    elif(ime == "KR_CHAR"):
        cvor.tip = Tip("CHAR", False, False, 0)
    elif(ime == "KR_INT"):
        cvor.tip = Tip("INT", False, False, 0)
    return cvor

def multiplikativni_izraz(cvor):
    ##print 'multiplikativni_izraz'
    dijete = cvor.listaDjece[0]
    ##print 'kmiz'
    if(dijete.naziv == "<cast_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = cast_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
    elif(dijete.naziv == "<multiplikativni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = multiplikativni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
        
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = cast_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #? cetvrti korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
        
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def aditivni_izraz(cvor):
    ##print 'aditivni_izraz'
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<multiplikativni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = multiplikativni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<aditivni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = aditivni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #drugi korak???
        if(not(dijete.tip.implicitnoINT())):
            #print dijete.tip.tip
            #print dijete.tip.jeNiz
            #print dijete.tip.parametri
            ispisiGresku(cvor)
        
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = multiplikativni_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def odnosni_izraz(cvor):
    ##print 'odnosni_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<aditivni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = aditivni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<odnosni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = odnosni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = aditivni_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def jednakosni_izraz(cvor):
    ##print 'jednakosni_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<odnosni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = odnosni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<jednakosni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = jednakosni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = odnosni_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def bin_i_izraz(cvor):
    ##print 'bin_i_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<jednakosni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = jednakosni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<bin_i_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_i_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = jednakosni_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def bin_xili_izraz(cvor):
    ##print 'bin_xili_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<bin_i_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_i_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<bin_xili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_xili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = bin_i_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def bin_ili_izraz(cvor):
    ##print 'bin_ili_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<bin_xili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_xili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<bin_ili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_ili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = bin_xili_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def log_i_izraz(cvor):
    ##print 'log_i_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<bin_ili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = bin_ili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<log_i_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = log_i_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = bin_ili_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def log_ili_izraz(cvor):
    ##print 'log_ili_izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<log_i_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = log_i_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<log_ili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = log_ili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        #?? drugi korak
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = log_i_izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor

def izraz_pridruzivanja(cvor):
    ##print 'izraz_pridruzivanja'
    dijete = cvor.listaDjece[0]
    ##print 'km'
    if(dijete.naziv == "<log_ili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = log_ili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<postfiks_izraz>"):
        #print 'putaaaaaa'
        dijete.tablica = cvor.tablica
        dijete = postfiks_izraz(dijete)
        
        #?? drugi korak JAKO UPITNO
        #dijete.l_izraz = 1 
        cvor.listaDjece[0] = dijete
        ##print dijete.naziv
        if(dijete.l_izraz != 1):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        dijete2 = cvor.listaDjece[0]
        if(not(pretvorbaDopustena(dijete.tip, dijete2.tip))):
            ##print 'tu'
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
        #print ')))))'
        ime = vratiVr(dijete2)
        indeks = "-1"
        if(len(dijete2.listaDjece) > 1):
            indeks = vratiVr(dijete2.listaDjece[2])
        vrijednost = vratiVr(dijete)
        #print 'smece'
        #print indeks
        #print ime
        #print vrijednost
        #print 'kraj'
        if(not isNumber(vrijednost)):
            tmp = dijete
            
            while(tmp.naziv != "<aditivni_izraz>"):
                tmp = tmp.listaDjece[0]
                
            prvi = vratiVr(tmp.listaDjece[0])
            drugi = vratiVr(tmp.listaDjece[2])
            operacija = tmp.listaDjece[1].naziv
            operacija = operacija.split(" ")
            operacija = operacija[2]
        
            if(isNumber(prvi)):
                ispis.write("\tMOVE %D " + str(prvi) + ", R0\n")
            else:
                ispis.write("\tLOAD R0, (G_" + prvi + ")\n")
            
            if(isNumber(drugi)):
                ispis.write("\tMOVE %D " + str(drugi) + ", R1\n")
            else:
                ispis.write("\tLOAD R1, (G_" + drugi + ")\n")
            
            if(operacija == "+"):    
                ispis.write("\tADD R0, R1, R0\n")
            elif(operacija == "-"):
                ispis.write("\tSUB R0, R1, R0\n")
            ispis.write("\tSTORE R0, (G_" + ime + ")\n")
        else:        
            if(indeks != "-1"):
                ispis.write("\nG_" + ime + indeks + "\tDW %D " + vrijednost + '\n')
            else:
                if(ime not in deklariraneVrijednosti):
                    #ispis.write("\nG_" + ime + "\tDW %D " + vrijednost + '\n')
                    lista_var.append(ime)
                    lista_vri.append(vrijednost)
                
                #moguce da stvara probleme
                ##print 'AAAAAAAAAAAAAAAAAAAAAA'
                ##print deklariraneVrijednosti
        
    return cvor
        
def izraz(cvor):
    ##print 'izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        ##print 'xxx'
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<izraz>"):
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[2] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = 0
    
    return cvor

def slozena_naredba(cvor):
    ##print 'slozena_naredba'
    #za nove lokalne varijable
    #cvor.tablica = Tablica(cvor.tablica)
    dijete = cvor.listaDjece[1]
    
    if(dijete.naziv == "<lista_naredbi>"):
        dijete.tablica = cvor.tablica
        dijete = lista_naredbi(dijete)
        cvor.listaDjece[1] = dijete
        #cvor.tablica = dijete.tablica ????????????
        
    elif(dijete.naziv == "<lista_deklaracija>"):
        dijete.tablica = cvor.tablica
        dijete = lista_deklaracija(dijete)
        cvor.listaDjece[1] = dijete
        
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = lista_naredbi(dijete)
        cvor.listaDjece[2] = dijete
        
    return cvor

def lista_naredbi(cvor):
    ##print 'lista_naredbi'
    ##print cvor.naziv
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<naredba>"):
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[0] = dijete
        
    elif(dijete.naziv == "<lista_naredbi>"):
        dijete.tablica = cvor.tablica
        dijete = lista_naredbi(dijete)
        cvor.listaDjece[0] = dijete
        
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[1] = dijete
        
    return cvor
        
def naredba(cvor):
    ##print 'naredba'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<slozena_naredba>"):
        #dijete.tablica = cvor.tablica
        ##print dijete.tablica
        dijete.tablica = Tablica(cvor.tablica)
        ##print dijete.tablica
        ##print '------------+++-----'
        dijete = slozena_naredba(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<izraz_naredba>"):
        dijete.tablica = cvor.tablica
        dijete = izraz_naredba(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<naredba_grananja>"):
        dijete.tablica = cvor.tablica
        dijete = naredba_grananja(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<naredba_petlje>"):
        dijete.tablica = cvor.tablica
        dijete = naredba_petlje(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<naredba_skoka>"):
        dijete.tablica = cvor.tablica
        dijete = naredba_skoka(dijete)
        cvor.listaDjece[0] = dijete
        
    return cvor

def izraz_naredba(cvor):
    ##print 'izraz_naredba'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "TOCKAZAREZ"):
        cvor.tip = Tip("INT", False, False, 0)
        
    elif(dijete.naziv == "<izraz>"):
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        
    return cvor
        

def naredba_grananja(cvor):
    ##print 'naredba_grananja'
    dijete = cvor.listaDjece[2]
    dijete.tablica = cvor.tablica
    dijete = izraz(dijete)
    cvor.listaDjece[2] = dijete
    
    vrijednost = vratiVr(dijete)
    if(isNumber(vrijednost)):
        ispis.write("\tMOVE %D " +  vrijednost + ", R0\n")
        ispis.write("\tJP_NZ LABELA\n")
    else:
        tmp = dijete
        while (tmp.naziv != "<odnosni_izraz>" or tmp.naziv != "<jednakosni_izraz>") and len(tmp.listaDjece) != 3:
            tmp = tmp.listaDjece[0]
        
        operacija = tmp.listaDjece[1].naziv
        operacija = operacija.split(" ")
        operacija = operacija[2]
        vrijednost1 = vratiVr(tmp.listaDjece[2])
        
        if(isNumber(vrijednost)):
            ispis.write("\tMOVE %D " + vrijednost + ", R1\n")
        else:
            ispis.write("\tLOAD R0, (G_" + vrijednost.upper() + ")\n")
        if(isNumber(vrijednost1)):
            ispis.write("\tMOVE %D " + vrijednost1 + ", R1\n")
        else:
            ispis.write("\tLOAD R1, (G_" + vrijednost1.upper() + ")\n")
        ispis.write("\tSUB R0, R1, R0\n")
        
        if(operacija == "<"):
            ispis.write("\tJP_UGE LABELA\n")
        elif(operacija == ">="):
            ispis.write("\tJP_ULT LABELA\n")
        elif(operacija == "=="):
            ispis.write("\tJP_NE LABELA\n")
        
        
    #????????????
    if(not(dijete.tip.implicitnoINT())):
        ispisiGresku(cvor)
            
    dijete = cvor.listaDjece[4]
    dijete.tablica = cvor.tablica
    dijete = naredba(dijete)
    cvor.listaDjece[4] = dijete
    
    ispis.write("LABELA")
        
    if(len(cvor.listaDjece) == 7):    
        dijete = cvor.listaDjece[6]
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[6] = dijete
    return cvor

def naredba_petlje(cvor):
    ##print 'naredba_petlje'
    dijete = cvor.listaDjece[0]
        
    if(dijete.naziv[0:8] == "KR_WHILE"):
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
        
        ispis.write("\nPETLJA")     
        dijete = cvor.listaDjece[4]
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[4] = dijete
        
        dijete = cvor.listaDjece[2]
        while(dijete.naziv != "<odnosni_izraz>"):
            dijete = dijete.listaDjece[0]
        
        operacija = dijete.listaDjece[1].naziv.split(" ")
        operacija = operacija[2]
        granica = vratiVr(dijete.listaDjece[2])
        iterator = vratiVr(dijete.listaDjece[0])
        
        ispis.write("\tMOVE %D " + granica + ", R0\n")
        ispis.write("\tLOAD R1, (G_" + iterator + ")\n")
        ispis.write("\tSUB R0, R1, R0\n")
        
        if(operacija == ">="):
            ispis.write("\tJP_SLE PETLJA\n")
        
    elif(dijete.naziv[0:6] == "KR_FOR"):
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = izraz_naredba(dijete)
        cvor.listaDjece[2] = dijete
        
        dijete = cvor.listaDjece[3]
        dijete.tablica = cvor.tablica
        dijete = izraz_naredba(dijete)
        cvor.listaDjece[3] = dijete
        
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[4]
        if(dijete.naziv == "<izraz>"):
            dijete.tablica = cvor.tablica
            dijete = izraz(dijete)
            cvor.listaDjece[4] = dijete
        
        
        ispis.write("\nPETLJA")    
        dijete = cvor.listaDjece[len(cvor.listaDjece) - 1]
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[len(cvor.listaDjece) - 1] = dijete
        
        dijete = cvor.listaDjece[3]
        while(dijete.naziv != "<odnosni_izraz>"):
            dijete = dijete.listaDjece[0]
        
        operacija = dijete.listaDjece[1].naziv.split(" ")
        operacija = operacija[2]
        granica = vratiVr(dijete.listaDjece[2])
        iterator = vratiVr(dijete.listaDjece[0])
        
        #print operacija
        #print granica
        ispis.write("\tMOVE %D " + granica + ", R1\n")
        ispis.write("\tLOAD R0, (G_" + iterator + ")\n")
        ispis.write("\tADD R0, %D 1, R0\n")
        ispis.write("\tSTORE R0, (G_" + iterator + ")\n")
        ispis.write("\tSUB R0, R1, R0\n")
        
        if(operacija == "<"):
            ispis.write("\tJP_ULT PETLJA\n")
    return cvor


def naredba_skoka(cvor):
    ##print 'naredba_skoka'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv[0:11] == "KR_CONTINUE" or dijete.naziv[0:8] == "KR_BREAK"):
        if(not(pronadiPetlju(cvor))):
            ispisiGresku(cvor)
    elif(dijete.naziv[0:9] == "KR_RETURN"):
        dijete = cvor.listaDjece[1]
        if(dijete.naziv[0:10] == "TOCKAZAREZ"):
            dijete.tip = Tip("VOID", False, False, 0)
            if(not(nadiFunkciju(dijete))):
                ispisiGresku(cvor)
                
        elif(dijete.naziv == "<izraz>"):
            dijete.tablica = cvor.tablica
            dijete = izraz(dijete)
            cvor.listaDjece[1] = dijete
            
            #??????
            #provjeriti nekako parametre
            
            if(not(nadiFunkciju(dijete))):
                ispisiGresku(cvor)
            
            ##print '=================='
            ##print dijete.tip.tip
            ##print dijete.tip.parametri
            if(dijete.tip.parametri != 0):
                if(not(provjeriPozvano(dijete))):
                    ispisiGresku(cvor)
                    
            vrijednost = vratiVrijednost(dijete)
            ispis.write("\tRET\n")
    return cvor
    
def prijevodna_jedinica(cvor):
    ##print 'prijevodna_jedinica'
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<vanjska_deklaracija>"):
        dijete.tablica = cvor.tablica
        dijete = vanjska_deklaracija(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<prijevodna_jedinica>"):
        dijete.tablica = cvor.tablica
        dijete = prijevodna_jedinica(dijete)
        cvor.listaDjece[0] = dijete
        
        #HUEHUE
        
        dijete = cvor.listaDjece[1]
        dijete2 = cvor.listaDjece[0]
        dijete.tablica = dijete2.tablica
        dijete = vanjska_deklaracija(dijete)
        cvor.listaDjece[1] = dijete
        
    return cvor

def vanjska_deklaracija(cvor):
    #????
    ##print 'vanjska_deklaracija'
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<definicija_funkcije>"):
        dijete.tablica = cvor.tablica
        dijete = definicija_funkcije(dijete)
        cvor.listaDjece[0] = dijete
    elif(dijete.naziv == "<deklaracija>"):
        dijete.tablica = cvor.tablica
        dijete = deklaracija(dijete)
        cvor.listaDjece[0] = dijete
        
    return cvor

        
def definicija_funkcije(cvor):
    ##print 'definicija_funkcije'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    
    cvor.listaDjece[0] = dijete
    
    
    tmp = cvor.listaDjece[1]
    im = tmp.naziv.split(" ")
    im = im[2]
    ispis.write("\nF_" + im.upper())
    if(dijete.tip.jeKonst):
        ispisiGresku(cvor)
        
    #3.korak ???
    dijete = cvor.listaDjece[1]
    ime = dijete.naziv.split(" ")
    ime = ime[2]
    
    for fun in listaDefiniranihFunkcija:
        if(fun.ime == ime):
            ispisiGresku(cvor)
    #provjeriti ime
    
    if(cvor.listaDjece[3].naziv[0:7] == "KR_VOID"):
        #4.korak ??
        #provjeriti da su deklaracija i definicija iste
        dijete = cvor.listaDjece[0]
        parametar = Tip("VOID", False, False, 0)
        tip = Tip(dijete.tip.tip,dijete.tip.jeNiz,dijete.tip.jeKonst,[parametar])
        if((deklariranoGlobalno(cvor.tablica, ime, tip)) < 0):
            ##print 'bl'
            ispisiGresku(cvor)
            
        #5.korak
        cvor.tablica.dodaj_u_tablicu(ime, tip)
        podatak = podatakTablica(ime, tip)
        listaDefiniranihFunkcija.append(podatak)
        #TREABA JOS TABLICA DEKLARACIJA!
    
        dijete = cvor.listaDjece[5]
        #dijete.tablica = cvor.tablica
        ##print '--------------'
        ##print cvor.tablica.lista
        dijete.tablica = Tablica(cvor.tablica)
        dijete = slozena_naredba(dijete)
        cvor.listaDjece[5] = dijete
    
    elif(cvor.listaDjece[3].naziv == "<lista_parametara>"):
        #4.korak
        dijete = cvor.listaDjece[3]
        dijete.tablica = cvor.tablica
        dijete = lista_parametara(dijete)
        cvor.listaDjece[3] = dijete
        
        #5. korak
        dijete = cvor.listaDjece[0]
        dijete2 = cvor.listaDjece[3] #parametri nekako unutra???
        #parametar = Tip("VOID", False, False, 0)
        tip = Tip(dijete.tip.tip,dijete.tip.jeNiz,dijete.tip.jeKonst, dijete2.tipovi)
        if((deklariranoGlobalno(cvor.tablica, ime, tip)) < 0):
            ispisiGresku(cvor)
        
        #6.korak
        cvor.tablica.dodaj_u_tablicu(ime, tip)
        podatak = podatakTablica(ime, tip)
        listaDefiniranihFunkcija.append(podatak)
        #U GLOBALNU!
        
        dijete = cvor.listaDjece[5]
        ##print '###############'
        ##print cvor.tablica
        ##print dijete.tablica
        dijete.tablica = Tablica(cvor.tablica)
        ##print '------------'
        ##print cvor.listaDjece[3].imena
        for i in range(0, len(cvor.listaDjece[3].tipovi)):
            dijete.tablica.dodaj_u_tablicu(cvor.listaDjece[3].imena[i], cvor.listaDjece[3].tipovi[i])
        dijete = slozena_naredba(dijete)
        cvor.listaDjece[5] = dijete
        
    return cvor
       
def lista_parametara(cvor):
    ##print 'lista_parametara'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<deklaracija_parametra>"):
        dijete.tablica = cvor.tablica
        dijete = deklaracija_parametra(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tipovi = [dijete.tip]
        cvor.imena = [dijete.ime]
    
    elif(dijete.naziv == "<lista_parametara>"):
        dijete.tablica = cvor.tablica
        dijete = lista_parametara(dijete)
        cvor.listaDjece[0] = dijete
        
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = deklaracija_parametra(dijete)
        cvor.listaDjece[2] = dijete
        dijete2 = cvor.listaDjece[0]
        
        for ime in dijete2.imena:
            if(dijete.ime == ime):
                ispisiGresku(cvor)
        
        for tip in dijete2.tipovi:
            cvor.tipovi.append(tip)
            
        cvor.tipovi.append(dijete.tip)
        
        for ime in dijete2.imena:
            cvor.imena.append(ime)
            
        cvor.imena.append(dijete.ime)
        
    return cvor

def deklaracija_parametra(cvor):
    ##print 'deklaracija_parametra'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    cvor.listaDjece[0] = dijete
    
    if(dijete.tip.tip == "VOID"):
        ispisiGresku(cvor)
    
    dijete = cvor.listaDjece[1]
    ime = dijete.naziv.split(" ")
    ime = ime[2]
    
    ##print '+++++++++++'
    ##print ime
    cvor.ime = ime
    dijete = cvor.listaDjece[0]
    if(len(cvor.listaDjece) == 2):
        cvor.tip = dijete.tip
    else:
        cvor.tip = Tip(dijete.tip.tip, True, dijete.tip.jeKonst, dijete.tip.parametri)
        
    return cvor

def lista_deklaracija(cvor):
    ##print 'lista_deklaracija'
    dijete = cvor.listaDjece[0]
    
    
    if(dijete.naziv == "<deklaracija>"):
        dijete.tablica = cvor.tablica
        dijete = deklaracija(dijete)
        cvor.listaDjece[0] = dijete
    
    elif(dijete.naziv == "<lista_deklaracija>"):
        dijete.tablica = cvor.tablica
        dijete = lista_deklaracija(dijete)
        cvor.listaDjece[0] = dijete
        
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = deklaracija(dijete)
        cvor.listaDjece[0] = dijete
        
    return cvor

def deklaracija(cvor):
    ##print 'deklaracija'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    cvor.listaDjece[0] = dijete
    
    dijete = cvor.listaDjece[1]
    dijete.tablica = cvor.tablica
    dijete.ntip = cvor.listaDjece[0].tip
    ##print cvor.listaDjece[0].tip.tip
    ##print '+++++'
    dijete = lista_init_deklaratora(dijete)
    ##print '-----------------'
    ##print cvor.listaDjece[0].tip
    #dijete.ntip = cvor.listaDjece[0].tip
    cvor.listaDjece[1] = dijete
    
    return cvor

def lista_init_deklaratora(cvor):
    ##print 'lista_init_deklaratora'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<init_deklarator>"):
        dijete.tablica = cvor.tablica
        dijete.ntip = cvor.ntip
        dijete = init_deklarator(dijete)
        #dijete.ntip = cvor.ntip
        cvor.listaDjece[0] = dijete
    
    elif(dijete.naziv == "<lista_init_deklaratora>"):
        dijete.tablica = cvor.tablica
        dijete.ntip = cvor.ntip
        dijete = lista_init_deklaratora(dijete)
        #dijete.ntip = cvor.ntip
        cvor.listaDjece[0] = dijete
        
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete.ntip = cvor.ntip
        dijete = init_deklarator(dijete)
        #dijete.ntip = cvor.ntip
        cvor.listaDjece[2] = dijete
        
    return cvor

def init_deklarator(cvor):
    ##print 'init_deklarator'
    dijete = cvor.listaDjece[0]
    
    dijete.tablica = cvor.tablica
    dijete.ntip = cvor.ntip
    dijete = izravni_deklarator(dijete)
    #dijete.ntip = cvor.ntip
    cvor.listaDjece[0] = dijete
    ime = dijete.listaDjece[0].naziv.split(" ")
    ime = ime[2].upper()
    
    if(len(cvor.listaDjece) == 1):
        ###print dijete.tip.jeNiz
        ##print dijete.tip
        if(dijete.tip.jeKonst):
            ispisiGresku(cvor)
        """if(dijete.tip.jeNiz):
            ##print 'tu2'
            ispisiGresku(cvor)"""
    elif(len(cvor.listaDjece) == 3):
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = inicijalizator(dijete)
        cvor.listaDjece[2] = dijete
        
        dijete2 = cvor.listaDjece[0]
        if(not(dijete2.tip.jeNiz)):
            ##print '$$$$$$$$$$$$$$$'
            ##print dijete2.tip.tip
            ##print dijete2.tip.parametri
            ##print dijete.tip.tip
            ##print dijete.tip.parametri
            if(not(pretvorbaDopustena(dijete.tip, dijete2.tip))):
                ispisiGresku(cvor)
                
            if(dijete.tip.parametri != 0):
                if(not(provjeriPozvano(dijete))):
                    ispisiGresku(cvor)
            
        elif(dijete2.tip.jeNiz):
            #????
            ##print dijete.br_elem
            ##print dijete2.br_elem
            ##print len(dijete2.tipovi)
            if(dijete.br_elem <= dijete2.br_elem):
                for i in range(0, len(dijete.tipovi)):
                    if(not(pretvorbaDopustena(dijete.tipovi[i], dijete2.tip))):
                        ispisiGresku(cvor)
            else:
                ispisiGresku(cvor)
        else:
            #??
            ispisiGresku(cvor)
        
        if(cvor.prethodni.prethodni.prethodni.prethodni.naziv == "<prijevodna_jedinica>" or cvor.prethodni.prethodni.prethodni.prethodni.prethodni.naziv == "<prijevodna_jedinica>"):
            if(len(dijete.listaDjece) == 3):
                pom = dijete.prethodni
                pom = pom.listaDjece[0]
                brojClanova = pom.listaDjece[2].naziv
                brojClanova = brojClanova.split(" ")
                brojClanova = int(brojClanova[2])
                nazivPolja = pom.listaDjece[0].naziv
                nazivPolja = nazivPolja.split(" ")
                nazivPolja = nazivPolja[2]
                dijete = dijete.listaDjece[1]
                vrijednost = vratiVr(dijete.listaDjece[0])
                #print dijete.naziv
                #print '4444444'
                #print vrijednost
                #print brojClanova
                
                listaVrijednosti = []
                while dijete.naziv != "<primarni_izraz>":
                    if(dijete.naziv == "<lista_izraza_pridruzivanja>" and len(dijete.listaDjece) == 3):
                        vrijednost = vratiVr(dijete.listaDjece[2])
                        listaVrijednosti.append(vrijednost)
                    dijete = dijete.listaDjece[0]
                
                vrijednost = vratiVr(dijete)
                listaVrijednosti.append(vrijednost)
                
                #print listaVrijednosti
                
                for i in range(0, len(listaVrijednosti)):
                    if(i == 0):
                        ispis.write("\n")
                    #ispis.write("G_" + nazivPolja.upper() + str(i) + "\tDW %D " + str(listaVrijednosti[brojClanova-i-1]) +"\n")
                    lista_var.append(nazivPolja.upper+str(i))
                    lista_vri.append(str(listaVrijednosti[brojClanova-i-1]))
                    
            else:    
                vrijednost = vratiVr(dijete)
                ispis.write("\nG_" + ime + "\tDW %D " + vrijednost +"\n")
                deklariraneGlobalno[ime] = 0
        else:
            tmp = dijete
            vrijednost = None
            while tmp.naziv != "<aditivni_izraz>":
                tmp = tmp.listaDjece[0]
            if(len(tmp.listaDjece) == 3):
                vrijednost1 = vratiVr(tmp.listaDjece[0])
                vrijednost2 = vratiVr(tmp.listaDjece[2])
                
                if(vrijednost1 in deklariraneVrijednosti):
                    vrijednost1 = deklariraneVrijednosti[vrijednost1]
                    
                if(vrijednost2 in deklariraneVrijednosti):
                    vrijednost2 = deklariraneVrijednosti[vrijednost2]
                    
                vrijednost = str(int(vrijednost1) + int(vrijednost2))
                lista_var.append(ime)
                lista_vri.append(vrijednost)
                #ispis.write("\nG_" + ime +"\tDW %D " + vrijednost +"\n")
            else:
                vrijednost = vratiVr(dijete)

                if(ime in deklariraneGlobalno):
                    deklariraneGlobalno[ime] += 1
                    ponavljanje = deklariraneGlobalno[ime]
                    lista_var.append(ime+str(ponavljanje))
                    lista_vri.append(vrijednost)
                    #ispis.write("\nG_" + ime + str(ponavljanje) + "\tDW %D " + vrijednost +"\n")
                else:    
                    if(vrijednost in deklariraneVrijednosti):
                        vrijednost = deklariraneVrijednosti[vrijednost]
                    lista_var.append(ime)
                    lista_vri.append(vrijednost) 
                    #ispis.write("\nG_" + ime + "\tDW %D " + vrijednost +"\n")
                
            deklariraneVrijednosti[ime] = vrijednost
    return cvor

def izravni_deklarator(cvor):
    ##print 'izravni_deklarator'
    if(len(cvor.listaDjece) > 1):
        dijete = cvor.listaDjece[2]
    
    if(len(cvor.listaDjece) == 1):
        if(cvor.ntip == "VOID"):
            ispisiGresku(cvor)
        
        dijete = cvor.listaDjece[0]
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        for i in cvor.tablica.lista:
            if(i.ime == ime):
                ispisiGresku(cvor)  #????
        
        tip = cvor.ntip
        cvor.tablica.dodaj_u_tablicu(ime, tip) #???
        cvor.tip = cvor.ntip
        ##print '----'
        ##print cvor.ntip
    
    elif(dijete.naziv[0:4] == "BROJ"):
        if(cvor.ntip == "VOID"):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[0]
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        for i in cvor.tablica.lista:
            if(i.ime == ime):
                ispisiGresku(cvor)  #????
                
        dijete = cvor.listaDjece[2]
        broj = dijete.naziv.split(" ")
        broj = broj[2]
        
        if(int(broj) <= 0 or int(broj) > 1024):
            ispisiGresku(cvor)
            
        tip = Tip(cvor.ntip.tip, True, cvor.ntip.jeKonst, cvor.ntip.parametri)
        cvor.tablica.dodaj_u_tablicu(ime, tip) #???
        
        cvor.tip = Tip(cvor.ntip.tip, True, cvor.ntip.jeKonst, cvor.ntip.parametri)
        cvor.br_elem = broj
        
    elif(dijete.naziv[0:7] == "KR_VOID"):
        ##print 'blaka blaka'
        dijete = cvor.listaDjece[0]
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        b = True
        for i in cvor.tablica.lista:
            if(i.ime == ime):
                b = False
                if(i.tip.tip != ntip):
                    ispisiGresku(cvor)
                else:
                    for x in i.tip.parametri:
                        if x.tip != "VOID":
                            ispisiGresku(cvor)
                cvor.tip = i.tip
        
        if(b):
            parametar = Tip("VOID", False, False, 0)
            tip = Tip(cvor.ntip.tip, False, cvor.ntip.jeKonst, [parametar])
            cvor.tablica.dodaj_u_tablicu(ime, tip) #???
            podatak = podatakTablica(ime, tip)
            listaDeklariranihFunkcija.append(podatak)
            cvor.tip = tip
        #????
            
    elif(dijete.naziv == "<lista_parametara>"):
        dijete.tablica = cvor.tablica
        dijete = lista_parametara(dijete)
        cvor.listaDjece[2] = dijete
        
        dijete = cvor.listaDjece[0]
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        dijete = cvor.listaDjece[2]
        b = True
        for i in cvor.tablica.lista:
            if(i.ime == ime):
                b = False
                if(i.tip.tip != ntip):
                    ispisiGresku(cvor)
                else:
                    for j in range(0, len(i.tip.parametri)):
                        if x.i.tip.parametri[j] != dijete.tip.parametri[j]:
                            ispisiGresku(cvor)
                cvor.tip = i.tip
        
        if(b):
            parametar = Tip("VOID", False, False, 0)
            tip = Tip(cvor.ntip.tip, False, cvor.ntip.jeKonst, dijete.tipovi)
            cvor.tablica.dodaj_u_tablicu(ime, tip) #???
            podatak = podatakTablica(ime, tip)
            listaDeklariranihFunkcija.append(podatak)
            cvor.tip = tip
            
    return cvor

def inicijalizator(cvor):
    ##print 'inicijalizator'
    #jako upitno??
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        
        ##print '---'
        ##print dijete.naziv
        if(dijete.tip.jeNiz):
            ime = nadiString(dijete)
            ime = ime[1:len(ime)-2]
            cvor.br_elem = len(ime) + 1
            tip = Tip("CHAR", False, False, 0)
            cvor.tipovi = []
            for i in range(0, cvor.br_elem):
                cvor.tipovi.append(tip)
        else:
            cvor.tip = dijete.tip
    elif(dijete.naziv == "L_VIT_ZAGRADA"):
        dijete = cvor.listaDjece[1]
        dijete.tablica = cvor.tablica
        dijete = lista_izraza_pridruzivanja(dijete)
        cvor.listaDjece[1] = dijete
        
        cvor.br_elem = dijete.br_elem
        cvor.tipovi = dijete.tipovi
        
    return cvor

def lista_izraza_pridruzivanja(cvor):
    ##print 'lista_izraza_pridruzivanja'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tipovi = [dijete.tip]
        cvor.br_elem = 1
        
    elif(dijete.naziv == "<lista_izraza_pridruzivanja>"):
        dijete.tablica = cvor.tablica
        dijete = lista_izraza_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        
        dijete2 = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[2] = dijete
        
        cvor.tipovi = copy.copy(dijete.tipovi)
        cvor.tipovi.append(dijete2.tip)
        cvor.br_elem = dijete.br_elem + 1
        
    return cvor

#---------------------------------------------------------------------


trenutnaRazina = 0
korijen = Cvor("", 0, None)
trenutniCvor = Cvor("", 0, None)
for red in sys.stdin:
    red = red.rstrip()
    brPraz = brojPraznih(red)
    
    if(brPraz == 0):
        korijen.naziv = red.strip()
        korijen.razina = brPraz
        trenutnaRazina = brPraz
        trenutniCvor = korijen
        continue
    
    if(brPraz > trenutnaRazina):
        cvor = Cvor(red.strip(), brPraz, trenutniCvor)
        trenutniCvor.listaDjece.append(cvor)
        trenutniCvor = cvor
        trenutnaRazina = brPraz
    else:
        trenutniCvor = korijen
        while(trenutniCvor.razina != brPraz - 1):
            trenutniCvor = trenutniCvor.listaDjece[len(trenutniCvor.listaDjece)-1]
        
        cvor = Cvor(red.strip(), brPraz, trenutniCvor)
        trenutniCvor.listaDjece.append(cvor)
        trenutniCvor = cvor
        trenutnaRazina = brPraz

#f = open("tekst.txt", 'w')
ispis = open("a.frisc", "w")
ispisStabla(korijen, 0)

###print trenutniCvor.naziv
###print trenutniCvor.prethodni.naziv

listaDefiniranihFunkcija = []
listaDeklariranihFunkcija = []
globalniDjelokrug = []
globalneVarijable = []
deklariraneVrijednosti = {}
deklariraneGlobalno = {}
lista_var = []
lista_vri = []

ispis.write("\tMOVE 40000, R7\n\tCALL F_MAIN\n\tHALT\n")
korijen.tablica = Tablica(None)G
korijen = prijevodna_jedinica(korijen)

for i in range(len(lista_var)):
	ispis.write("G_"+lista_var[i]+"\tDW %D "+str(lista_vri[i])+"\n")

#print globalniDjelokrug
"""if(not(provjeriMain(korijen))):
    #print 'main'
    sys.exit(0)
    
if(not(sveDeklarirane(korijen.tablica))):
    #print 'funkcija'
    sys.exit(0)"""
