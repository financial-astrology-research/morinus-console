import wx
import os
import astrology
import chart
#import houses
#import planets
import customerpd
import commonwnd
import primdirs
import common
import Image, ImageDraw, ImageFont
import util
import mtexts


class CustomerWnd(commonwnd.CommonWnd):
	def __init__(self, parent, chrt, options, mainfr, cpt, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.chart = chrt
		self.options = options		
		self.mainfr = mainfr
		self.cpt = cpt
		self.bw = self.options.bw

		self.speculum = 0
		if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN or self.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
			self.speculum = 1

		line_num = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if self.options.speculums[self.speculum][i] == True:
				line_num += 1

		BOR = CustomerWnd.BORDER

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 1
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.CELL_WIDTH = 8*self.FONT_SIZE

		self.LINE_NUM = line_num

		self.TABLE_HEIGHT = ((self.LINE_NUM)*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = ((self.COLUMN_NUM+1)*(self.CELL_WIDTH))
	
		self.WIDTH = (BOR+self.TABLE_WIDTH+BOR)
		self.HEIGHT = (BOR+self.TABLE_HEIGHT+BOR)

		self.SetBackgroundColour(self.options.clrbackground)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Cpt']


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

		BOR = CustomerWnd.BORDER

		x = BOR
		y = BOR

		if self.speculum == 0:
			self.drawplacidian(draw, x, y, tableclr)
		else:
			self.drawregiomontan(draw, x, y, tableclr)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawplacidian(self, draw, x, y, clr):
		clrtxt = (0,0,0)
		if not self.bw:
			clrtxt = self.options.clrtexts

		txts = (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'], mtexts.txts['AscDiffLat'], mtexts.txts['Semiarcus'], mtexts.txts['Meridiandist'], mtexts.txts['Horizondist'], mtexts.txts['TemporalHour'], mtexts.txts['HourlyDist'], mtexts.txts['PMP'], mtexts.txts['AscDiffPole'], mtexts.txts['PoleHeight'], mtexts.txts['AODO'])

		#top horizontal line
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=clr)

		j = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if not self.options.speculums[self.speculum][i]:
				continue

			wsp,hsp = draw.textsize(' ', self.fntText)
			w,h = draw.textsize(txts[i], self.fntText)
			draw.text((x+2*wsp, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txts[i], fill=clrtxt, font=self.fntText)

			data = self.cpt.speculums[self.speculum][i]
			d,m,s = util.decToDeg(data)

			if i == customerpd.CustomerPD.LONG:
				lon = self.cpt.speculums[self.speculum][customerpd.CustomerPD.LONG]
				if self.options.ayanamsha != 0:
					lon -= self.chart.ayanamsha
					lon = util.normalize(lon)

				d,m,s = util.decToDeg(lon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offs = (self.CELL_WIDTH-w-wsp-wsg)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
				draw.text((x+self.CELL_WIDTH+offs+w+wsp, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clrtxt, font=self.fntMorinus)
			elif i == customerpd.CustomerPD.LAT or i == customerpd.CustomerPD.DECL or i == customerpd.CustomerPD.ADLAT:
				sign = ''
				if data < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)				
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
			elif i == customerpd.CustomerPD.RA or i == customerpd.CustomerPD.PMP or i == customerpd.CustomerPD.ADPH or i == customerpd.CustomerPD.POH:
				txt = (str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if i == customerpd.CustomerPD.RA:
					if self.options.intime:
						d,m,s = util.decToDeg(data/15.0)
						txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
					else:
						txt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)				
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
			elif i == customerpd.CustomerPD.SA or i == customerpd.CustomerPD.MD or i == customerpd.CustomerPD.HD or i == customerpd.CustomerPD.TH or i == customerpd.CustomerPD.HOD or i == customerpd.CustomerPD.AODO:
				sign = ''
				if i == customerpd.CustomerPD.SA or i == customerpd.CustomerPD.TH or i == customerpd.CustomerPD.HOD: 
					sign = 'D'
					if data < 0.0:
						sign = 'N'
				elif i == customerpd.CustomerPD.MD:
					sign = 'M'
					if data < 0.0:
						sign = 'I'
				elif i == customerpd.CustomerPD.HD:
					sign = 'A'
					if data < 0.0:
						sign = 'D'
				elif i == customerpd.CustomerPD.AODO:
					sign = 'A'
					if data < 0.0:
						sign = 'D'
				txt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)

			draw.line((x, y+(j+1)*self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+(j+1)*self.LINE_HEIGHT), fill=clr)

			j += 1

		#side-lines
		draw.line((x, y, x, y+self.TABLE_HEIGHT), fill=clr)
		draw.line((x+self.CELL_WIDTH, y, x+self.CELL_WIDTH, y+self.TABLE_HEIGHT), fill=clr)
		draw.line((x+2*self.CELL_WIDTH, y, x+2*self.CELL_WIDTH, y+self.TABLE_HEIGHT), fill=clr)



	def drawregiomontan(self, draw, x, y, clr):
		clrtxt = (0,0,0)
		if not self.bw:
			clrtxt = self.options.clrtexts

		txts = (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'], mtexts.txts['Meridiandist'], mtexts.txts['Horizondist'], mtexts.txts['ZD'], mtexts.txts['Pole'], mtexts.txts['Q'], mtexts.txts['WReg'], mtexts.txts['CMP'], mtexts.txts['RMP'])

		#top horizontal line
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=clr)

		j = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if not self.options.speculums[self.speculum][i]:
				continue

			wsp,hsp = draw.textsize(' ', self.fntText)
			w,h = draw.textsize(txts[i], self.fntText)
			draw.text((x+2*wsp, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txts[i], fill=clrtxt, font=self.fntText)

			data = self.cpt.speculums[self.speculum][i]
			d,m,s = util.decToDeg(data)

			if i == customerpd.CustomerPD.LONG:
				lon = self.cpt.speculums[self.speculum][customerpd.CustomerPD.LONG]
				if self.options.ayanamsha != 0:
					lon -= self.chart.ayanamsha
					lon = util.normalize(lon)

				d,m,s = util.decToDeg(lon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offs = (self.CELL_WIDTH-w-wsp-wsg)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
				draw.text((x+self.CELL_WIDTH+offs+w+wsp, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clrtxt, font=self.fntMorinus)
			elif i == customerpd.CustomerPD.LAT or i == customerpd.CustomerPD.DECL or i == customerpd.CustomerPD.Q:
				sign = ''
				if data < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)				
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
			elif i == customerpd.CustomerPD.RA or i == customerpd.CustomerPD.ZD or i == customerpd.CustomerPD.POLE or i == customerpd.CustomerPD.W or i == customerpd.CustomerPD.CMP or i == customerpd.CustomerPD.RMP:
				sign = ''
				if i == customerpd.CustomerPD.ZD:
					sign = 'Z'
					if data < 0.0:
						sign = 'N'

				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if i == customerpd.CustomerPD.RA:
					if self.options.intime:
						d,m,s = util.decToDeg(data/15.0)
						txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
					else:
						txt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)				
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)
			elif i == customerpd.CustomerPD.RMD or i == customerpd.CustomerPD.RHD:
				sign = ''
				if i == customerpd.CustomerPD.RMD:
					sign = 'M'
					if data < 0.0:
						sign = 'I'
				else:
					sign = 'A'
					if data < 0.0:
						sign = 'D'

				txt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offs = (self.CELL_WIDTH-w)/2
				draw.text((x+self.CELL_WIDTH+offs, y+self.LINE_HEIGHT*j+(self.LINE_HEIGHT-h)/2), txt, fill=clrtxt, font=self.fntText)

			draw.line((x, y+(j+1)*self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+(j+1)*self.LINE_HEIGHT), fill=clr)

			j += 1

		#side-lines
		draw.line((x, y, x, y+self.TABLE_HEIGHT), fill=clr)
		draw.line((x+self.CELL_WIDTH, y, x+self.CELL_WIDTH, y+self.TABLE_HEIGHT), fill=clr)
		draw.line((x+2*self.CELL_WIDTH, y, x+2*self.CELL_WIDTH, y+self.TABLE_HEIGHT), fill=clr)




