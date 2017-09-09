import math
import wx
import os
import astrology
import planets
import fixstars
import fortune
import houses
import chart
import common
import commonwnd
import Image, ImageDraw, ImageFont
import mtexts
import util


class FixStarsAspectsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(2*18*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/6
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = len(self.chart.fixstars.data)
		self.CELL_WIDTH = 6*self.FONT_SIZE
		self.SQUARE_SIZE = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.COLUMN_NUM = 23

		self.PLANETSOFFS = 4
		self.LOFOFFS = 16
		self.HOUSESOFFS = 17
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.COLUMN_NUM -= 1
				self.LOFOFFS -= 1
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.COLUMN_NUM -= 1
				self.LOFOFFS -= 1
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.COLUMN_NUM -= 1
				self.LOFOFFS -= 1
				self.HOUSESOFFS -= 1
			if not self.options.shownodes:
				self.COLUMN_NUM -= 2
				self.LOFOFFS -= 2
				self.HOUSESOFFS -= 2
			if not self.options.showlof:
				self.COLUMN_NUM -= 1
				self.HOUSESOFFS -= 1
			if not self.options.houses:
				self.COLUMN_NUM -= 6

		self.TITLE_HEIGHT = self.SQUARE_SIZE
		self.TITLE_WIDTH = (self.COLUMN_NUM*self.SQUARE_SIZE)
		self.SPACE_TITLEY = 0

		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*((self.LINE_HEIGHT)+(self.SPACE)))
		self.TABLE_WIDTH = (self.CELL_WIDTH+(self.COLUMN_NUM)*(self.SQUARE_SIZE+self.SPACE))
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, 4*self.FONT_SIZE/5)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntAspects = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/5)
		self.fntText = ImageFont.truetype(common.common.abc, 3*self.FONT_SIZE/5)
		self.fntTextOrb = ImageFont.truetype(common.common.abc, self.FONT_SIZE/2)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
		self.arsigndiff = (0, -1, -1, 2, -1, 3, 4, -1, -1, -1, 6)
		self.hidx = (1, 2, 3, 10, 11, 12)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['FSAsps']

# ###################################
# Elias v 8.0.0
# ###################################
	def getAsp(self, typ, lon1, lon2, orb):
		lona1 = lon1
		lona2 = lon2
		if self.options.ayanamsha != 0:
			lona1 -= self.chart.ayanamsha
			lona1 = util.normalize(lona1)
			lona2 -= self.chart.ayanamsha
			lona2 = util.normalize(lona2)
		if not lona1 > lona2:
			a= lona1
			lona1 = lona2
			lona2 = a
		diff = lona1 -typ
		if ((lona2-orb) < diff) and ((lona2+orb) > diff):
			return True
		else:
			return False

	def getOrb(self, typ, lon1, lon2, orb):
		lona1 = lon1
		lona2 = lon2
		if self.options.ayanamsha != 0:
			lona1 -= self.chart.ayanamsha
			lona1 = util.normalize(lona1)
			lona2 -= self.chart.ayanamsha
			lona2 = util.normalize(lona2)
		if not lona1 > lona2:
			a= lona1
			lona1 = lona2
			lona2 = a
		diff = lona1 -typ
		if ((lona2-orb) < diff) and ((lona2+orb) > diff):
			if lona2 < diff:
				return (diff-lona2)
			else:
				return (lona2-diff)
		else:
			return False
# ###################################

	def drawBkg(self):
# ###################################
# Elias v8.0.0 
# ###################################
		if self.options.traditionalaspects:
			runAspects = [0, 3, 5, 6, 10]
		else:
			runAspects = range(chart.Chart.CONJUNCTIO , (chart.Chart.OPPOSITIO+1))
# ###################################
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		#Squares of the asps
		yy = BOR+self.TITLE_HEIGHT+self.SPACE
		num = len(self.chart.fixstars.data)
		for i in range(num):
			xx = BOR+self.CELL_WIDTH+self.SPACE
			for j in range(self.COLUMN_NUM):
				self.drawSquare(draw, xx, yy, tableclr)
				xx += self.SQUARE_SIZE+self.SPACE
			yy += self.SQUARE_SIZE+self.SPACE

		#Names
		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE
		num = len(self.chart.fixstars.data)
		for i in range(num):
			self.drawRect(draw, x, y+i*(self.LINE_HEIGHT+self.SPACE), tableclr)
			name = self.chart.fixstars.data[i][fixstars.FixStars.NAME]
			if name == '':
				name = self.chart.fixstars.data[i][fixstars.FixStars.NOMNAME]
			w,h = draw.textsize(name, self.fntText)
			draw.text((x+(self.CELL_WIDTH-w)/2, y+i*(self.LINE_HEIGHT+self.SPACE)+(self.LINE_HEIGHT-h)/2), name, fill=txtclr, font=self.fntText)

		#AscMC
		x = BOR+self.CELL_WIDTH+self.SPACE
		y = BOR
		txts = ('0', '3', '1', '2')
		for i in range(len(txts)):
			self.drawSquare(draw, x, y, tableclr)
			w,h = draw.textsize(txts[i], self.fntSymbol)
			draw.text((x+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), txts[i], fill=txtclr, font=self.fntSymbol)
			x += self.SQUARE_SIZE+self.SPACE

		ASC = self.chart.houses.ascmc[houses.Houses.ASC]
		DESC = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC]+180.0)
		MC = self.chart.houses.ascmc[houses.Houses.MC]
		IC = util.normalize(self.chart.houses.ascmc[houses.Houses.MC]+180.0)
		ascmc = [ASC, DESC, MC, IC]
#		num = len(self.chart.fsaspmatrixangles)
#		for i in range(num):
#			lon1 = self.chart.fixstars.data[self.chart.fsaspmatrixangles[i][0]][fixstars.FixStars.LON]
#			num2 = len(self.chart.fsaspmatrixangles[i][1])
#			for j in range(num2):
#				lon2 = ascmc[self.chart.fsaspmatrixangles[i][1][j]]
#				showasp = self.isShowAsp(chart.Chart.CONJUNCTIO, lon1, lon2)
#				if showasp:
#					txt = common.common.Aspects[chart.Chart.CONJUNCTIO]
#					w,h = draw.textsize(txt, self.fntAspects)
#					clr = self.options.clraspect[chart.Chart.CONJUNCTIO]
#					if self.bw:
#						clr = (0,0,0)
#					xx = BOR+self.CELL_WIDTH+self.SPACE+self.chart.fsaspmatrixangles[i][1][j]*(self.SQUARE_SIZE+self.SPACE)
#					yy = BOR+self.TITLE_HEIGHT+self.SPACE+self.chart.fsaspmatrixangles[i][0]*(self.SQUARE_SIZE+self.SPACE)
#					draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
# ###################################
# Elias v8.0.0 ASC MC
# ###################################
		num= len(self.chart.fixstars.data)
		for i in range(num):
			lon1 = self.chart.fixstars.data[i][fixstars.FixStars.LON]
			orb= self.options.fixstars[self.chart.fixstars.data[i][fixstars.FixStars.NOMNAME]]
			for j in range(4):
				lon2 = ascmc[j]
				for numasp in runAspects:
					degree = chart.Chart.Aspects[numasp]
					AspType = self.getAsp(degree, lon1, lon2, orb)
			
					# Only show selected aspects in Options.
					if AspType and self.options.aspect[numasp]:
						txt = common.common.Aspects[numasp]
						w,h = draw.textsize(txt, self.fntAspects)
						clr = self.options.clraspect[numasp]
						if self.bw:
							clr = (0,0,0)
						# Print Aspect
						xx = BOR+self.CELL_WIDTH+self.SPACE-(self.SQUARE_SIZE/5)+j*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE-(self.SQUARE_SIZE/5)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
						
						# Print Orb
						OrbDegree = "%0.1f" % (self.getOrb(degree, lon1, lon2, orb))
						w,h = draw.textsize(OrbDegree, self.fntTextOrb)
						xx = BOR+self.CELL_WIDTH+self.SPACE+j*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE+((self.SQUARE_SIZE-h)/1.7)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), OrbDegree, fill=clr, font=self.fntTextOrb)
# ###################################
		

		#Planets
		j = 0
		num = len(common.common.Planets)
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes) or (i == astrology.SE_TRUE_NODE and not self.options.shownodes)):
				continue

			self.drawSquare(draw, x, y, tableclr)
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					objidx = i
					if i >= len(common.common.Planets)-1:
						objidx -= 1
					clr = self.options.clrindividual[objidx]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			w,h = draw.textsize(common.common.Planets[i], self.fntMorinus)
			draw.text((x+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), common.common.Planets[i], fill=clr, font=self.fntMorinus)
			x += (self.SQUARE_SIZE+self.SPACE)
			j += 1

		num = len(self.chart.fsaspmatrix)
		for i in range(num):
			lon1 = self.chart.fixstars.data[self.chart.fsaspmatrix[i][0]][fixstars.FixStars.LON]
			num2 = len(self.chart.fsaspmatrix[i][1])
			skipped = 0

# ###################################
# Elias v8.0.0 PLANETS
# ###################################
		num= len(self.chart.fixstars.data)
		orb = chart.Chart.def_fixstarsorb
		for i in range(num):
			lon1 = self.chart.fixstars.data[i][fixstars.FixStars.LON]
			orb= self.options.fixstars[self.chart.fixstars.data[i][fixstars.FixStars.NOMNAME]]
			for j in range(len(common.common.Planets)):
				lon2 = self.chart.planets.planets[j].data[planets.Planet.LONG]
				for numasp in runAspects:
					degree = chart.Chart.Aspects[numasp]
					AspType = self.getAsp(degree, lon1, lon2, orb)
					
					# Only show selected aspects in Options.
					if AspType and self.options.aspect[numasp]:
						txt = common.common.Aspects[numasp]
						w,h = draw.textsize(txt, self.fntAspects)
						clr = self.options.clraspect[numasp]
						if self.bw:
							clr = (0,0,0)
						# Print Aspect
						xx = BOR+self.CELL_WIDTH+self.SPACE-(self.SQUARE_SIZE/5)+self.PLANETSOFFS*(self.SQUARE_SIZE+self.SPACE)+(j-skipped)*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE-(self.SQUARE_SIZE/5)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
						
						# Print Orb
						OrbDegree = "%0.1f" % (self.getOrb(degree, lon1, lon2, orb))
						w,h = draw.textsize(OrbDegree, self.fntTextOrb)
						xx = BOR+self.CELL_WIDTH+self.SPACE+self.PLANETSOFFS*(self.SQUARE_SIZE+self.SPACE)+(j-skipped)*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE+((self.SQUARE_SIZE-h)/1.7)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), OrbDegree, fill=clr, font=self.fntTextOrb)	
# ###################################

		#LoF
		if not self.options.intables or (self.options.intables and self.options.showlof):
			self.drawSquare(draw, x, y, tableclr)
			w,h = draw.textsize(common.common.fortune, self.fntMorinus)
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[astrology.SE_MEAN_NODE+1]
				else:
					clr = self.options.clrperegrin

			draw.text((x+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), common.common.fortune, clr, font=self.fntMorinus)
			x += (self.SQUARE_SIZE+self.SPACE)

# ###################################
# Elias v8.0.0 LOF
# ###################################
			num= len(self.chart.fixstars.data)
			for i in range(num):
				lon1 = self.chart.fixstars.data[i][fixstars.FixStars.LON]
				orb= self.options.fixstars[self.chart.fixstars.data[i][fixstars.FixStars.NOMNAME]]
				lon2 = self.chart.fortune.fortune[fortune.Fortune.LON]
				for numasp in runAspects:
					degree = chart.Chart.Aspects[numasp]
					AspType = self.getAsp(degree, lon1, lon2, orb)
				
					# Only show selected aspects in Options.
					if AspType and self.options.aspect[numasp]:
						txt = common.common.Aspects[numasp]
						w,h = draw.textsize(txt, self.fntAspects)
						clr = self.options.clraspect[numasp]
						if self.bw:
							clr = (0,0,0)

						# Print Aspect
						xx = BOR+self.CELL_WIDTH+self.SPACE-(self.SQUARE_SIZE/5)+self.LOFOFFS*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE-(self.SQUARE_SIZE/5)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
						
						# Print Orb
						OrbDegree = "%0.1f" % (self.getOrb(degree, lon1, lon2, orb))
						w,h = draw.textsize(OrbDegree, self.fntTextOrb)
						xx = BOR+self.CELL_WIDTH+self.SPACE+self.LOFOFFS*(self.SQUARE_SIZE+self.SPACE)
						yy = BOR+self.TITLE_HEIGHT+self.SPACE+((self.SQUARE_SIZE-h)/1.7)+i*(self.SQUARE_SIZE+self.SPACE)
						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), OrbDegree, fill=clr, font=self.fntTextOrb)	
# ###################################

		#Houses
		if not self.options.intables or (self.options.intables and self.options.houses):
			for i in range(len(self.hidx)):
				self.drawSquare(draw, x+(self.SQUARE_SIZE+self.SPACE)*i, y, tableclr)
				w,h = draw.textsize(common.common.Housenames2[self.hidx[i]-1], self.fntText)
				draw.text((x+(self.SQUARE_SIZE+self.SPACE)*i+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), common.common.Housenames2[self.hidx[i]-1], fill=(0,0,0), font=self.fntText)
	
			aroffs = (0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5)
			isopp = (False, False, False, True, True, True, True, True, True, False, False, False)
#			num = len(self.chart.fsaspmatrixhcs)
#			for i in range(num):
#				lon1 = self.chart.fixstars.data[self.chart.fsaspmatrixhcs[i][0]][fixstars.FixStars.LON]
#				num2 = len(self.chart.fsaspmatrixhcs[i][1])
#				for j in range(num2):
#					k = self.chart.fsaspmatrixhcs[i][1][j]
#					lon2 = self.chart.houses.cusps[k+1]
#					print "K: "+str(k)
#					asp = chart.Chart.CONJUNCTIO
#					if isopp[k]:
#						asp = chart.Chart.OPPOSITIO
#					showasp = self.isShowAsp(asp, lon1, lon2)
#					if showasp:
#						txt = common.common.Aspects[asp]
#						w,h = draw.textsize(txt, self.fntAspects)
#						clr = self.options.clraspect[asp]
#						if self.bw:
#							clr = (0,0,0)
#						xx = BOR+self.CELL_WIDTH+self.SPACE+self.HOUSESOFFS*(self.SQUARE_SIZE+self.SPACE)+aroffs[k]*(self.SQUARE_SIZE+self.SPACE)
#						yy = BOR+self.TITLE_HEIGHT+self.SPACE+self.chart.fsaspmatrixhcs[i][0]*(self.SQUARE_SIZE+self.SPACE)
#						draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
# ###################################
# Elias v8.0.0 HOUSES
# ###################################
			num= len(self.chart.fixstars.data)
			cusps= [0, 1, 2, 9, 10, 11]
			for i in range(num):
				lon1 = self.chart.fixstars.data[i][fixstars.FixStars.LON]
				orb= self.options.fixstars[self.chart.fixstars.data[i][fixstars.FixStars.NOMNAME]]
				for j in cusps:
					lon2 = self.chart.houses.cusps[j+1]
					for numasp in runAspects:
						degree = chart.Chart.Aspects[numasp]
						AspType = self.getAsp(degree, lon1, lon2, orb)
				
						# Only show selected aspects in Options.
						if AspType and self.options.aspect[numasp]:
							txt = common.common.Aspects[numasp]
							w,h = draw.textsize(txt, self.fntAspects)
							clr = self.options.clraspect[numasp]
							if self.bw:
								clr = (0,0,0)

							# Print Aspect
							xx = BOR+self.CELL_WIDTH+self.SPACE-(self.SQUARE_SIZE/5)+self.HOUSESOFFS*(self.SQUARE_SIZE+self.SPACE)+aroffs[j]*(self.SQUARE_SIZE+self.SPACE)
							yy = BOR+self.TITLE_HEIGHT+self.SPACE-(self.SQUARE_SIZE/5)+i*(self.SQUARE_SIZE+self.SPACE)
							draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), txt, fill=clr, font=self.fntAspects)
						
							# Print Orb
							OrbDegree = "%0.1f" % (self.getOrb(degree, lon1, lon2, orb))
							w,h = draw.textsize(OrbDegree, self.fntTextOrb)
							xx = BOR+self.CELL_WIDTH+self.SPACE+self.HOUSESOFFS*(self.SQUARE_SIZE+self.SPACE)+aroffs[j]*(self.SQUARE_SIZE+self.SPACE)
							yy = BOR+self.TITLE_HEIGHT+self.SPACE+((self.SQUARE_SIZE-h)/1.7)+i*(self.SQUARE_SIZE+self.SPACE)
							draw.text((xx+(self.SQUARE_SIZE-w)/2, yy+(self.SQUARE_SIZE-h)/2), OrbDegree, fill=clr, font=self.fntTextOrb)	
# ###################################

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawSquare(self, draw, x, y, tableclr):
		draw.line((x, y, x+self.SQUARE_SIZE, y), fill=tableclr)
		draw.line((x, y, x, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x+self.SQUARE_SIZE, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y), fill=tableclr)


	def drawRect(self, draw, x, y, tableclr):
		draw.line((x, y, x+self.CELL_WIDTH, y), fill=tableclr)
		draw.line((x, y, x, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x, y+self.SQUARE_SIZE, x+self.CELL_WIDTH, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x+self.CELL_WIDTH, y+self.SQUARE_SIZE, x+self.CELL_WIDTH, y), fill=tableclr)


	def isShowAsp(self, typ, lon1, lon2, p = -1):
		res = False

		if typ != chart.Chart.NONE and (not self.options.intables or self.options.aspect[typ]):
			val = True
			#check traditional aspects
			if self.options.intables:
				if self.options.traditionalaspects:
					if not(typ == chart.Chart.CONJUNCTIO or typ == chart.Chart.SEXTIL or typ == chart.Chart.QUADRAT or typ == chart.Chart.TRIGON or typ == chart.Chart.OPPOSITIO):
						val = False
					else:
						lona1 = lon1
						lona2 = lon2
						if self.options.ayanamsha != 0:
							lona1 -= self.chart.ayanamsha
							lona1 = util.normalize(lona1)
							lona2 -= self.chart.ayanamsha
							lona2 = util.normalize(lona2)
						sign1 = int(lona1/chart.Chart.SIGN_DEG)
						sign2 = int(lona2/chart.Chart.SIGN_DEG)
						signdiff = math.fabs(sign1-sign2)
						#check pisces-aries transition
						if signdiff > chart.Chart.SIGN_NUM/2:
							signdiff = chart.Chart.SIGN_NUM-signdiff#!?
						if self.arsigndiff[typ] != signdiff:
							val = False

				if not self.options.aspectstonodes and p == astrology.SE_MEAN_NODE:
					val = False

			res = val

		return res



	def isExact(self, exact, lon1, lon2):
		res = False

		if self.options.intables and self.options.traditionalaspects:
			lona1 = lon1
			lona2 = lon2
			if self.options.ayanamsha != 0:
				lona1 -= self.chart.ayanamsha
				lona1 = util.normalize(lona1)
				lona2 -= self.chart.ayanamsha
				lona2 = util.normalize(lona2)
			deg1 = int(lona1%chart.Chart.SIGN_DEG)
			deg2 = int(lona2%chart.Chart.SIGN_DEG)
			if deg1 == deg2:
				res = True
		else:
			if exact:
				res = True

		return res



