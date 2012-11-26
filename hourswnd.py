import wx
import os
import Image, ImageDraw, ImageFont
import astrology
import chart
import common
import commonwnd
import hours
import util
import mtexts


class HoursWnd(commonwnd.CommonWnd):
	HOURSPERHALFDAY = 12

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.COLUMN_NUM = 2
		self.LINE_NUM = HoursWnd.HOURSPERHALFDAY #Planets
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.SMALL_CELL_WIDTH = 2*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.TITLE_HEIGHT = 3*self.LINE_HEIGHT
		self.TITLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)
		self.SPACE_TITLEY = 0
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Hrs']


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
		lon = self.chart.place.deglon+self.chart.place.minlon/60.0
		if not self.chart.place.east:
			lon *= -1
		offs = lon*4.0/1440.0
		jdlocal = self.chart.time.jd+offs
		jy, jm, jd, jh = astrology.swe_revjul(jdlocal, 1)
		hh, mm, ss = util.decToDeg(jh)

		txt = mtexts.txts['LocalBirthTime']+': '+str(hh)+':'+str(mm).zfill(2)+':'+str(ss).zfill(2)
		w,h = draw.textsize(txt, self.fntText)
		draw.text((BOR+(self.TITLE_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		if self.chart.time.ph != None:
			rh, rm, rs = self.chart.time.ph.revTime(self.chart.time.ph.risetime)
			sh, sm, ss = self.chart.time.ph.revTime(self.chart.time.ph.settime)
			if self.chart.time.ph.daytime:
				txt1 = mtexts.txts['RiseTime']+': '+str(rh)+':'+str(rm).zfill(2)+':'+str(rs).zfill(2)
				txt2 = mtexts.txts['SetTime']+': '+str(sh)+':'+str(sm).zfill(2)+':'+str(ss).zfill(2)
			else:
				txt2 = mtexts.txts['RiseTime']+': '+str(rh)+':'+str(rm).zfill(2)+':'+str(rs).zfill(2)
				txt1 = mtexts.txts['SetTime']+': '+str(sh)+':'+str(sm).zfill(2)+':'+str(ss).zfill(2)

			w,h = draw.textsize(txt1, self.fntText)
			draw.text((BOR+(self.TITLE_WIDTH-w)/2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt1, fill=txtclr, font=self.fntText)
			w,h = draw.textsize(txt2, self.fntText)
			draw.text((BOR+(self.TITLE_WIDTH-w)/2, BOR+2*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt2, fill=txtclr, font=self.fntText)

			x = BOR
			y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

			self.begtime = 0.0
			if self.chart.time.ph.daytime:
				self.begtime = self.chart.time.ph.risetime
			else:
				self.begtime = self.chart.time.ph.settime
			for i in range(int(HoursWnd.HOURSPERHALFDAY)):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, i)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		hr = 0
		endtime = 0.0

		if self.chart.time.ph.daytime:
			endtime = self.chart.time.ph.risetime+self.chart.time.ph.hrlen*(idx+1)
			hr = idx
		else:
			endtime = self.chart.time.ph.settime+self.chart.time.ph.hrlen*(idx+1)
			hr = idx+int(HoursWnd.HOURSPERHALFDAY)

		planetaryhour = hours.PlanetaryHours.PHs[self.chart.time.ph.weekday][hr]

		summa = 0
		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == 1:
				tclr = (0,0,0)
				if not self.bw:
					if self.options.useplanetcolors:
						tclr = self.options.clrindividual[planetaryhour]
					else:
						dign = self.chart.dignity(planetaryhour)
						tclr = self.clrs[dign]

				txtpl = common.common.Planets[planetaryhour] 
				w,h = draw.textsize(txtpl, self.fntMorinus)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txtpl, fill=tclr, font=self.fntMorinus)
			elif i > 1:
				h, m, s = 0, 0, 0
				if i == 2:
					h, m, s = self.chart.time.ph.revTime(self.begtime)
				else:
					h, m, s = self.chart.time.ph.revTime(endtime)

				txt = str(h)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

				self.begtime = endtime

			summa += offs[i]








