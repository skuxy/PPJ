__author__ = 'Mate'
import sys
import copy

def odvojiZnakove():
    vratiListu = sys.stdin.readline().rstrip().split(' ')
    vratiListu.pop(0)
    return vratiListu

def pronadiPrazneZnakove():
    prazniZnakovi = []
    for znak in nezavrsniZnakovi:
        for j in produkcijeGramatike[znak]:
            if j == '$':
                prazniZnakovi.append(znak)
    
    promjena = 1
    while promjena != 0:
        promjena = 0
        for znak in nezavrsniZnakovi:
            if znak in prazniZnakovi:
                continue
            for j in produkcijeGramatike[znak]:
                j = j.split(' ')
                neValja = 0
                for z in j:
                    if z not in prazniZnakovi:
                        neValja = 1
                        break
                if neValja == 0:
                    prazniZnakovi.append(znak)
                    promjena = 1
    return prazniZnakovi

def ZapocinjeIzravnoZnakom():
    for znak in nezavrsniZnakovi:
        zapocinjeZnakom[znak] = {}
        for produkcija in produkcijeGramatike[znak]:
            produkcija = produkcija.split(' ')
            for i in range(0, len(produkcija)):
                if produkcija[i] in prazniNezZnakovi:
                    zapocinjeZnakom[znak][produkcija[i]] = '1'
                else:
                    if produkcija[i] != '$':
                        zapocinjeZnakom[znak][produkcija[i]] = '1'
                    break

def pronadiZapocinjeZnakom():
    for znak in nezavrsniZnakovi:
        noviNezavrsni = []
        
        for okruzenje in zapocinjeZnakom[znak]:
            if okruzenje in nezavrsniZnakovi:
                noviNezavrsni.append(okruzenje)
            
        while len(noviNezavrsni) > 0:
            novi = noviNezavrsni.pop(0)
            for i in zapocinjeZnakom[novi]:
                if (i not in zapocinjeZnakom[znak]):
                    if(i in nezavrsniZnakovi):
                        noviNezavrsni.append(i)
                    zapocinjeZnakom[znak][i] = '*'
    
def napuniZapocinje():
    lista = []
    for znak in nezavrsniZnakovi:
        lista.append(znak)
    for znak in zavrsniZnakovi:
        lista.append(znak)
    for znak in lista:
        Zapocinje[znak] = []
        for okruzenje in zapocinjeZnakom[znak]:
            if okruzenje in zavrsniZnakovi:
                Zapocinje[znak].append(okruzenje)

def nadiSlijedeci(stanje, stanjeIz):
    tocka = nadiTocku(stanjeIz)
    niz = ""
    if(stanjeIz[tocka + len(stanje) + 1] != '<'):
        return niz
    for i in range(tocka + len(stanje) + 1, len(stanjeIz)):
        niz += stanjeIz[i]
        if stanjeIz[i] == '>':
            return niz
    

def nadiTocku(stanjeIz):
    for i in range(0, len(stanjeIz)):
        if stanjeIz[i] == '.':
            return i
    
def nadiOkruzenje(stanjeIz):
    novi = stanjeIz.split('{')
    okruzenje = novi[1]
    okruzenje = okruzenje[0:len(okruzenje)-1]
    okruzenje = okruzenje.split(',')
    return okruzenje
    
def napraviStanje(stanje, stanjeIz):
    if stanjeIz == '<%>':
        niz = ""
        listaStanja = []
        for prijelaz in produkcijeGramatike[stanje]:
            prijelaz = prijelaz.replace(" ", "")
            if prijelaz == '$':
                prijelaz = ''
            niz = stanje +  '->.' + prijelaz + ',{#}'
            listaStanja.append(niz)
            listaStanjaNKA.append(niz)
    else:
        niz = ""
        listaStanja = []
        for prijelaz in produkcijeGramatike[stanje]:
            prijelaz = prijelaz.replace(" ", "")
            okruzenje = nadiOkruzenje(stanjeIz)
            if prijelaz == '$':
                okruzenjeIspis = ""
                for i in range(0, len(okruzenje)):
                    if i != len(okruzenje) - 1:
                        okruzenjeIspis += okruzenje[i] + ','
                    else:
                        okruzenjeIspis += okruzenje[i]
                niz = stanje + '->.,{' + okruzenjeIspis + '}'
            else:    
                slijedeci = nadiSlijedeci(stanje, stanjeIz)
                if slijedeci in prazniNezZnakovi:
                    slijedeciOkruzenje = Zapocinje[slijedeci]
                    for i in slijedeciOkruzenje:
                        if i not in okruzenje:
                            okruzenje.append(i)
                okruzenjeIspis = ""
                for i in range(0, len(okruzenje)):
                    if i != len(okruzenje) - 1:
                        okruzenjeIspis += okruzenje[i] + ','
                    else:
                        okruzenjeIspis += okruzenje[i]
                niz = stanje + '->.' + prijelaz + ',{' + okruzenjeIspis + '}'
            if(niz not in listaStanjaNKA):
                listaStanjaNKA.append(niz)
            listaStanja.append(niz)
                
        
    return listaStanja

def nadiStanje(tocka, prijelaz):
    niz = ""
    for i in range(tocka+1, len(prijelaz)):
        niz += prijelaz[i]
        if(prijelaz[i] == '>'):
            return niz

def pomakniTocku(prijelaz):
    tocka = nadiTocku(prijelaz)
    if(prijelaz[tocka+1] == '<'):
        i = tocka + 1
        while prijelaz[i] != '>':
            i += 1
        niz = prijelaz[0:tocka] + prijelaz[tocka+1:i+1] + '.' + prijelaz[i+1:len(prijelaz)]
        return niz
    else:
        niz = ""
        i = tocka + 1
        while niz not in zavrsniZnakovi:
            niz += prijelaz[i]
            i += 1
        niz = prijelaz[0:tocka] + prijelaz[tocka+1:i] + '.' + prijelaz[i:len(prijelaz)]
        return niz

def nadiZnak(prijelaz):
    tocka = nadiTocku(prijelaz)
    if(prijelaz[tocka+1] == '<'):
        i = tocka + 1
        while prijelaz[i] != '>':
            i += 1
        return prijelaz[tocka+1:i+1]
    else:
        niz = ""
        i = tocka + 1
        while niz not in zavrsniZnakovi:
            niz += prijelaz[i]
            i += 1
        return prijelaz[tocka+1:i]
    
def pretvori(prijelaz):
    #print '-------------------a'
    #print prijelaziEpsilonNKA
    #print prijelaz
    tocka = nadiTocku(prijelaz)
    if(prijelaz[tocka+1] == '<'):
        stanje = nadiStanje(tocka, prijelaz)
        novaStanja = napraviStanje(stanje, prijelaz)
        if len(novaStanja) > 0:
            if prijelaz not in prijelaziEpsilonNKA:
                prijelaziEpsilonNKA[prijelaz] = {}
            prijelaziEpsilonNKA[prijelaz]['$'] = novaStanja
            for i in novaStanja:
                if i not in prijelaziEpsilonNKA:
                    #listaStanjaNKA.append(i)
                    pretvori(i)
    elif(prijelaz[tocka+1] == ','):
        return
    stari = prijelaz
    prijelaz = pomakniTocku(prijelaz)
    znak = nadiZnak(stari)
    if stari not in prijelaziEpsilonNKA:
        prijelaziEpsilonNKA[stari] = {}
    prijelaziEpsilonNKA[stari][znak] = [prijelaz]
    listaStanjaNKA.append(prijelaz)
    pretvori(prijelaz)

def nadiEpsilonOkruzenje(element):
    okruzenje = []
    if element not in prijelaziEpsilonNKA:
        okruzenje.append(element)
        return okruzenje
    noviElementi = []
    prijelazi = []
    okruzenje.append(element)
    noviElementi.append(element)
    while len(noviElementi) > 0:
        for i in range(0, len(noviElementi)):
            if((noviElementi[i] in prijelaziEpsilonNKA) and prijelaziEpsilonNKA[noviElementi[i]].has_key('$')):
                for j in range(0, len(prijelaziEpsilonNKA[noviElementi[i]]['$'])):
                    if (prijelaziEpsilonNKA[noviElementi[i]]['$'][j] not in prijelazi):
                        prijelazi.append(prijelaziEpsilonNKA[noviElementi[i]]['$'][j])
        
        noviElementi = []
        for i in range(0, len(prijelazi)):
            if prijelazi[i] not in okruzenje:
                okruzenje.append(prijelazi[i])
                noviElementi.append(prijelazi[i])
    
    return okruzenje 
    
nezavrsniZnakovi = odvojiZnakove()
pocetniNezavrsni = nezavrsniZnakovi[0]
#print nezavrsniZnakovi

zavrsniZnakovi = odvojiZnakove()
#print zavrsniZnakovi

sinkroZnakovi = odvojiZnakove()
#print sinkroZnakovi

produkcijeGramatike = {}
for red in sys.stdin:
    red = red.rstrip()
    if red[0] != ' ':
        if red not in produkcijeGramatike:
            produkcijeGramatike[red] = []
        zadnjiZnak = red
    else:
        red = red.strip()
        produkcijeGramatike[zadnjiZnak].append(red)

#dodajemo novi pocetni znak
produkcijeGramatike['<%>'] = [pocetniNezavrsni]
nezavrsniZnakovi.append('<%>')
#print produkcijeGramatike
#print '----------------------------'


prazniNezZnakovi = pronadiPrazneZnakove()

#print prazniNezZnakovi
#print '----------------------------'

zapocinjeZnakom = {}
ZapocinjeIzravnoZnakom()

#print zapocinjeZnakom
#print '----------------------------'

pronadiZapocinjeZnakom()
for znak in zavrsniZnakovi:
    if znak not in zapocinjeZnakom:
        zapocinjeZnakom[znak] = {}
    zapocinjeZnakom[znak][znak] = '*'
for znak in nezavrsniZnakovi:
    if znak not in zapocinjeZnakom:
        zapocinjeZnakom[znak] = {}
    zapocinjeZnakom[znak][znak] = '*'
#print zapocinjeZnakom
#print '----------------------------'


Zapocinje = {}
napuniZapocinje()

#print Zapocinje


prijelaziEpsilonNKA = {}
listaStanjaNKA = []
pomStanje = '<%>->.' + pocetniNezavrsni + ',{#}'
listaStanjaNKA.append(pomStanje)
#prijelaziEpsilonNKA['<%>']['$'] = napraviStanje(pocetniNezavrsni, '<%>')

#print prijelaziEpsilonNKA
#sys.exit(0)

pretvori(pomStanje)
#for i in prijelaziEpsilonNKA['<%>']['$']:
#    pretvori(i)

#print '----------------------------'
#print listaStanjaNKA
#print '-    -   -   -   -   -   -   -   -   '
#print prijelaziEpsilonNKA
#for i in prijelaziEpsilonNKA:
#    print i
#    print prijelaziEpsilonNKA[i]


epsilonOkruzenja = {}
for stanje in listaStanjaNKA:
    okruzenje = nadiEpsilonOkruzenje(stanje)
    epsilonOkruzenja[stanje] = okruzenje
    
#print '- - - -- - -- -- - -- - -- -- - - -- '
#print epsilonOkruzenja


#nezavrsniZnakovi.remove('<%>')
prijelaziNKA = {}
for stanje in prijelaziEpsilonNKA:
    prijelaz = []
    if stanje not in prijelaziNKA:
        prijelaziNKA[stanje] = {}
    for znak in nezavrsniZnakovi:
        #print stanje
        provjeriZa = epsilonOkruzenja[stanje]
        #print provjeriZa
        for i in provjeriZa:
            #print str(i) + '- - - -- - -- - -- - - ' + str(znak)
            if i in prijelaziEpsilonNKA and (znak in prijelaziEpsilonNKA[i]):
                #print prijelaziNKA
                for j in range(0, len(prijelaziEpsilonNKA[i][znak])):
                    #print prijelaziEpsilonNKA[i][znak]
                    #print 'tu3'
                    if prijelaziEpsilonNKA[i][znak][j] not in prijelaz:
                        prijelaz.append(prijelaziEpsilonNKA[i][znak][j])
        pomPrijelaz = set([])
        for x in prijelaz:
            okruz = epsilonOkruzenja[x]
            for y in okruz:
                pomPrijelaz.add(y)
        pomPrijelaz = list(pomPrijelaz)
        prijelaz = copy.copy(pomPrijelaz)
        #print prijelaz
        prijelaziNKA[stanje][znak] = prijelaz
        prijelaz = []
    
    prijelaz = []    
    for znak in zavrsniZnakovi:
        provjeriZa = epsilonOkruzenja[stanje]
        #print provjeriZa
        for i in provjeriZa:
            #print str(i) + '- - - -- - -- - -- - - ' + str(znak)
            if i in prijelaziEpsilonNKA and (znak in prijelaziEpsilonNKA[i]):
                #print prijelaziNKA
                for j in range(0, len(prijelaziEpsilonNKA[i][znak])):
                    #print prijelaziEpsilonNKA[i][znak]
                    #print 'tu1'
                    if prijelaziEpsilonNKA[i][znak][j] not in prijelaz:
                        #print 'tu2'
                        prijelaz.append(prijelaziEpsilonNKA[i][znak][j])
        #print prijelaz
        pomPrijelaz = set([])
        for x in prijelaz:
            okruz = epsilonOkruzenja[x]
            #print okruz
            for y in okruz:
                pomPrijelaz.add(y)
        pomPrijelaz = list(pomPrijelaz)
        prijelaz = copy.copy(pomPrijelaz)
        #print prijelaz
        prijelaziNKA[stanje][znak] = prijelaz
        prijelaz = []
    
#print "- - -- - -- - -- - - -"
#print prijelaziNKA
#print "- - -- - -- - -- - - -"


prijelaziDKA = {}
preimenuj = {}
brojac = 0
abc = pomStanje
pomStanje = '[' + pomStanje + ']'
novaStanja = [pomStanje]
#print '------------------------'
while len(novaStanja) > 0:
    pomLista = []
    for i in range(0, len(novaStanja)):
        if novaStanja[i] not in prijelaziDKA:
            prijelaziDKA[novaStanja[i]] = {}
            preimenuj[novaStanja[i]] = brojac
            brojac += 1
        novStanje = novaStanja[i]
        #print novStanje
        novStanje = novStanje[1:len(novStanje)-1]
        novStanje = novStanje.split('|')
        #novStanje = novStanje[0]
        #print novStanje
        for z in range(0, len(novStanje)):      
            for znak in nezavrsniZnakovi:
                st = ""
                #print novStanje
                #print znak
                if novStanje[z] in prijelaziNKA:
                    for j in range(0, len(prijelaziNKA[novStanje[z]][znak])):
                        #print 'tu'
                        if j == 0:
                            st += prijelaziNKA[novStanje[z]][znak][j]
                        else:
                            st += '|' + prijelaziNKA[novStanje[z]][znak][j]
                if len(st) > 0:
                    #print 'tu2'
                    st = '[' + st + ']'
                    #print st
                    prijelaziDKA[novaStanja[i]][znak] = st
                    if st not in prijelaziDKA:
                        if st not in pomLista:
                            pomLista.append(st)
    #novaStanja = copy.copy(pomLista)
    #print novaStanja
    
    #pomLista = []
    for i in range(0, len(novaStanja)):
        if novaStanja[i] not in prijelaziDKA:
            prijelaziDKA[novaStanja[i]] = {}
        novStanje = novaStanja[i]
        #print novStanje
        novStanje = novStanje[1:len(novStanje)-1]
        novStanje = novStanje.split('|')
        #novStanje = novStanje[0]
        #print novStanje
        for z in range(0, len(novStanje)):      
            for znak in zavrsniZnakovi:
                st = ""
                #print novStanje
                #print znak
                if novStanje[z] in prijelaziNKA:
                    for j in range(0, len(prijelaziNKA[novStanje[z]][znak])):
                        #print 'tu'
                        if j == 0:
                            st += prijelaziNKA[novStanje[z]][znak][j]
                        else:
                            st += '|' + prijelaziNKA[novStanje[z]][znak][j]
                if len(st) > 0:
                    #print 'tu2'
                    st = '[' + st + ']'
                    #print st
                    prijelaziDKA[novaStanja[i]][znak] = st
                    if st not in prijelaziDKA:
                        if st not in pomLista:
                            pomLista.append(st)
    novaStanja = copy.copy(pomLista)

#print '-----------------------------------'
#print prijelaziDKA

niz = ''
okruz = epsilonOkruzenja[abc]
for i in range(0, len(epsilonOkruzenja[abc])):
    if i == 0:
        niz += epsilonOkruzenja[abc][i]
    else:
        niz += '|' + epsilonOkruzenja[abc][i]

niz = '[' + niz + ']'        
#print niz

prijelaziDKA[niz] = prijelaziDKA[pomStanje]
prijelaziDKA.pop(pomStanje, None)
preimenuj[niz] = preimenuj[pomStanje]
preimenuj.pop(pomStanje, None)

#print prijelaziDKA
#print '-------------------------'
for i in prijelaziDKA:
    print i
  
#print '- -- - -- - - -------------'
#print preimenuj

kopijaPrijelaza = {}
for stanja in prijelaziDKA:
    novi = preimenuj[stanja]
    kopijaPrijelaza[novi] = {}
    for znak in prijelaziDKA[stanja]:
        pom = preimenuj[prijelaziDKA[stanja][znak]]
        kopijaPrijelaza[novi][znak] = pom
        
#print kopijaPrijelaza
#print '----------------------------------------'

pomLista = []
for i in zavrsniZnakovi:
    pomLista.append(i)
pomLista.append('#')
Akcija = {}
for stanja in prijelaziDKA:
    novi = preimenuj[stanja]
    Akcija[novi] = {}
    #print Akcija
    for znak in pomLista:
        if znak in prijelaziDKA[stanja]:
            pom = preimenuj[prijelaziDKA[stanja][znak]]
            Akcija[novi][znak] = 'Pomakni(' + str(pom) + ')'
        else:
            tmp = stanja[1:len(stanja)-1]
            tmp = tmp.split('|')
            #print st
            #print znak
            for st in tmp:
                if(st == 'q0'):
                    continue
                tocka = nadiTocku(st)
                if(st[tocka+1] == ','):
                    viticaste = st[tocka+3:len(st)-1]
                    #print viticaste
                    viticaste = viticaste.split(',')
                    if znak in viticaste:
                        pom = st.split('.')
                        pom = pom[0]
                        #print pom
                        if pom[len(pom)-1] == '>' and pom[len(pom)-2] == '-':
                           pom += '$'
                        Akcija[novi][znak] = 'Reduciraj(' + str(pom) + ')'

pomStanje = '[<%>->' + pocetniNezavrsni + '.,{#}]'
tmp = preimenuj[pomStanje]
Akcija[tmp]['#'] = 'Prihvati()'
print Akcija

NovoStanje = {}
for stanja in prijelaziDKA:
    novi = preimenuj[stanja]
    NovoStanje[novi] = {}
    for znak in nezavrsniZnakovi:
        if znak in prijelaziDKA[stanja]:
            pom = preimenuj[prijelaziDKA[stanja][znak]]
            NovoStanje[novi][znak] = 'Stavi(' + str(pom) + ')'

print '-----------------------'         
print NovoStanje

f = open("izlaz.txt", 'w')
f.write('%A\n')
for stanje in Akcija:
    f.write(str(stanje) + '\n')
    for znak in Akcija[stanje]:
        f.write(' ' + znak + '\n')
        f.write(' ' + Akcija[stanje][znak] + '\n')
        
f.write('%N\n')
for stanje in NovoStanje:
    f.write(str(stanje) + '\n')
    for znak in NovoStanje[stanje]:
        f.write(' ' + znak + '\n')
        f.write(' ' + NovoStanje[stanje][znak] + '\n')