__author__ = 'bobo'
import sys
import fileinput


class Jedinka:
	def __init__(self,UnifZnak, Value,IsConst, Parent="",Function=""):
		self.UnifZnak = UnifZnak
		self.Parent = Parent
		self.Value = Value
		self.IsConst = IsConst #boolean, pliz
		#klasa zadana u roditelju
	def checkRangeInt(self):
		if self.Value > 2147483647:
			end()
		elif self.Value < -2147483648:
			end()
		
	def checkRangeChar(self):
		if self.Value < 0 or self.Value > 255: end()		
	def parsePridruzivanje(self, Source):
		self.Value = Source.Value
		self.IsConst = Source.IsConst
			
	#za array ne treba provjeravati je li num tip, jer je to osigurano u
	#syntax analizi
class Funkcija:
	def __init__(self, Name, ReturnType, ArgsType):
		self.Name = Name
		self.ReturnType= ReturnType
		self.ArgsType = []
		for x in ArgsType:
			self.ArgsType.append(x)

class Cvor:
	def __init__(self, Klasa, Kids):
		self.Klasa = Klasa
		self.Kids = []
		for clan in Kids:
			self.Kids.append(clan)

def convertConst(Jedinka):
	return Jedinka.IsConst != True			

def end():
	sys.exit(0)

a = Jedinka("BROJ",3,True)
b = Jedinka("Broj",4,False)
print  a.Value + "kk" + a.IsConst
print (str) b.Value + "kk" + a.IsConst
b.parsePridruzivanje(a)
print (str) a.Value + "kk" + a.IsConst
print (str) b.Value + "kk" + a.IsConst
	

			

	
		
