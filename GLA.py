#!/usr/bin/env python
import os.path

class ParStanja:
    def __init__(self):
        self.lijevo_stanje = None
        self.desno_stanje = None
        

class Automat:
    def __init__(self, ):
        self.br_stanja = 0
        self.prijelazi = []
        self.naziv_stanja = 'a'
        self.lista_stanja = []
        self.stanje_analizatora = None
        self.akcije = []
        self.prihvatljivo_stanje = None
        

def razdvojiNiz(znakovniNiz):
    #U akcijama razdvaja <imeStanja> i regularniIzraz
    #Vraca listu sa dva stringa
    i = 0
    while(znakovniNiz[i] is not '>'):
        i += 1
    vratiNiz = []
    vratiNiz.append(znakovniNiz[1:i])
    vratiNiz.append(znakovniNiz[i+1:len(znakovniNiz)])
    return vratiNiz    

def novo_stanje(automat):
    #Funkcija stvara novo stanje za automat nekog regularnog izraza
    automat.br_stanja = automat.br_stanja + 1 
    return automat.br_stanja - 1

def je_operator(izraz, i):
    #Funkcija provjerava ima li operator svoje znacenje ili prefiksiran neparnim brojem znakova \
    #Funkcija vraca bool
    br = 0
    while((i-1) >= 0 and izraz[i-1] == '\\'):
        br = br + 1
        i = i - 1
    if(br%2 == 0):
        return True
    else:
        return False

def razdvojiViticaste(niz):
    otvorena = 0
    zatvorena = 0
    promjena = 0
    zadnjaPromjena = 0
    ispis = ""
    for i in range(0, len(niz)):
        if(niz[i] == '{' and je_operator(niz, i)):
            ispis += niz[zatvorena:i]
            otvorena = i
        elif(niz[i] == '}' and je_operator(niz, i)):
            ispis += '(' + regIzrazi[niz[otvorena:i+1]] + ')'
            zatvorena = i+1
            promjena = 1
    ispis += niz[zatvorena:len(niz)+1]
    return ispis
    """for i in range(0, len(pomRazdvajanje)):
        for j in range(0, len(pomRazdvajanje[i])):
            if(pomRazdvajanje[i][j] == '{' and jest_ime(pomRazdvajanje[i], j-1)):
                novi += pomRazdvajanje[i][zatvorenaZagrada:j]
                otvorenaZagrada = j
            elif(pomRazdvajanje[i][j] == '}' and jest_ime(pomRazdvajanje[i], j-1)):
                novi += '(' + regIzrazi[pomRazdvajanje[i][otvorenaZagrada:j+1]] + ')'
                zatvorenaZagrada = j+1
                promjena = 1
        
        novi += pomRazdvajanje[i][zatvorenaZagrada:len(pomRazdvajanje[i])+1]
        pomRazdvajanje[i] = novi
        novi = ""
        zatvorenaZagrada = 0
                
    if promjena == 1:
        citajRed[1] = ""
        for i in range(0, len(pomRazdvajanje)):
            if (i != len(pomRazdvajanje)-1):
                citajRed[1] += pomRazdvajanje[i] + '|'
            else:
                citajRed[1] += pomRazdvajanje[i]
                
    regIzrazi[citajRed[0]] = citajRed[1]
    citajRed = raw_input()"""

    
def pronadiZatvorenu(izraz, pocetakTrazenja):
    #Funkcija trazi odgovaraju zatvorenu zagradu otvorenoj zagradi u zadanom nizu
    #Funckcija vraca poziciju zatvorene zagrade
    j = pocetakTrazenja
    brojOtvorenih = 0
        
    while(True):
        if(izraz[j] == '('):
            brojOtvorenih += 1
        elif(izraz[j] == ')'):
            brojOtvorenih -= 1
        if(brojOtvorenih == 0):
            return j
        j += 1
        
    return j

def dodaj_epsilon_prijelaz(automat, lijevo_stanje, desno_stanje):
    #Funkcija dodaje epsilon prijelaz u automat
    automat.prijelazi.append(automat.naziv_stanja + str(lijevo_stanje) + ',$->' + automat.naziv_stanja + str(desno_stanje))
    
def dodaj_prijelaz(automat, lijevo_stanje, desno_stanje, prijelazni_znak):
    #Funkcija dodaje prijelaz u automat
    automat.prijelazi.append(automat.naziv_stanja + str(lijevo_stanje) + ',' + prijelazni_znak + '->' + automat.naziv_stanja + str(desno_stanje))

def dodaj_u_Listustanja(automat, broj):
    #Funkcija automatu u listu svih stanja dodaje novo stanje
    automat.lista_stanja.append(automat.naziv_stanja + str(broj))
    
def pretvori(izraz, automat):
    #Funkcija pretvara regularni izraz u automat
    izbori = []
    br_zagrada = 0
    zadnjiOperatorIzbora = 0
    for i in range(0, len(izraz)):
        if(izraz[i]=='(' and je_operator(izraz, i)):
            br_zagrada = br_zagrada + 1
        elif(izraz[i]==')' and je_operator(izraz, i)):
            br_zagrada = br_zagrada - 1
        elif(br_zagrada==0 and izraz[i]=='|' and je_operator(izraz, i)):
            izbori.append(izraz[zadnjiOperatorIzbora:i]) #grupiraj lijevi negrupirani dio niza znakova izraz u niz izbori
            zadnjiOperatorIzbora = i + 1

    if(len(izbori) > 0):
        izbori.append(izraz[zadnjiOperatorIzbora: len(izraz)])

    lijevo_stanje = novo_stanje(automat)
    desno_stanje = novo_stanje(automat)
    if(len(izbori) > 0):   #ako je pronaden barem jedan operator izbora
        for i in range(0, len(izbori)):
            privremeno = ParStanja()
            privremeno = pretvori(izbori[i], automat) #treba vratiti objekt ParStanja
            dodaj_epsilon_prijelaz(automat, lijevo_stanje, privremeno.lijevo_stanje)
            dodaj_u_Listustanja(automat, lijevo_stanje)
            dodaj_u_Listustanja(automat, privremeno.lijevo_stanje)
            dodaj_epsilon_prijelaz(automat, privremeno.desno_stanje, desno_stanje)
            dodaj_u_Listustanja(automat, privremeno.desno_stanje)
            dodaj_u_Listustanja(automat, desno_stanje)
    else:
        prefiksirano = False
        zadnje_stanje = lijevo_stanje
        i = 0
        while (i < len(izraz)):
            #print izraz + ',' + izraz[i] + ',' + str(i)
            if(prefiksirano is True):
                #slucaj 1
                prefiksirano = False
                if (izraz[i] == 't'):
                    prijelazni_znak = '\\t'
                elif (izraz[i] == 'n'):
                    prijelazni_znak = '\\n' #PROVJERITI DA LI JE OK
                elif (izraz[i] == '_'):
                    prijelazni_znak = ' '
                else:
                    prijelazni_znak = izraz[i]
                
                #a, b su integeri
                a = novo_stanje(automat)
                b = novo_stanje(automat)
                dodaj_prijelaz(automat, a, b, prijelazni_znak)
                dodaj_u_Listustanja(automat, a)
                dodaj_u_Listustanja(automat, b)
            else:
                #slucaj 2
                if (izraz[i] == '\\'): #upitno isto da li treba promjenit
                    #print "da"
                    prefiksirano = True
                    i = i + 1
                    continue #nastavi for petlju
                if (izraz[i] != '('):
                    #slucaj 2a
                    a = novo_stanje(automat)
                    b = novo_stanje(automat)
                    if(izraz[i] == '$'):
                        dodaj_epsilon_prijelaz(automat, a, b)
                        dodaj_u_Listustanja(automat, a)
                        dodaj_u_Listustanja(automat, b)
                    else:
                        dodaj_prijelaz(automat, a, b, izraz[i])
                        dodaj_u_Listustanja(automat, a)
                        dodaj_u_Listustanja(automat, b)
                else:
                    # slucaj 2b
                    j = pronadiZatvorenu(izraz, i)
                    privremeno = ParStanja()
                    privremeno = pretvori(izraz[i+1:j], automat)
                    a = privremeno.lijevo_stanje
                    b = privremeno.desno_stanje
                    i = j

            #provjera ponavljanja
            if((i+1) < len(izraz) and izraz[i+1]=='*'):
                x = a
                y = b
                a = novo_stanje(automat)
                b = novo_stanje(automat)
                dodaj_epsilon_prijelaz(automat, a, x)
                dodaj_epsilon_prijelaz(automat, y, b)
                dodaj_epsilon_prijelaz(automat, a, b)
                dodaj_epsilon_prijelaz(automat, y, x)
                dodaj_u_Listustanja(automat, a)
                dodaj_u_Listustanja(automat, b)
                dodaj_u_Listustanja(automat, x)
                dodaj_u_Listustanja(automat, y)
                i = i+1
            
            #povezivanje s ostatkom automata
            dodaj_epsilon_prijelaz(automat, zadnje_stanje, a)
            dodaj_u_Listustanja(automat, a)
            dodaj_u_Listustanja(automat, zadnje_stanje)
            zadnje_stanje = b
            i += 1
            
        dodaj_epsilon_prijelaz(automat, zadnje_stanje, desno_stanje)
        dodaj_u_Listustanja(automat, zadnje_stanje)
        dodaj_u_Listustanja(automat, desno_stanje)
    
    parstanja = ParStanja()
    parstanja.lijevo_stanje = lijevo_stanje
    parstanja.desno_stanje = desno_stanje
    return parstanja

def jest_ime(niz, polozaj):
    #Provjerava da li je regularna definicija
    if(polozaj >= len(niz)):
        return False
    else:
        if(niz[polozaj] == '\\'):
            return False
        else:
           return True
    
#tu pocinje ucitavanje
regIzrazi = {}
citajRed = raw_input()
while (citajRed[0] != '%'):
    citajRed = citajRed.split(' ')
    pomRazdvajanje = citajRed[1].split('|')
    promjena = 0
    zatvorenaZagrada = 0
    novi = ""
    for i in range(0, len(pomRazdvajanje)):
        for j in range(0, len(pomRazdvajanje[i])):
            if(pomRazdvajanje[i][j] == '{' and jest_ime(pomRazdvajanje[i], j-1)):
                novi += pomRazdvajanje[i][zatvorenaZagrada:j]
                otvorenaZagrada = j
            elif(pomRazdvajanje[i][j] == '}' and jest_ime(pomRazdvajanje[i], j-1)):
                novi += '(' + regIzrazi[pomRazdvajanje[i][otvorenaZagrada:j+1]] + ')'
                zatvorenaZagrada = j+1
                promjena = 1
        
        novi += pomRazdvajanje[i][zatvorenaZagrada:len(pomRazdvajanje[i])+1]
        pomRazdvajanje[i] = novi
        novi = ""
        zatvorenaZagrada = 0
                
    if promjena == 1:
        citajRed[1] = ""
        for i in range(0, len(pomRazdvajanje)):
            if (i != len(pomRazdvajanje)-1):
                citajRed[1] += pomRazdvajanje[i] + '|'
            else:
                citajRed[1] += pomRazdvajanje[i]
                
    regIzrazi[citajRed[0]] = citajRed[1]
    citajRed = raw_input()
#print regIzrazi

#citajRed = raw_input()
stanjaAnalizatora = citajRed.split(' ')
stanjaAnalizatora.remove('%X')
pocAnalizator = stanjaAnalizatora[0]

citajRed = raw_input()
imenaJedinki = citajRed.split(' ')
imenaJedinki.remove('%L')

listaAutomata = []
listaPrihvatljivihStanja = []
listaPocetnihStanja = []
i = 0
listaStanjaAnalizatora = []
while True:
    try:
        citajRed = raw_input() #tu je ime stanja i regularni izraz
        stanjeIzraz = razdvojiNiz(citajRed)
        imeStanja = stanjeIzraz[0] #stanje akcije
        regularniIzraz = stanjeIzraz[1] #regularni izraz za akciju
        #if(regularniIzraz in regIzrazi):
        #   regularniIzraz = regIzrazi[regularniIzraz]
        regularniIzraz = razdvojiViticaste(regularniIzraz)
        #print regularniIzraz
        automat = Automat()
        #najgluplji nacin imenovanja stanja ikad
        tmp = i
        if(i<=25):
            automat.naziv_stanja = chr(ord(automat.naziv_stanja) + i)
        else:
            while(i > 25):
                automat.naziv_stanja += 'a'
                i -= 25
            automat.naziv_stanja += chr(ord('a') + i)
        
        i = tmp
        
        automat.stanje_analizatora = imeStanja #kojem stanju treba pridru?iti automat
        par_stanja = ParStanja()
        par_stanja = pretvori(regularniIzraz, automat)
        listaAutomata.append(automat) #??
        automat.prihvatljivo_stanje = automat.naziv_stanja + str(par_stanja.desno_stanje)
        listaPrihvatljivihStanja.append(automat.naziv_stanja + str(par_stanja.desno_stanje))
        listaPocetnihStanja.append(automat.naziv_stanja + str(par_stanja.lijevo_stanje))
        listaAutomata[i].lista_stanja = list(set(listaAutomata[i].lista_stanja))
        listaAutomata[i].lista_stanja.sort()
        automat.prijelazi.append(automat.stanje_analizatora + ',$->' + automat.naziv_stanja + str(par_stanja.lijevo_stanje)) #dodajemo epsilon prijelaz iz stanja analizatora
        if automat.stanje_analizatora not in listaStanjaAnalizatora:
            listaStanjaAnalizatora.append(automat.stanje_analizatora)
        automat.prijelazi.sort()
        while(citajRed != '}'):
            citajRed = raw_input() #treba smislit sta sa akcijama
            automat.akcije.append(citajRed)
        i += 1
    except (EOFError):
        break

#path = "./analizator"
#completeName = os.path.join(path, "automat.txt")
#f = open(completeName,'w')
f = open("automat.txt", 'w')
f.write("pocetno_stanje,") #Dodajemo novo pocetno stanje u definiciju automata
for i in range(0, len(listaAutomata)): #Ispisujemo sva ostala stanja
    for j in range(0, len(listaAutomata[i].lista_stanja)):
        if(j != len(listaAutomata[i].lista_stanja) and i != len(listaAutomata)):
            f.write(listaAutomata[i].lista_stanja[j] + ',')
        else:
            f.write(listaAutomata[i].lista_stanja[j]) #Zbog zadnjeg stanja

for i in range(0, len(listaStanjaAnalizatora)):
    f.write(listaStanjaAnalizatora[i] + ',')
    
f.write("\npocetno_stanje\n") #Ispisujemo pocetno stanje

for i in range(0, len(listaPrihvatljivihStanja)): #Ispisujemo prihvatljiva stanja
    if(i != len(listaPrihvatljivihStanja)-1):
        f.write(listaPrihvatljivihStanja[i] + ',')
    else:
        f.write(listaPrihvatljivihStanja[i]) #zadnji zarez


f.write("\npocetno_stanje,$->" + pocAnalizator + '\n') #prijelaz u pocetno stanje analizatora

for i in range(0, len(listaAutomata)): #dodajemo ostale prijelaze
    for j in range(0, len(listaAutomata[i].prijelazi)):
        f.write(listaAutomata[i].prijelazi[j] + '\n') #pazi zadnji red! i /n NE ZELI ISPISATI
        
f.write("%\n")
for i in range(0, len(listaAutomata)):
    f.write(listaAutomata[i].prihvatljivo_stanje + '\n')
    for j in range(0, len(listaAutomata[i].akcije)):
        f.write(listaAutomata[i].akcije[j] + '\n')

f.write('%')
f.close() # you can omit in most cases as the destructor will call if   
