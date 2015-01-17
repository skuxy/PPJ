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

lista_fija = []
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
	zbrajanje = False
	u_tijelu_fije = False
	pridruzivanje = False
	returnanje = False
	globalna = False
	negativan = False
	je_operacija = False
	oduzimanje = False
	binarno_ili = False
	binarno_i = False
	binarno_xor = False
	
	
	sadrzaj_registara= {}
	counter_registara=0
	
	broj_argumenata = 0
	
	
	for clan in lista:
		print str(negativan)
		trenutni=0
		name = clan.naziv.split(" ")
		print name[2]
		if name[0] == "KR_INT":
			if clan.prethodni.prethodni.prethodni.naziv=="<definicija_funkcije>":
				je_funkcija = True
				continue
			elif clan.prethodni.prethodni.prethodni.naziv == "<deklaracija>":
				#print "gloob"
				je_deklaracija_var = True
				if not u_tijelu_fije:
					globalna = True
			elif navodenje_argumenata:
				continue
		
		elif name[0] == "BROJ":
			if negativan:
				name[2]=int(name[2])*-1
			if returnanje:
				if not negativan:
					stog_arg.append(int(name[2]))
				else:
					stog_arg.append(int(name[2])*-1)		
			if globalna:
				lista_glob_konstanti.append(int(name[2]))	
				
		
			
										
		
		elif name[0] == "IDN":
			if name[2] in lista_fija:
				je_funkcija = True
			if je_funkcija and not u_tijelu_fije:
				dodaj_labelu_fije(name[2])
				lista_fija.append(name[2])
				zadnja_fija = name[2]
			elif je_funkcija and u_tijelu_fije:
				stream.write("\tCALL F_"+str(name[2].upper())+"\n")
				
			elif navodenje_argumenata:
				broj_argumenata += 1 #Hm? Hm!
			elif je_deklaracija_var:
				if globalna:
					lista_globalnih_var.append(name[2])	
			elif returnanje and not je_operacija and clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv != "<aditivni_izraz>":
				returnanje=False
				if name[2] in lista_globalnih_var:
					return_value("(G_"+name[2].upper()+")")
			elif clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv == "<aditivni_izraz>" and not zbrajanje and not je_operacija:
				#stog_arg.append(int(name[2]))
				
				zbrajanje = True
				if name[2] in lista_globalnih_var:
					stream.write("\tLOAD  R"+str(trenutni)+", (G_"+str(name[2].upper())+")\n") #loudaj u registar counter+1 i spremi u polje!
					trenutni+=1
					je_operacija = True
			elif zbrajanje and je_operacija:
				if name[2] in lista_globalnih_var:
					stream.write("\tLOAD  R"+str(trenutni+1)+", (G_"+str(name[2].upper())+")\n")	
					stream.write("\tADD R"+str(trenutni)+", R"+str(trenutni+1)+", R"+str(trenutni)+"\n")
			elif clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv == "<aditivni_izraz>" and not oduzimanje and not je_operacija:
				oduzimanje = True
				#print "jedan"
				if name[2] in lista_globalnih_var:
					stream.write("\tLOAD  R"+str(trenutni)+", (G_"+str(name[2].upper())+")\n") #loudaj u registar counter+1 i spremi u polje!
					trenutni+=1
				je_operacija = True
			elif oduzimanje and je_operacija:
				#print "w"
				if name[2] in lista_globalnih_var:
					stream.write("\tLOAD  R"+str(trenutni+1)+", (G_"+str(name[2].upper())+")\n")	
					stream.write("\tSUB R"+str(trenutni)+", R"+str(trenutni+1)+", R"+str(trenutni)+"\n")	
			elif clan.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.prethodni.naziv == "<odnosni_izraz>":
				if not je_operacija:
					if name[2] in lista_globalnih_var:
						stream.write("\tLOAD  R"+str(trenutni)+", (G_"+str(name[2].upper())+")\n") 
						trenutni+=1			
					je_operacija=True
				else:
					if binarno_ili:
						if name[2] in lista_globalnih_var:
							stream.write("\tLOAD  R"+str(trenutni+1)+", (G_"+str(name[2].upper())+")\n")	
							stream.write("\tOR R"+str(trenutni)+", R"+str(trenutni+1)+", R"+str(trenutni)+"\n")	
					elif binarno_i:
						if name[2] in lista_globalnih_var:
							stream.write("\tLOAD  R"+str(trenutni+1)+", (G_"+str(name[2].upper())+")\n")	
							stream.write("\tAND R"+str(trenutni)+", R"+str(trenutni+1)+", R"+str(trenutni)+"\n")
					elif binarno_xor:
						if name[2] in lista_globalnih_var:
							stream.write("\tLOAD  R"+str(trenutni+1)+", (G_"+str(name[2].upper())+")\n")	
							stream.write("\tXOR R"+str(trenutni)+", R"+str(trenutni+1)+", R"+str(trenutni)+"\n")					
		
		
		elif name[0] == "OP_PRIDRUZI":
			if je_deklaracija_var:
				continue #hm?			#recimo da je rijeseno, should be
		
		
		elif name[0] == "KR_VOID":
			if navodenje_argumenata:
				continue		
					
		elif name[0] == "TOCKAZAREZ":
			je_funkcija = False
			je_deklaracija_var = False
			binarno_ili=False	
			binarno_i=False
			globalna = False #Hm? jesam li zaribao? ------nisam!
		
				
			if returnanje and not je_operacija and stog_arg:
				reza = stog_arg.pop()
				if negativan:
					reza *= -1
				
				if SemantickiAnalizator.okINT(reza):
					return_value(str(reza), True)
				else:
					print "OKE NE"
			
			if je_operacija and returnanje:
				stream.write("\tMOVE R"+str(trenutni)+", R6\n")
				stream.write("\tRET\n")
			if returnanje and not je_operacija:
				stream.write("\tRET\n")	
			je_operacija = False	
			returnanje = False
		
		elif name[0] == "PLUS":
			zbrajanje = True	
			
		elif name[0] == "MINUS":
			oduzimanje = True
			if clan.prethodni.naziv=="<unarni_operator>":
				if negativan:
					negativan = False
				elif negativan == False:
					negativan = True					
			
		elif name[0] == "OP_BIN_ILI":
			binarno_ili=True
			je_operacija=True	
		
		elif name[0] == "OP_BIN_I":
			binarno_i=True
			je_operacija=True	
			
		elif name[0] == "OP_BIN_XILI":
			binarno_xor = True
			je_operacija = True		
		
		elif name[0] == "KR_RETURN":
			returnanje = True		
				
				
		elif name[0] == "L_ZAGRADA":
			pass #za sada
			"""if mozda_je_fija and u_tijelu_fije:
				stream.write("\tCALL F_"+str(zadnja_fija).upper()+"\n")
				je_funkcija = False
				navodenje_argumenata = True"""
		elif name[0] == "D_ZAGRADA":
			if navodenje_argumenata:
				if broj_argumenata == 0:
					continue
				navodenje_argumenata = False
		
		#ako je izvan, globalka je, vjerojatno se treba spremiti na kraj		
		elif name[0] == "L_VIT_ZAGRADA":
			u_tijelu_fije = True 

		elif name[0] == "D_VIT_ZAGRADA":
			u_tijelu_fije = False					
 
jednaki_ispis() #isto za sve, init stoga, poziv F_MAIN, HALTer
citaj_listove(SemantickiAnalizator.lista_listova)
stream.write("\n")

#print lista_glob_konstanti
#print lista_globalnih_var

for i in range(len(lista_glob_konstanti)):
	stream.write("\nG_"+lista_globalnih_var[i].upper()+"\tDW %D "+str(lista_glob_konstanti[i]))
	
#print lista_glob_konstanti
#print lista_globalnih_var

