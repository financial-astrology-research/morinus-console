import os
import mtexts

class Common:
	def __init__(self):

		self.ephepath = os.path.join('SWEP', 'Ephem')

		self.symbols = os.path.join('Res', 'Morinus.ttf')
		self.abc = os.path.join('Res', 'FreeSans.ttf')

		self.Aspects = ('M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y')
		self.Signs1 = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')
		self.Signs2 = ('m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x')
		self.Uranus = ('H', '6')
		self.Pluto = ('J', '7', '8', '9')
		self.Housenames = ('I', '2', '3', 'IV', '5', '6', 'VII', '8', '9', 'X', '11', '12')
		self.Housenames2 = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
		self.months = (mtexts.txts['January'], mtexts.txts['February'], mtexts.txts['March'], mtexts.txts['April'], mtexts.txts['May'], mtexts.txts['June'], mtexts.txts['July'], mtexts.txts['August'], mtexts.txts['September'], mtexts.txts['October'], mtexts.txts['November'], mtexts.txts['December'])

		self.monthabbr = (mtexts.txts['Jan2'], mtexts.txts['Feb2'], mtexts.txts['Mar2'], mtexts.txts['Apr2'], mtexts.txts['May2'], mtexts.txts['Jun2'], mtexts.txts['Jul2'], mtexts.txts['Aug2'], mtexts.txts['Sep2'], mtexts.txts['Oct2'], mtexts.txts['Nov2'], mtexts.txts['Dec2'])
		self.days = (mtexts.txts['Monday'], mtexts.txts['Tuesday'], mtexts.txts['Wednesday'], mtexts.txts['Thursday'], mtexts.txts['Friday'], mtexts.txts['Saturday'], mtexts.txts['Sunday'])

		self.fortune = '4'

		self.retr = 'Z'


	def update(self, options):

		uranus = self.Uranus[0]
		if not options.uranus:
			uranus = self.Uranus[1]
		pluto = self.Pluto[options.pluto]

		self.Planets = ('A', 'B', 'C', 'D', 'E', 'F', 'G', uranus, 'I', pluto, 'K', 'L')



