from datetime import datetime, timedelta
# ##################################
# Elias V 7.3.0
import astrology
# ##################################
import wx
import planets
import common
import commonwnd
import Image, ImageDraw, ImageFont
import mtexts

# ##################################
# Roberto V 7.3.0
# *** SOME *** texts txtsxxx -> txts
# ##################################

class FirdariaWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, opts, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, opts, id, size)

		self.parent = parent
		self.fird = chrt.firdaria
		self.options = opts		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 1
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 12*self.FONT_SIZE
		self.BIG_CELL_WIDTH = 20*self.FONT_SIZE

		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = (self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH)
		self.SPACE_TITLEY = 0

		self.EXTRA_PERIODS = 3 #Three more planetary periods after year 75
# ##################################
# Roberto V 7.3.0		
		self.LINE_NUM = (planets.Planets.PLANETS_NUM + self.EXTRA_PERIODS)*6 #(planets.Planets.PLANETS_NUM+1)+2 #+2 is the number of the Nodes of the Moon
# ##################################
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+self.LINE_NUM*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
# ##################################
# Elias V 8.0.0		
		self.clrs = [self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil]
# ##################################
		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)

		self.drawBkg()


	def getExt(self):
# ##################################
# Roberto V 7.3.0		
		#return mtexts.txtsabbrevs['Fir']
		return mtexts.txts['Firdaria']
# ##################################

	def drawBkg(self):
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

		#Title
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt = mtexts.txts['Firdaria']
		if self.fird.isdaily:
			txt += ' ('+mtexts.txts['Diurnal']+')'
		else:
			if self.options.isfirbonatti:
				txt += ' ('+mtexts.txts['Nocturnal']+': '+mtexts.txts['Bonatus']+')'
			else:
				txt += ' ('+mtexts.txts['Nocturnal']+': '+mtexts.txts['AlBiruni']+')'
	
		w,h = draw.textsize(txt, self.fntText)
		draw.text((BOR+(self.BIG_CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

# ##################################
# Roberto V 7.3.0 
# Elias V 7.3.0 replace planets (8,9) for nodes (10,11)
		#plstxts = (common.common.planets[0], common.common.planets[1], common.common.planets[2], common.common.planets[3], common.common.planets[4], common.common.planets[5], common.common.planets[6], common.common.planets[7], common.common.planets[8])
		plstxts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[10], common.common.Planets[11])
# ##################################

		if self.fird.isdaily:
			planetaryyears = self.fird.dailyplanetaryyears
		else:
			if self.options.isfirbonatti:
				planetaryyears = self.fird.nightlyplanetaryyearsbonatti
			else:
				planetaryyears = self.fird.nightlyplanetaryyearsalbiruni

		ln = 0
		starting = self.fird.startdate
		for index in range(len(planetaryyears) + self.EXTRA_PERIODS):
			aindex = index % len(planetaryyears)
			planet, years = planetaryyears[aindex]
			ending = datetime(starting.year + years, starting.month, starting.day)
# ##################################
# Elias V 8.0.0
			# [Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, MeanNode, TrueNode]
			planetseliascorrection=[6,5,4,0,3,2,1,7,8]
			#txt = plstxts[planet]
			txt = plstxts[planetseliascorrection[planet]]
			w,h = draw.textsize(txt, self.fntMorinus)
			clr = (0,0,0)

			if not self.bw:
				objidx = planetseliascorrection[planet]
				if self.options.useplanetcolors:
					if planetseliascorrection[planet] > astrology.SE_SATURN:
						objidx = 10 #Set Node color
					clr = self.options.clrindividual[objidx]
				else:
					dign = self.chart.dignity(objidx)
					clr = self.clrs[dign]
# ##################################

			draw.rectangle(((BOR, BOR+(ln+1)*self.LINE_HEIGHT),(BOR+self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH, BOR+(ln+2)*self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			draw.line((BOR+self.SMALL_CELL_WIDTH, BOR+(ln+1)*self.LINE_HEIGHT, BOR+self.SMALL_CELL_WIDTH, BOR+(ln+2)*self.LINE_HEIGHT), fill=tableclr)
			draw.text((BOR+(self.SMALL_CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2+(ln+1)*self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
			ending2 = ending+timedelta(days=-1)
			txt = str(starting.year)+'.'+str(starting.month).zfill(2)+'.'+str(starting.day).zfill(2)+' - '+str(ending2.year)+'.'+str(ending2.month).zfill(2)+'.'+str(ending2.day).zfill(2)+' ('+str(years)+' '+'Years'+')'
			w,h = draw.textsize(txt, self.fntText)
			draw.text((BOR+self.SMALL_CELL_WIDTH+(self.BIG_CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2+(ln+1)*self.LINE_HEIGHT), txt, fill=txtclr, font=self.fntText)

			ln += 1
			ln = self.displaySubPeriods(draw, planetaryyears, aindex, starting, ending, plstxts, ln, BOR, txtclr, tableclr)
			starting = ending

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def displaySubPeriods(self, draw, planetaryyears, index, starting, ending, plstxts, ln, BOR, txtclr, tableclr):
		if self.fird.isNode(index):
			return ln

		subperiodstart = starting

# ##################################
# Elias V 7.3.0
# BUG SOLVED: total_seconds() is a function too new to ubuntu 10.04 systems. I created an alternative subfunction for no error code.
		try:
			secs = (ending - starting).total_seconds()
		except:
			secs = (ending - starting).seconds + (ending - starting).microseconds / 1E6 + (ending - starting).days * 86400		

# reestructure for sentence without new planets.

		#for i in range(planets.Planets.PLANETS_NUM):
		for i in range(7):
# ##################################
			planet, years = planetaryyears[index]
			subperiodends = subperiodstart + timedelta(seconds = secs / 7) #Is this equal to PLANETS_NUM?
# ##################################
# Elias V 8.0.0
			# [Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, MeanNode, TrueNode]
			planetseliascorrection=[6,5,4,0,3,2,1,7,8]
			#txt = plstxts[planet]
			txt = plstxts[planetseliascorrection[planet]]
			w,h = draw.textsize(txt, self.fntMorinus)
			clr = (0,0,0)

			if not self.bw:
				objidx = planetseliascorrection[planet]
				if self.options.useplanetcolors:
					if planetseliascorrection[planet] > astrology.SE_SATURN:
						objidx = 10 #Set Node color
					clr = self.options.clrindividual[objidx]
				else:
					dign = self.chart.dignity(objidx)
					clr = self.clrs[dign]

#				objidx = planet
#				if planet > 10:
#					objidx -= 1
#				#clr = self.options.clrPlanets[objidx]		
# ##################################
			draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR+(ln+i+1)*self.LINE_HEIGHT),(BOR+2*self.SMALL_CELL_WIDTH+self.CELL_WIDTH, BOR+(ln+i+2)*self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			draw.line((BOR+2*self.SMALL_CELL_WIDTH, BOR+(ln+i+1)*self.LINE_HEIGHT, BOR+2*self.SMALL_CELL_WIDTH, BOR+(ln+i+2)*self.LINE_HEIGHT), fill=tableclr)
			draw.text((BOR+self.SMALL_CELL_WIDTH+(self.SMALL_CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2+(ln+i+1)*self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
			txt = str(subperiodstart.year)+'.'+str(subperiodstart.month).zfill(2)+'.'+str(subperiodstart.day).zfill(2)
			w,h = draw.textsize(txt, self.fntText)
			draw.text((BOR+2*self.SMALL_CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2+(ln+i+1)*self.LINE_HEIGHT), txt, fill=txtclr, font=self.fntText)
			subperiodstart = subperiodends
			index = self.fird.nextIndex(index)

		return ln+i+1


