#!/usr/bin/env python
import sys
from time import sleep

class Cvor():
    #naziv = ''
    #listaDjece = []
    
    def __init__(self, ime):
        self.naziv = ime
        self.listaDjece = []

def izbaciRazmake(red):
    red = red.split(' ')
    vrati = []
    vrati.append(red[0])
    vrati.append(red[1])
    niz = ''
    for i in range(2, len(red)):
        if i == 2:
            niz += red[i]
        else:
            niz += ' ' + red[i]
    vrati.append(niz)
    return vrati

def prebrojiZnakove(niz):
    brojac = 0
    pom = ""
    for i in range(0, len(niz)):
        pom += niz[i]
        if pom in trenutniZnakovi:
            brojac += 1
            pom = ""
    return brojac

def obavi():
    global i
    global znak
    global trenutnoStanje
    global ubaciUStanje
    
    #print '---------------------'
    #print 'na vrhu'
    #print stogParsera
    #print trenutnoStanje
    if znak in Akcije[trenutnoStanje]:
        #print 'tu'
        prijelaz = Akcije[trenutnoStanje][znak]
        #print prijelaz
        if(prijelaz[0:7] == 'Pomakni'):
            cvor = Cvor(ubaciUStanje)
            novoStanje = prijelaz.split('(')
            novoStanje = novoStanje[1][0:len(novoStanje[1])-1]
            #print novoStanje
            
            stogParsera.append(cvor)
            stogParsera.append(novoStanje)
            if znak not in trenutniZnakovi:
                trenutniZnakovi.append(znak)
            
            trenutnoStanje = novoStanje
            i += 1
            
        elif(prijelaz[0:9] == 'Reduciraj'):
            redukcija = prijelaz.split('(')
            redukcija = redukcija[1][0: len(redukcija[1])-1]
            #print redukcija
            redukcija = redukcija.split('-')
            
            noviCvor = redukcija[0]
            cvor = Cvor(noviCvor)
            
            #print redukcija
            desnaStrana = redukcija[1][1:len(redukcija[1])]
            #print desnaStrana
            #print '--------'
            brojac = prebrojiZnakove(desnaStrana)
            if desnaStrana == '$':
                pomCvor = Cvor('$')
                cvor.listaDjece.insert(0, pomCvor)
            #print desnaStrana
            #print brojac
            for j in range(0, 2*brojac):
                #print 'aaaaaaaaaaaaaaa'
                skini = stogParsera.pop(len(stogParsera) - 1)
                if j % 2 == 1:
                    cvor.listaDjece.insert(0, skini)
                    #print skini.naziv
                    #print trenutniZnakovi
                    """if skini.naziv[0] != '<':
                        tmp = izbaciRazmake(skini.naziv)
                        tmp = tmp[0]
                        trenutniZnakovi.remove(tmp)
                    else:
                        trenutniZnakovi.remove(skini.naziv)"""
            stogParsera.append(cvor)
            if noviCvor not in stogParsera:
                trenutniZnakovi.append(noviCvor)
            
            pomStanje = stogParsera[len(stogParsera) - 2]
            #print stogParsera
            #print pomStanje
            #print '---'
            #print '---------------------'
            #print stogParsera
            #print pomStanje
            #print NovoStanje
            novoStanje = NovoStanje[pomStanje][noviCvor]
            novoStanje = novoStanje.split('(')
            novoStanje = novoStanje[1][0:len(novoStanje[1])-1]
            
            stogParsera.append(novoStanje)
            trenutnoStanje = novoStanje
            
        elif(prijelaz[0:8] == 'Prihvati'):
            return 1
    else:
        while znak not in sinkroZnakovi:
            i += 1
            red = listaRedova[i]
            #ubaciUStanje = red
            red = izbaciRazmake(red)
            znak = red[0]
        
        while znak not in Akcije[trenutnoStanje]:
            stogParsera.pop(len(stogParsera)-1)
            stogParsera.pop(len(stogParsera)-1)
            trenutnoStanje = stogParsera[len(stogParsera)-1]
            
    return 0

def ispisStabla(korijen, praznina):
    print ' '*praznina + korijen.naziv
    for dijete in korijen.listaDjece:
        ispisStabla(dijete, praznina+1)
        
f = open('izlaz.txt', 'r')

citajRed = f.readline().rstrip()
sinkroZnakovi = citajRed.split(',')
#print sinkroZnakovi

citajRed = f.readline().rstrip()
citajRed = f.readline().rstrip()
Akcije = {}
while citajRed != '%N':
    if citajRed[0] != ' ':
        Akcije[citajRed] = {}
        stanje = citajRed
    else:
        citajRed = citajRed.strip()
        if citajRed[0:7] == 'Pomakni' or citajRed[0:9] == 'Reduciraj' or citajRed[0:8] == 'Prihvati':
            Akcije[stanje][znak] = citajRed
        else:
            znak = citajRed
            Akcije[stanje][znak] = ''
    citajRed = f.readline().rstrip()

#print Akcije

NovoStanje = {}
for citajRed in f:
    citajRed = citajRed.rstrip()
    if citajRed[0] != ' ':
        stanje = citajRed
        NovoStanje[stanje] = {}
    else:
        citajRed = citajRed.strip()
        if citajRed[0:5] == 'Stavi':
            NovoStanje[stanje][znak] = citajRed
        else:
            znak = citajRed
            NovoStanje[stanje][znak] = ''

trenutnoStanje = '0'
stogParsera = []
stogParsera.append('?')
stogParsera.append(trenutnoStanje)
listaRedova = []
for red in sys.stdin:
    red = red.rstrip()
    listaRedova.append(red)
#print listaRedova

i = 0
trenutniZnakovi = []
while i < len(listaRedova):
    red = listaRedova[i]
    ubaciUStanje = red
    red = izbaciRazmake(red)
    znak = red[0]
    #print trenutnoStanje
    obavi()

#print stogParsera

znak = '#'
vraceno = 0
while vraceno == 0:
    vraceno = obavi()

#print '------------------'    
#print stogParsera

korijenStabla = stogParsera.pop(len(stogParsera)-2)

praznina = 0
ispisStabla(korijenStabla, praznina)

