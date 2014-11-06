#!/usr/bin/env python

import fileinput
import time


#popunjavam sve potrebne tablice potrebne za rad analizatora

#lista svih stanja automata
SvaStanja = []
#pocetno stanje u obliku liste, mozda moze biti prosireno eprijelazom
PocetnoStanje = []
#lista svih prihvatljivih stanja
PrihvatljivaStanja = []
#popis svih prijelaza, u obliku dictionarya
TablicaPrijelaza = {}
#popis svih akcija, ovisno o zavrsnom stanju, u obliku dicta
Akcije = {}

def PopuniEOkolinu(trazeno_stanje):
	#ideja je da se petlja vrti dok god ima promjena u iteraciji
	TrazenaEOkolina = []
	Promjena = False
	if (trazeno_stanje,'$') in TablicaPrijelaza:
		for x in TablicaPrijelaza[(trazeno_stanje,'$')]:
			TrazenaEOkolina.append(x)
			Promjena = True
	while(Promjena == True):
		Promjena = False
		for state in TrazenaEOkolina:
			if (state,'$') in TablicaPrijelaza:
				for x in TablicaPrijelaza[(state,'$')]:
					if x not in TrazenaEOkolina:
						TrazenaEOkolina.append(x)
						Promjena = True
	return TrazenaEOkolina

def makniDuplikate(lista):
    seen = set()
    seen_add = seen.add
    return [ x for x in lista if not (x in seen or seen_add(x))]
#ulaz s automata generiranog GLA-om
AutomatStream = fileinput.input("automat.txt")

SvaStanja = AutomatStream.readline().strip().split(',')
#cistim zadnje polje liste, prazan string ostao iz Generatora
SvaStanja.pop()

PocetnoStanje = AutomatStream.readline().strip()

PrihvatljivaStanja = AutomatStream.readline().strip().split(',')

Prijelaz = "" #linija automata gdje je opisan prijelaz
while(1):
	Prijelaz = AutomatStream.readline().strip()
	if Prijelaz == '%': break #kraj navodjenja prijelaza
	Prijelaz = Prijelaz.split("->")
	Lijeva = Prijelaz[0]
	Desna = Prijelaz[1]
	Lijeva = Lijeva.split(',')
	if (Lijeva[0],Lijeva[1]) not in TablicaPrijelaza.keys():
		TablicaPrijelaza[(Lijeva[0],Lijeva[1])] = []
	TablicaPrijelaza[(Lijeva[0],Lijeva[1])].append(Desna)

#popunjavam akcije zavrsnih stanja
while(1):
	State = AutomatStream.readline().strip() #zavrsno stanje
	if(State in PrihvatljivaStanja):
		Akcije.keys().append(State)
		OtvorenaViticasta = AutomatStream.readline().strip()
		Akcije[State] = []
		while(1):
			x = AutomatStream.readline().strip()
			if x == '}': break #kraj akcije
			Akcije[State].append(x)
	if State == "": break 

#zavrsio upis u tablice, provjerio sam i radi ispravno
#oznaka trenutne linije, pocinje s 1
linija = 1

#index trenutnog chara
indexTrenutnog = 0

#index kraja zadnje jedinke
zadnjiZavrsni = 0


#index zavrsnog znaka s najvecim prefiksom
indexNajdaljeg = 0

#zavrsno stanje s najvecim prefiksom
najveceProcitano = ""



AutomatStream.close()
PrimjerJezika = open("PPJ_Testni_primjeri_2011-12/02_nadji_x_retci/test.in")

#ucitavam cijeli primjer u jedan string
Tekst = ""
while(1):
	x=PrimjerJezika.read(1)
	if x == "": break
	Tekst += x
#ucitao sam cijeli primjer u jedan string	

#popis mogucih stanja
TrenutnoStanje = []
TrenutnoStanje.append(PocetnoStanje)


while(1):
	#samo inicijaliziram polje za eokolinu
	EOkolina = []
	Char = Tekst[indexTrenutnog]
	if len(TrenutnoStanje) != 1:	
		for stanje in TrenutnoStanje:
			EOkolina = PopuniEOkolinu(stanje)
			EOkolina = makniDuplikate(EOkolina)
			
		EOkolina += TrenutnoStanje
	else:
		EOkolina = PopuniEOkolinu(TrenutnoStanje[0])		
		EOkolina += TrenutnoStanje
	#stanja u koje je moguce uci iz eOkoline za dan input		
	NovaStanja = []
	print EOkolina
	
	obnovioSe = False #ako se tokom iteracije svih nije naslo stanje
					  #gdje se moze preci
	for stanje in EOkolina:
		if (stanje,Char) in TablicaPrijelaza:
			#ako moze prijeci u vise stanja (jer je eNKA)
			for x in TablicaPrijelaza[(stanje,Char)]:
				NovaStanja.append(x)
				NovaStanja = makniDuplikate(NovaStanja) #just in case
			obnovioSe = True
	if obnovioSe == True:		
		for x in NovaStanja:
			#punim eokolinom i za nova stanja
			NovaStanja+=PopuniEOkolinu(x)
			NovaStanja = makniDuplikate(NovaStanja)
		for stanje in NovaStanja:
			if x in PrihvatljivaStanja and indexTrenutnog>=indexNajdaljeg:
				#print x
				najveceProcitano = x
				indexNajdaljeg=indexTrenutnog
				
	if obnovioSe==False:
		if "-" != Akcije[najveceProcitano][0]:
			print Akcije[najveceProcitano][0]
			print linija
			print Tekst[zadnjiZavrsni:indexNajdaljeg+1]
			print "_________________________________________"
			time.sleep(3)
			zadnjiZavrsni = indexNajdaljeg
			TrenutnoStanje = []
			TrenutnoStanje.append(PocetnoStanje)
			indexTrenutnog = indexNajdaljeg
		elif "-" == Akcije[najveceProcitano][0]:
			print "yua"
			linija+=1
			zadnjiZavrsni = indexNajdaljeg
			indexTrenutnog = indexNajdaljeg
		
	else: #ako se apdejtala lista sa novim stanjima
		TrenutnoStanje = NovaStanja

		
	#ako je nova lajna
	indexTrenutnog+=1
	
	
	
			
	
	
	
	






