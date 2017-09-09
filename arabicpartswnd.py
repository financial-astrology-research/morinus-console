import os
import wx
import astrology
import planets
import chart
import arabicparts
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class ArabicPartsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		lengthparts = 0
		if chrt.parts.parts != None:
			lengthparts = len(chrt.parts.parts)
		self.LINE_NUM = 1+lengthparts
		self.COLUMN_NUM = 4

		self.CELL_WIDTH = 12*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = (self.COLUMN_NUM*(self.CELL_WIDTH))
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Ara']


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

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		#Title
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txts = (mtexts.txts['Name'], mtexts.txts['Formula'], mtexts.txts['Longitude'], mtexts.txts['Almuten'])
		for i in range(len(txts)):
			w,h = draw.textsize(txts[i], self.fntText)
			draw.text((BOR+(self.CELL_WIDTH)*i+(self.CELL_WIDTH-w)/2, BOR+(self.TITLE_HEIGHT-h)/2), txts[i], fill=txtclr, font=self.fntText)

		#Parts
		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		self.drawlinelof(draw, x, y, mtexts.txts['LotOfFortune'], self.chart.fortune.fortune, tableclr)

		if self.chart.parts.parts != None:
			num = len(self.chart.parts.parts)
			x = BOR
			for i in range(num):
				y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_HEIGHT)*(i+1)
				self.drawline(draw, x, y, self.chart.parts.parts, tableclr, i)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawlinelof(self, draw, x, y, name, data, clr):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == 1:
				w,h = draw.textsize(name, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), name, fill=txtclr, font=self.fntText)
			elif i == 2:
				formula = u''
				if self.options.lotoffortune == chart.Chart.LFMOONSUN:
					formula = mtexts.txts['AC']+u' + '+mtexts.txts['MO']+u' - '+mtexts.txts['SU']
				elif self.options.lotoffortune == chart.Chart.LFDMOONSUN:
					A = mtexts.txts['AC']
					B = mtexts.txts['MO']
					C = mtexts.txts['SU']

					if not self.chart.planets.planets[astrology.SE_SUN].abovehorizon:
						tmp = C
						C = B
						B = tmp
					formula = A+u' + '+B+u' - '+C
				else:
					A = mtexts.txts['AC']
					B = mtexts.txts['SU']
					C = mtexts.txts['MO']

					if not self.chart.planets.planets[astrology.SE_SUN].abovehorizon:
						tmp = C
						C = B
						B = tmp
					formula = A+u' + '+B+u' - '+C

				w,h = draw.textsize(formula, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), formula, fill=txtclr, font=self.fntText)
			elif i == 3:
				lon = data[i-3]
				if self.options.ayanamsha != 0:
					lon = lon-self.chart.ayanamsha
					lon = util.normalize(lon)
				d,m,s = util.decToDeg(lon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				txtsign = self.signs[sign]
				wsg,hsg = draw.textsize(txtsign, self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)/2), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == 4:
				self.drawDegWinner(draw, x+summa, y, 3, True, self.chart.almutens.essentials.degwinner, txtclr)

			summa += offs[i]


	def drawline(self, draw, x, y, data, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == arabicparts.ArabicParts.NAME:
				name = data[idx][i]
				w,h = draw.textsize(name, self.fntText)
				draw.text((x+summa+(offs[i+1]-w)/2, y+(self.LINE_HEIGHT-h)/2), data[idx][i], fill=txtclr, font=self.fntText)
			elif i == arabicparts.ArabicParts.FORMULA:
				A = mtexts.partstxts[data[idx][1][0]]
				B = mtexts.partstxts[data[idx][1][1]]
				C = mtexts.partstxts[data[idx][1][2]]

				if data[idx][arabicparts.ArabicParts.DIURNAL] and not self.chart.planets.planets[astrology.SE_SUN].abovehorizon:
					tmp = C
					C = B
					B = tmp

				formula = A+u' + '+B+u' - '+C

				w,h = draw.textsize(formula, self.fntText)
				draw.text((x+summa+self.CELL_WIDTH+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), formula, fill=txtclr, font=self.fntText)
			elif i == arabicparts.ArabicParts.LONG:
				lon = data[idx][i]
				if self.options.ayanamsha != 0:
					lon = lon-self.chart.ayanamsha
					lon = util.normalize(lon)
				d,m,s = util.decToDeg(lon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				txtsign = self.signs[sign]
				wsg,hsg = draw.textsize(txtsign, self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)/2), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == arabicparts.ArabicParts.DEGWINNER:
				self.drawDegWinner2(draw, x+summa, y, data[idx][i], txtclr)

			summa += offs[i]


	def drawDegWinner(self, draw, x, y, i, onlyone, degwinner, txtclr):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
		subnum = len(degwinner[0])
		mwidth = 0
		for j in range(subnum):
			pid = degwinner[i][j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
				sco = degwinner[i][0][1]
				txt = '('+str(sco)+')'
				w,h = draw.textsize(txt, self.fntText)
				wsp,hsp = draw.textsize(' ', self.fntText)
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				pltxt = common.common.Planets[aux[j][0]]
				wpl,hpl = draw.textsize(pltxt, self.fntMorinus)
				txt = '('+str(aux[j][1])+')'
				wsp,hsp = draw.textsize(' ', self.fntText)
				w,h = draw.textsize(txt, self.fntText)
				prev = 0
				for p in range(j):
					prev += aux[j][2]+wsp

				offs = i
				if onlyone:
					offs = 0
				draw.text((x+(self.CELL_WIDTH-(mwidth))/2+prev, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)


	def drawDegWinner2(self, draw, x, y, degwinner, txtclr):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
		subnum = len(degwinner)
		mwidth = 0
		for j in range(subnum):
			pid = degwinner[j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
				sco = degwinner[0][1]
				txt = '('+str(sco)+')'
				w,h = draw.textsize(txt, self.fntText)
				wsp,hsp = draw.textsize(' ', self.fntText)
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				pltxt = common.common.Planets[aux[j][0]]
				wpl,hpl = draw.textsize(pltxt, self.fntMorinus)
				txt = '('+str(aux[j][1])+')'
				wsp,hsp = draw.textsize(' ', self.fntText)
				w,h = draw.textsize(txt, self.fntText)
				prev = 0
				for p in range(j):
					prev += aux[j][2]+wsp

				draw.text((x+(self.CELL_WIDTH-(mwidth))/2+prev, y+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)








