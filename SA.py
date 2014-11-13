__author__ = "Brona"
import sys
import re


#prvo cu srediti upis Akcija i NovoStanje
Akcije = {}

for Linija in sys.stdin:
	#ako je izlistao sve Akcije
	if "--------------" in Linija: break
	Linija = Linija.strip().split(',')
	Linija[0] = re.sub(r'[^\w]',"",Linija[0]) #rijesavam zagrade
	#print Linija
	NesortAkcije = Linija[1].strip().split(':')
	NesortAkcije[0] = re.sub(r'\{|\'',"",NesortAkcije[0])#again
	#NesortAkcije[0] = re.sub(r'\'','',NesortAkcije[0])
	NesortAkcije[1] = re.sub(r'\'|\}\)',"",NesortAkcije[1])
	#NesortAkcije[1] = re.sub(r'\}\)','',NesortAkcije[1])
	Akcije[Linija[0]] = ([NesortAkcije[0]],[NesortAkcije[1].strip()])

for ajtem in Akcije.iteritems():
	print ajtem
NovoStanje	= {}
for Linija in sys.stdin:
	#isto kao i gore
	Linija = Linija.strip().split(',')
	Linija[0] = re.sub(r'[^\w]',"",Linija[0])
	for index in range(len(Linija)): 
		Linija[index] = re.sub(r'\{|\}\)',"",Linija[index])
		
	NovoStanje[Linija[0]] = []
	for index in range(1,len(Linija)):
		NovoStanje[Linija[0]].append(Linija[index])
	
for ajtem in NovoStanje.itervalues():
	for x in ajtem:
		print x
	
