import SemantickiAnalizator

SemantickiAnalizator.execute()

#SemantickiAnalizator.izvuci_djecu(SemantickiAnalizator.korijen)
#for x in SemantickiAnalizator.lista_listova:
#	print x.naziv
#	print x.prethodni.prethodni.prethodni.naziv

stream = open("a.frisc","w")

lista_globalnih_var = []
lista_glob_konstanti = []
#index_glob = 0
lista_registara = [] #max 6, sedmi je stack pointer
stog_arg = []


registri = []
trenutni = 0

argumenti = []
def jednaki_ispis():	
	#ovo je u svakom kodu jednako
	stream.write("\tMOVE 40000, R7\n\tCALL F_MAIN\n\tHALT")


def return_value(val, broj=False):
	if broj:
		stream.write("\tMOVE %D "+str(val)+", R6\n")
		stream.write("\tRET\n")
	else:
		stream.write("\tLOAD R6, "+str(val)+"\n")
		stream.write("\tRET\n")	
	
def dodaj_labelu_fije(labela):
	stream.write("\n\nF_"+str(labela).upper())	

def citaj_listove(lista):
	
	#milijarde flagova
	je_funkcija = False
	navodenje_argumenata = False
	je_deklaracija_var = False
	je_operacija = False
	u_tijelu_fije = False
	pridruzivanje = False
	returnanje = False
	globalna = False
	negativan = False
	
	sadrzaj_registara= {}
	counter_registara=0
	
	broj_argumenata = 0
	
	
	for clan in lista:
		name = clan.naziv.split(" ")
		if name[0] == "KR_INT":
			if clan.prethodni.prethodni.prethodni.naziv=="<definicija_funkcije>":
				je_funkcija = True
				continue
			elif clan.prethodni.prethodni.prethodni.naziv == "<deklaracija>":
				je_deklaracija_var = True
				if not u_tijelu_fije:
					globalna = True
			elif navodenje_argumenata:
				continue
		elif name[0] == "BROJ":
			if returnanje:
				stog_arg.append(int(name[2]))	
			if je_deklaracija_var:
				lista_glob_konstanti.append(int(name[2]))	
		
		elif name[0] == "MINUS":
			#print "je"
			if clan.prethodni.naziv=="<unarni_operator>":
				print "aha"
				if negativan:
					negativan = False
				elif negativan == False:
					#print "je"
					negativan = True	
											
		elif name[0] == "IDN":
			if je_funkcija:
				dodaj_labelu_fije(name[2])
			elif navodenje_argumenata:
				broj_argumenata += 1 #Hm? Hm!
			elif je_deklaracija_var:
				if globalna:
					lista_globalnih_var.append(name[2])	
			elif returnanje and clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv != "<aditivni_izraz>":
				returnanje=False
				if name[2] in lista_globalnih_var:
					return_value("(G_"+name[2].upper()+")")
			elif clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv == "<aditivni_izraz>":
				stog_arg.append(int(name[2]))
			#	stream.write("\tLOAD	" #loudaj u registar counter+1 i spremi u polje!
		
		elif name[0] == "OP_PRIDRUZI":
			if je_deklaracija_var:
				continue #hm?			#recimo da je rijeseno, should be
		
		
		elif name[0] == "KR_VOID":
			if navodenje_argumenata:
				continue		
					
		elif name[0] == "TOCKAZAREZ":
			je_funkcija = False
			je_deklaracija_var = False
			je_operacija = False
			globalna = False #Hm? jesam li zaribao?
			if returnanje:
				reza = stog_arg.pop()
				if negativan:
					reza *= -1
				
				if SemantickiAnalizator.okINT(reza):
					return_value(str(reza), True)
				else:
					print "OKE NE"
		
		elif name[0] == "PLUS":
			pass				
				
		
		elif name[0] == "KR_RETURN":
			returnanje = True		
				
				
		elif name[0] == "L_ZAGRADA":
			if je_funkcija:
				je_funkcija = False
				navodenje_argumenata = True
		elif name[0] == "D_ZAGRADA":
			if navodenje_argumenata:
				navodenje_argumenata = False
		
		#ako je izvan, globalka je, vjerojatno se treba spremiti na kraj		
		elif name[0] == "L_VIT_ZAGRADA":
			u_tijelu_fije = True 

		elif name[0] == "D_VIT_ZAGRADA":
			u_tijelu_fije = False					
 
jednaki_ispis() #isto za sve, init stoga, poziv F_MAIN, HALTer
citaj_listove(SemantickiAnalizator.lista_listova)
stream.write("\n\n")

#print lista_glob_konstanti
#print lista_globalnih_var

for i in range(len(lista_glob_konstanti)):
	stream.write("\nG_"+lista_globalnih_var[i].upper()+"\tDW %D "+str(lista_glob_konstanti[i]))
