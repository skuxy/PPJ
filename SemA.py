#!/usr/bin/env python
import sys
from time import sleep
import copy

class Tip():
    def __init__(self, tip, jeNiz, jeKonst, parametri):
        self.tip = tip
        self.jeNiz = jeNiz
        self.jeKonst = jeKonst
        self.parametri = parametri
        
    def implicitnoINT(self):
        if((self.tip == "INT" or self.tip == "CHAR") and (self.jeNiz == False) and (self.parametri == 0)):
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
    f.write(' '*praznina + korijen.naziv + '\n')
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
        print tablica.lista
        for zapis in tablica.lista:
            
            print zapis.tip.tip
            print zapis.ime
            print zapis.tip.parametri
            print idn
            if(zapis.ime == idn):
                return True
            
        if(tablica.prethodni != None):
            print 'ikad'
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
   # print iz.tip
   # print u.tip
   # print 'fdsfsdfsdfs'
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
    #print pretvorbaDopustena(cvor.tip, pom.tip)
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
            
    print ispis
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
    while tablica.prethodni != None:
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
    
#-----------------------------------------------------------------------

def primarni_izraz(cvor):
    print 'primarni_izraz'
    dijete = cvor.listaDjece[0]
    print dijete.naziv
    
    if(dijete.naziv[0:3] == "IDN"):
        #???????????
        ime = dijete.naziv.split(" ")
        ime = ime[2]
        
        dijete.tablica = cvor.tablica
        if(provjeriDeklarirano(dijete.tablica, ime)):
            #????
            print 'PICKMA MATERINA'
            print ime
            cvor.tip = vratiIdentifikator(dijete.tablica, ime)
            print cvor.tip
            if(cvor.tip == None):
                for fun in listaDefiniranihFunkcija:
                    if fun.ime == ime:
                        cvor.tip = fun.tip
            print 'weeeeee'
            print cvor.tip.tip
            print cvor.tip.parametri
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
            print 'vr1'
        else:
            ispisiGresku(cvor)
        
    elif(dijete.naziv[0:11] == "NIZ_ZNAKOVA"):
        print 'BLALALALALLALALALLA'
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
    print 'postfiks_izraz'
    dijete = cvor.listaDjece[0]
    print len(cvor.listaDjece)
    
    if(dijete.naziv == "<primarni_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = primarni_izraz(dijete)
        cvor.listaDjece[0] = dijete
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        #print dijete.tip.tip
        
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
                print '---'
                print x.naziv"""
            
            print dijete.tipovi
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
    print 'lista_argumenata'
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
        
        print cvor.tipovi
        cvor.tipovi.append(dijete2.tip)
        print '#####################'
        print cvor.tipovi
        
    return cvor
        
def unarni_izraz(cvor):
    print 'unarni_izraz'
    dijete = cvor.listaDjece[0]
    print dijete.naziv
    
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
    print 'cast_izraz'
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
        print dijete.tip.tip
        print dijete.tip.jeNiz
        print dijete.tip.jeKonst
        print dijete2.tip.tip
        print dijete2.tip.jeNiz
        print dijete2.tip.jeKonst
        print '+++++++++++++++'
        if(not(provjeriCast(dijete2.tip, dijete.tip))):
            print 'tu'
            ispisiGresku(cvor) #valjda?
        
        #cvor.tip = dijete.tip
        cvor.tip = Tip(dijete.tip.tip, dijete.tip.jeNiz, dijete.tip.jeKonst, dijete2.tip.parametri)
        cvor.l_izraz = 0 
        
    return cvor

def ime_tipa(cvor):
    print 'ime_tipa'
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
    print 'specifikator_tipa'
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
    print 'multiplikativni_izraz'
    dijete = cvor.listaDjece[0]
    print 'kmiz'
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
    print 'aditivni_izraz'
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
    print 'odnosni_izraz'
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
    print 'jednakosni_izraz'
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
    print 'bin_i_izraz'
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
    print 'bin_xili_izraz'
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
    print 'bin_ili_izraz'
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
    print 'log_i_izraz'
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
    print 'log_ili_izraz'
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
    print 'izraz_pridruzivanja'
    dijete = cvor.listaDjece[0]
    print 'km'
    if(dijete.naziv == "<log_ili_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = log_ili_izraz(dijete)
        cvor.listaDjece[0] = dijete
        
        cvor.tip = dijete.tip
        cvor.l_izraz = dijete.l_izraz
        
    elif(dijete.naziv == "<postfiks_izraz>"):
        dijete.tablica = cvor.tablica
        dijete = postfiks_izraz(dijete)
        
        #?? drugi korak JAKO UPITNO
        #dijete.l_izraz = 1 
        cvor.listaDjece[0] = dijete
        print dijete.naziv
        if(dijete.l_izraz != 1):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[2]  
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[2] = dijete
        
        #???
        dijete2 = cvor.listaDjece[0]
        if(not(pretvorbaDopustena(dijete.tip, dijete2.tip))):
            print 'tu'
            ispisiGresku(cvor)
            
        cvor.tip = Tip("INT", False, False, 0)
        cvor.l_izraz = 0
        
    return cvor
        
def izraz(cvor):
    print 'izraz'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        print 'xxx'
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
    print 'slozena_naredba'
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
    print 'lista_naredbi'
    print cvor.naziv
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
    print 'naredba'
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<slozena_naredba>"):
        #dijete.tablica = cvor.tablica
        print dijete.tablica
        dijete.tablica = Tablica(cvor.tablica)
        print dijete.tablica
        print '------------+++-----'
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
    print 'izraz_naredba'
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
    print 'naredba_grananja'
    dijete = cvor.listaDjece[2]
    dijete.tablica = cvor.tablica
    dijete = izraz(dijete)
    cvor.listaDjece[2] = dijete
        
    #????????????
    if(not(dijete.tip.implicitnoINT())):
        ispisiGresku(cvor)
            
    dijete = cvor.listaDjece[4]
    dijete.tablica = cvor.tablica
    dijete = naredba(dijete)
    cvor.listaDjece[4] = dijete
        
    if(len(cvor.listaDjece) == 7):    
        dijete = cvor.listaDjece[6]
        dijete.tablica = cvor.tablica
        dijete = naredba(dijete)
        cvor.listaDjece[6] = dijete
    return cvor

def naredba_petlje(cvor):
    print 'naredba_petlje'
    dijete = cvor.listaDjece[0]
        
    if(dijete.naziv[0:8] == "KR_WHILE"):
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[2] = dijete
        
        if(not(dijete.tip.implicitnoINT())):
            ispisiGresku(cvor)
            
        dijete = cvor.listaDjece[4]
        dijete.tablica = cvor.tablica
        dijete = izraz(dijete)
        cvor.listaDjece[4] = dijete
        
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
            
        dijete = cvor.listaDjece[len(cvor.listaDjece) - 1]
        dijete.tablica = cvor.tablica
        dijete = izraz_naredba(dijete)
        cvor.listaDjece[len(cvor.listaDjece) - 1] = dijete
        
    return cvor


def naredba_skoka(cvor):
    print 'naredba_skoka'
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
            
            print '=================='
            print dijete.tip.tip
            print dijete.tip.parametri
            if(dijete.tip.parametri != 0):
                if(not(provjeriPozvano(dijete))):
                    ispisiGresku(cvor)
    return cvor
    
def prijevodna_jedinica(cvor):
    print 'prijevodna_jedinica'
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
    print 'vanjska_deklaracija'
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

def vanjska_jedinica(cvor):
    dijete = cvor.listaDjece[0]
    if(dijete.naziv == "<definicija_funkcije"):
        print 'f'
    elif(dijete.naziv == "<deklaracija>"):
        print 'b'
        
def definicija_funkcije(cvor):
    print 'definicija_funkcije'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    cvor.listaDjece[0] = dijete
    
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
            print 'bl'
            ispisiGresku(cvor)
            
        #5.korak
        cvor.tablica.dodaj_u_tablicu(ime, tip)
        podatak = podatakTablica(ime, tip)
        listaDefiniranihFunkcija.append(podatak)
        #TREABA JOS TABLICA DEKLARACIJA!
    
        dijete = cvor.listaDjece[5]
        #dijete.tablica = cvor.tablica
        print '--------------'
        print cvor.tablica.lista
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
        print '###############'
        print cvor.tablica
        print dijete.tablica
        dijete.tablica = Tablica(cvor.tablica)
        print '------------'
        print cvor.listaDjece[3].imena
        for i in range(0, len(cvor.listaDjece[3].tipovi)):
            dijete.tablica.dodaj_u_tablicu(cvor.listaDjece[3].imena[i], cvor.listaDjece[3].tipovi[i])
        dijete = slozena_naredba(dijete)
        cvor.listaDjece[5] = dijete
        
    return cvor
       
def lista_parametara(cvor):
    print 'lista_parametara'
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
    print 'deklaracija_parametra'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    cvor.listaDjece[0] = dijete
    
    if(dijete.tip.tip == "VOID"):
        ispisiGresku(cvor)
    
    dijete = cvor.listaDjece[1]
    ime = dijete.naziv.split(" ")
    ime = ime[2]
    
    print '+++++++++++'
    print ime
    cvor.ime = ime
    dijete = cvor.listaDjece[0]
    if(len(cvor.listaDjece) == 2):
        cvor.tip = dijete.tip
    else:
        cvor.tip = Tip(dijete.tip.tip, True, dijete.tip.jeKonst, dijete.tip.parametri)
        
    return cvor

def lista_deklaracija(cvor):
    print 'lista_deklaracija'
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
    print 'deklaracija'
    dijete = cvor.listaDjece[0]
    dijete.tablica = cvor.tablica
    dijete = ime_tipa(dijete)
    cvor.listaDjece[0] = dijete
    
    dijete = cvor.listaDjece[1]
    dijete.tablica = cvor.tablica
    dijete.ntip = cvor.listaDjece[0].tip
    print cvor.listaDjece[0].tip.tip
    print '+++++'
    dijete = lista_init_deklaratora(dijete)
    print '-----------------'
    print cvor.listaDjece[0].tip
    #dijete.ntip = cvor.listaDjece[0].tip
    cvor.listaDjece[1] = dijete
    
    return cvor

def lista_init_deklaratora(cvor):
    print 'lista_init_deklaratora'
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
    print 'init_deklarator'
    dijete = cvor.listaDjece[0]
    
    dijete.tablica = cvor.tablica
    dijete.ntip = cvor.ntip
    dijete = izravni_deklarator(dijete)
    #dijete.ntip = cvor.ntip
    cvor.listaDjece[0] = dijete
    
    if(len(cvor.listaDjece) == 1):
        #print dijete.tip.jeNiz
        print dijete.tip
        if(dijete.tip.jeKonst):
            ispisiGresku(cvor)
        """if(dijete.tip.jeNiz):
            print 'tu2'
            ispisiGresku(cvor)"""
    elif(len(cvor.listaDjece) == 3):
        dijete = cvor.listaDjece[2]
        dijete.tablica = cvor.tablica
        dijete = inicijalizator(dijete)
        cvor.listaDjece[2] = dijete
        
        dijete2 = cvor.listaDjece[0]
        if(not(dijete2.tip.jeNiz)):
            print '$$$$$$$$$$$$$$$'
            print dijete2.tip.tip
            print dijete2.tip.parametri
            print dijete.tip.tip
            print dijete.tip.parametri
            if(not(pretvorbaDopustena(dijete.tip, dijete2.tip))):
                ispisiGresku(cvor)
                
            if(dijete.tip.parametri != 0):
                if(not(provjeriPozvano(dijete))):
                    ispisiGresku(cvor)
            
        elif(dijete2.tip.jeNiz):
            #????
            print dijete.br_elem
            print dijete2.br_elem
            print len(dijete2.tipovi)
            if(dijete.br_elem <= dijete2.br_elem):
                for i in range(0, len(dijete.tipovi)):
                    if(not(pretvorbaDopustena(dijete.tipovi[i], dijete2.tip))):
                        ispisiGresku(cvor)
            else:
                ispisiGresku(cvor)
        else:
            #??
            ispisiGresku(cvor)
            
    return cvor

def izravni_deklarator(cvor):
    print 'izravni_deklarator'
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
        print '----'
        print cvor.ntip
    
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
        print 'blaka blaka'
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
    print 'inicijalizator'
    #jako upitno??
    dijete = cvor.listaDjece[0]
    
    if(dijete.naziv == "<izraz_pridruzivanja>"):
        dijete.tablica = cvor.tablica
        dijete = izraz_pridruzivanja(dijete)
        cvor.listaDjece[0] = dijete
        
        print '---'
        print dijete.naziv
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
    print 'lista_izraza_pridruzivanja'
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

f = open("tekst.txt", 'w')    
ispisStabla(korijen, 0)

#print trenutniCvor.naziv
#print trenutniCvor.prethodni.naziv

listaDefiniranihFunkcija = []
listaDeklariranihFunkcija = []
globalniDjelokrug = []

korijen.tablica = Tablica(None)
korijen = prijevodna_jedinica(korijen)

if(not(provjeriMain(korijen))):
    print 'main'
    sys.exit(0)
    
if(not(sveDeklarirane(korijen.tablica))):
    print 'funkcija'
    sys.exit(0)
