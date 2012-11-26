import os
import math
import wx
import Image, ImageDraw, ImageFont
import common
import astrology
import chart
import houses
import fortune
import primdirs
import pdsinchart
import pdsinchartstepperdlg
import pdsinchartframe
import pdsinchartingressframe
import pdsinchartdlgopts
import fixstars
import mtexts
import util


class PrimDirsListWnd(wx.ScrolledWindow):
	SCROLL_RATE = 20
	BORDER = 20

	def __init__(self, parent, chrt, options, pds, mainfr, currpage, maxpage, fr, to, id = -1, size = wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

		self.parent = parent
		self.chart = chrt
		self.options = options
		self.bw = self.options.bw
		self.pds = pds
		self.mainfr = mainfr

		self.SetBackgroundColour(self.options.clrbackground)
		self.SetScrollRate(PrimDirsListWnd.SCROLL_RATE, PrimDirsListWnd.SCROLL_RATE)

		self.pmenu = wx.Menu()
		self.ID_SaveAsBitmap = wx.NewId()
		self.ID_SaveAsText = wx.NewId()
		self.ID_BlackAndWhite = wx.NewId()
		if chrt.htype == chart.Chart.RADIX:
			self.ID_PDsInChartInZod = wx.NewId()
			self.ID_PDsInChartInMun = wx.NewId()
			self.ID_PDsInChartIngress = wx.NewId()

		self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txts['SaveAsBmp'], mtexts.txts['SaveTable'])
		self.pmenu.Append(self.ID_SaveAsText, mtexts.txts['SaveAsText'], mtexts.txts['SavePDs'])
		mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txts['BlackAndWhite'], mtexts.txts['TableBW'], wx.ITEM_CHECK)
		if chrt.htype == chart.Chart.RADIX:
			self.pmenu.Append(self.ID_PDsInChartInZod, mtexts.txts['PDsInChartInZod'], mtexts.txts['PDsInChartInZod'])
			self.pmenu.Append(self.ID_PDsInChartInMun, mtexts.txts['PDsInChartInMun'], mtexts.txts['PDsInChartInMun'])
			self.pmenu.Append(self.ID_PDsInChartIngress, mtexts.txts['PDsInChartIngress'], mtexts.txts['PDsInChartIngress'])
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
		self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
		self.Bind(wx.EVT_MENU, self.onSaveAsText, id=self.ID_SaveAsText)
		self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
		if chrt.htype == chart.Chart.RADIX:
			self.Bind(wx.EVT_MENU, self.onPDsInChartZod, id=self.ID_PDsInChartInZod)
			self.Bind(wx.EVT_MENU, self.onPDsInChartMun, id=self.ID_PDsInChartInMun)
			self.Bind(wx.EVT_MENU, self.onPDsInChartIngress, id=self.ID_PDsInChartIngress)

		if (self.bw):
			mbw.Check()

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = (self.FONT_SIZE/2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = parent.LINE_NUM #Per column
		self.COLUMN_NUM = 6

		self.currpage = currpage
		self.maxpage = maxpage
		self.fr = fr
		self.to = to

		self.SMALL_CELL_WIDTH = (4*self.FONT_SIZE)
		self.CELL_WIDTH = (6*self.FONT_SIZE)
		self.BIG_CELL_WIDTH = (8*self.FONT_SIZE)
		self.TABLE_WIDTH = (2*self.SMALL_CELL_WIDTH+3*self.CELL_WIDTH+self.BIG_CELL_WIDTH)
		self.SPACE_TITLEY = 4
		self.TITLE_CELL_HEIGHT = (2*self.LINE_HEIGHT)
		self.TABLE_HEIGHT = ((self.TITLE_CELL_HEIGHT)+(self.SPACE_TITLEY)+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.SPACE_BETWEEN_TABLESX = 4
		self.TITLE_CELL_WIDTH = (2*self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX+1)
		self.SECOND_TABLE_OFFSX = (self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX)
	
		self.WIDTH = (PrimDirsListWnd.BORDER+self.TITLE_CELL_WIDTH+PrimDirsListWnd.BORDER)
		self.HEIGHT = (PrimDirsListWnd.BORDER+self.TABLE_HEIGHT+PrimDirsListWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntAspects = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/4)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)

		self.drawBkg()
		self.curposx = None
		self.curposy = None


	def onPopupMenu(self, event):
		self.curposx, self.curposy = event.GetPosition()
		self.PopupMenu(self.pmenu, event.GetPosition())


	def onSaveAsBitmap(self, event):
		name = self.chart.name+mtexts.txts['PD']
		dlg = wx.FileDialog(self, mtexts.txts['SaveAsBmp'], '', name, mtexts.txts['BMPFiles'], wx.FD_SAVE)
		if os.path.isdir(self.mainfr.fpathimgs):
			dlg.SetDirectory(self.mainfr.fpathimgs)
		else:
			dlg.SetDirectory(u'.')

		if (dlg.ShowModal() == wx.ID_OK):
			dpath = dlg.GetDirectory()
			fpath = dlg.GetPath()
			if (not fpath.endswith(u'.bmp')):
				fpath+=u'.bmp'
			#Check if fpath already exists!?
			if (os.path.isfile(fpath)):
 				dlgm = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
				if (dlgm.ShowModal() == wx.ID_NO):
					dlgm.Destroy()
					dlg.Destroy()
					return
				dlgm.Destroy()

			self.mainfr.fpathimgs = dpath
			self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_BMP)

		dlg.Destroy()


	def onSaveAsText(self, event):
		if self.options.langid != 0:
			dlg = wx.MessageDialog(self, mtexts.txts['SwitchToEnglish'], mtexts.txts['Message'], wx.OK)
			dlg.ShowModal()
			return		

		name = self.chart.name+mtexts.txts['PD']
		dlg = wx.FileDialog(self, mtexts.txts['SaveAsText'], '', name, mtexts.txts['TXTFiles'], wx.FD_SAVE)
		if os.path.isdir(self.mainfr.fpathimgs):
			dlg.SetDirectory(self.mainfr.fpathimgs)
		else:
			dlg.SetDirectory(u'.')

		if dlg.ShowModal() == wx.ID_OK:
			dpath = dlg.GetDirectory()
			fpath = dlg.GetPath()
			if not fpath.endswith(u'.txt'):
				fpath+=u'.txt'
			#Check if fpath already exists!?
			if os.path.isfile(fpath):
 				dlg = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
				if dlg.ShowModal() == wx.ID_NO:
					return

			self.mainfr.fpathimgs = dpath
			self.pds.print2file(fpath)		


	def onBlackAndWhite(self, event):
		if (self.bw != event.IsChecked()):
			self.bw = event.IsChecked()
			self.drawBkg()
			self.Refresh()


	def onPDsInChartZod(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and self.pds.pds[pdnum].mundane:
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, False)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartframe.PDsInChartFrame(self.mainfr, txt, pdchart, self.chart, self.options)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, False)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def onPDsInChartMun(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and not self.pds.pds[pdnum].mundane:# and "From the planets" in Options (Disable the Terrestrial-menuitem instead)
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, True)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartframe.PDsInChartFrame(self.mainfr, txt, pdchart, self.chart, self.options, 0, False)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, True)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def onPDsInChartIngress(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and self.pds.pds[pdnum].mundane:
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, False)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			return

		#create Ingress-chart
		cal = chart.Time.GREGORIAN
		if self.chart.time.cal == chart.Time.JULIAN:
			cal = chart.Time.JULIAN
		tim = chart.Time(y, m, d, ho, mi, se, self.chart.time.bc, cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
		ingchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartingressframe.PDsInChartIngressFrame(self.mainfr, txt, self.chart, pdchart, ingchart, self.options)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, False)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def calc(self, event, terrestrial):
		valid, pdnum = self.getPDNum(event)

		if valid:
			y, m, d, t = astrology.swe_revjul(self.pds.pds[pdnum].time, 1)
			ho, mi, se = util.decToDeg(t)

			da = self.pds.pds[pdnum].arc
			if not self.pds.pds[pdnum].direct:
				da *= -1

			pdinch = pdsinchart.PDsInChart(self.chart, da) #self.yz, mz, dz, tz ==> chart
			pdh, pdm, pds = util.decToDeg(pdinch.tz)
			cal = chart.Time.GREGORIAN
			if self.chart.time.cal == chart.Time.JULIAN:
				cal = chart.Time.JULIAN
			tim = chart.Time(pdinch.yz, pdinch.mz, pdinch.dz, pdh, pdm, pds, self.chart.time.bc, cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			if not terrestrial:
				if self.options.pdincharttyp == pdsinchartdlgopts.PDsInChartsDlgOpts.FROMMUNDANEPOS:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)
					#modify planets ...
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.planets.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.houses = houses.Houses(tim.jd, 0, pdchart.place.lat, pdchart.place.lon, 'R', pdchart.obl[0], self.options.ayanamsha, pdchart.ayanamsha)
						pdchart.planets.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])

					#modify lof
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.fortune.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.fortune.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])

				elif self.options.pdincharttyp == pdsinchartdlgopts.PDsInChartsDlgOpts.FROMZODIACALPOS:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False, chart.Chart.YEAR, True)

					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False, chart.Chart.YEAR, True)
					#modify planets ...
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.planets.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.houses = houses.Houses(tim.jd, 0, pdchart.place.lat, pdchart.place.lon, 'R', pdchart.obl[0], self.options.ayanamsha, pdchart.ayanamsha)
						pdchart.planets.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])

					#modify lof
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.fortune.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.fortune.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
	
				else:#Full Astronomical Procedure
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)

					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)

					pdpls = pdchartpls.planets.planets
					if self.options.pdinchartsecmotion:
						pdpls = pdchart.planets.planets

					raequasc, declequasc, dist = astrology.swe_cotrans(pdchart.houses.ascmc[houses.Houses.EQUASC], 0.0, 1.0, -self.chart.obl[0])
					pdchart.planets.calcFullAstronomicalProc(da, self.chart.obl[0], pdpls, pdchart.place.lat, pdchart.houses.ascmc2, raequasc) #planets
					pdchart.fortune.calcFullAstronomicalProc(pdchartpls.fortune, da, self.chart.obl[0]) 

			else:
				if self.options.pdinchartterrsecmotion:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
				else:
					pdchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
					raequasc, declequasc, dist = astrology.swe_cotrans(pdchart.houses.ascmc[houses.Houses.EQUASC], 0.0, 1.0, -self.chart.obl[0])
					pdchart.planets.calcMundaneWithoutSM(da, self.chart.obl[0], pdchart.place.lat, pdchart.houses.ascmc2, raequasc)

				pdchart.fortune.recalcForMundaneChart(self.chart.fortune.fortune[fortune.Fortune.LON], self.chart.fortune.fortune[fortune.Fortune.LAT], self.chart.fortune.fortune[fortune.Fortune.RA], self.chart.fortune.fortune[fortune.Fortune.DECL], pdchart.houses.ascmc2, pdchart.raequasc, pdchart.obl[0], pdchart.place.lat)


			keytxt = mtexts.typeListDyn[self.options.pdkeyd]
			if not self.options.pdkeydyn:
				keytxt = mtexts.typeListStat[self.options.pdkeys]

			return True, y, m, d, ho, mi, se, t, mtexts.typeListDirs[self.options.primarydir], keytxt, self.pds.pds[pdnum].direct, math.fabs(da), pdchart

		else:
			return False, 2000, 1, 1, 1, 1, 1, 1.0, '', '', True, 0.0, None


	def getPDNum(self, event):
		xu, yu = self.GetScrollPixelsPerUnit()
		xs, ys = self.GetViewStart()
		yscrolledoffs = yu*ys
		xscrolledoffs = xu*xs
		x,y = self.curposx, self.curposy
		offs = PrimDirsListWnd.BORDER+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY

		self.SECOND_TABLE_OFFSX = (self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX)
		if (y+yscrolledoffs > offs and y+yscrolledoffs < offs+self.TABLE_HEIGHT) and ((x+xscrolledoffs > PrimDirsListWnd.BORDER and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.TABLE_WIDTH) or (x+xscrolledoffs > PrimDirsListWnd.BORDER+self.SECOND_TABLE_OFFSX and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.SECOND_TABLE_OFFSX+self.TABLE_WIDTH)):
			col = 0
			rownum = (y+yscrolledoffs-offs)/self.LINE_HEIGHT
			if x+xscrolledoffs > PrimDirsListWnd.BORDER and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.TABLE_WIDTH:
				pass
			else:
				col = 1

			pdnum = (self.currpage-1)*2*self.LINE_NUM+self.LINE_NUM*col+rownum

			return pdnum < len(self.pds.pds), pdnum


	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)


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

		#Title
		BOR = PrimDirsListWnd.BORDER
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_CELL_WIDTH, BOR+self.TITLE_CELL_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		dirtxt = mtexts.typeListDirs[self.options.primarydir]
		keytypetxt = mtexts.txts['DynamicKey']
		if not self.options.pdkeydyn:
			keytypetxt = mtexts.txts['StaticKey']
		keytxt = mtexts.typeListDyn[self.options.pdkeyd]
		if not self.options.pdkeydyn:
			keytxt = mtexts.typeListStat[self.options.pdkeys]

		clr = self.options.clrtexts
		if self.bw:
			clr = (0,0,0)
		txt = dirtxt+'   '+keytypetxt+': '+keytxt
		w,h = draw.textsize(txt, self.fntText)
		draw.text((BOR+(self.TITLE_CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)

		txt = str(self.currpage)+' / '+str(self.maxpage)
		draw.text((BOR+self.TITLE_CELL_WIDTH-self.TITLE_CELL_WIDTH/10, BOR+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)

		txt = (mtexts.txts['MZ'], mtexts.txts['Prom'], mtexts.txts['DC'], mtexts.txts['Sig'], mtexts.txts['Arc'], mtexts.txts['Date'])
		widths = (self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.BIG_CELL_WIDTH)
		summa = 0
		for i in range(self.COLUMN_NUM):
			w,h = draw.textsize(txt[i], self.fntText)
			draw.text((BOR+summa+(widths[i]-w)/2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt[i], fill=clr, font=self.fntText)
			summa += widths[i]
		summa = 0
		for i in range(self.COLUMN_NUM):
			w,h = draw.textsize(txt[i], self.fntText)
			draw.text((self.SECOND_TABLE_OFFSX+BOR+summa+(widths[i]-w)/2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt[i], fill=clr, font=self.fntText)
			summa += widths[i]

		#Tables
		x = BOR
		y = BOR+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
		rng = self.to-self.fr #+1!?
		lim = rng
		leftovers = False
		if lim > self.LINE_NUM:
			lim = self.LINE_NUM
			leftovers = True
		idx = self.fr
		for i in range(lim):
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, idx, tableclr)
			idx += 1
		if leftovers:
			x = BOR+self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX
			y = BOR+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
			lim = rng-self.LINE_NUM##
			idx = self.fr+self.LINE_NUM##
			for i in range(lim):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, idx, tableclr)
				idx += 1

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def	display(self, currpage, fr, to):
		self.currpage = currpage
		self.fr = fr
		self.to = to

		self.drawBkg()
		self.Refresh()


	def drawline(self, draw, x, y, idx, clr):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines and PD
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.BIG_CELL_WIDTH)

		BOR = PrimDirsListWnd.BORDER
		summa = 0
		txtclr = self.options.clrtexts
		if self.bw:
			txtclr = (0,0,0)
		for i in range(self.COLUMN_NUM+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)
			#pd
			if i == 1:#M/Z
				mtxt = mtexts.txts['M']
				if not self.pds.pds[idx].mundane:
					mtxt = mtexts.txts['Z']
				
				w,h = draw.textsize(mtxt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), mtxt, fill=txtclr, font=self.fntText)
			elif i == 2:#Prom
				if self.pds.pds[idx].promasp == chart.Chart.MIDPOINT or self.pds.pds[idx].sigasp == chart.Chart.RAPTPAR or self.pds.pds[idx].sigasp == chart.Chart.RAPTCONTRAPAR:
					promtxt = common.common.Planets[self.pds.pds[idx].prom]
					prom2txt = common.common.Planets[self.pds.pds[idx].prom2]

					wp,hp = draw.textsize(promtxt, self.fntMorinus)
					wsp,hsp = draw.textsize(' ', self.fntText)
					wp2,hp2 = draw.textsize(prom2txt, self.fntMorinus)
					offset = (offs[i]-(wp+wsp+wp2))/2
					tclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].prom)]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=tclr, font=self.fntMorinus)
					tclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom2
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].prom2)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hp2)/2), prom2txt, fill=tclr, font=self.fntMorinus)
				elif self.pds.pds[idx].prom >= primdirs.PrimDir.ANTISCION and self.pds.pds[idx].prom < primdirs.PrimDir.TERM:
					promasptxt = ''
					wspa = 0
					wsp,hsp = draw.textsize(' ', self.fntText)
					if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO:
						promasptxt += common.common.Aspects[self.pds.pds[idx].promasp]
						wspa = wsp
					wa,ha = draw.textsize(promasptxt, self.fntAspects)

					anttxt = mtexts.txts['Antis']
					if self.pds.pds[idx].prom >= primdirs.PrimDir.CONTRAANT:
						anttxt = mtexts.txts['ContraAntis']
					wt,ht = draw.textsize(anttxt, self.fntText)

					promtxt = ''
					promfnt = None
					antoffs = 0
					tclr = (0,0,0)
					if self.pds.pds[idx].prom == primdirs.PrimDir.ANTISCIONLOF or self.pds.pds[idx].prom == primdirs.PrimDir.CONTRAANTLOF:
						promtxt = common.common.fortune
						promfnt = self.fntMorinus
						if not self.bw:
							if self.options.useplanetcolors:
								tclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1]
							else:
								tclr = self.options.clrperegrin
					elif self.pds.pds[idx].prom == primdirs.PrimDir.ANTISCIONASC or self.pds.pds[idx].prom == primdirs.PrimDir.CONTRAANTASC:
						promtxt = mtexts.txts['Asc']
						promfnt = self.fntText				
						if not self.bw:
							tclr = txtclr
					elif self.pds.pds[idx].prom == primdirs.PrimDir.ANTISCIONMC or self.pds.pds[idx].prom == primdirs.PrimDir.CONTRAANTMC:
						promtxt = mtexts.txts['MC']
						promfnt = self.fntText				
						if not self.bw:
							tclr = txtclr
					else:
						antoffs = primdirs.PrimDir.ANTISCION
						if self.pds.pds[idx].prom >= primdirs.PrimDir.CONTRAANT:
							antoffs = primdirs.PrimDir.CONTRAANT

						promtxt = common.common.Planets[self.pds.pds[idx].prom-antoffs]
						promfnt = self.fntMorinus

						if not self.bw:
							if self.options.useplanetcolors:
								objidx = self.pds.pds[idx].prom-antoffs
								if objidx == astrology.SE_MEAN_NODE+1:
									objidx = astrology.SE_MEAN_NODE
								elif objidx > astrology.SE_MEAN_NODE+1:
									objidx = astrology.SE_MEAN_NODE+1
								tclr = self.options.clrindividual[objidx]
							else:
								tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].prom-antoffs)]

					wp,hp = draw.textsize(promtxt, promfnt)

					offset = (offs[i]-(wa+wspa+wt+wsp+wp))/2
					if promasptxt != '':
						clrasp = (0,0,0)
						if not self.bw:
							if self.pds.pds[idx].promasp == chart.Chart.PARALLEL or self.pds.pds[idx].promasp == chart.Chart.CONTRAPARALLEL:
								clrasp = self.options.clrperegrin
							else:
								clrasp = self.options.clraspect[self.pds.pds[idx].promasp]
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)/2), promasptxt, fill=clrasp, font=self.fntAspects)

					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-ht)/2), anttxt, fill=txtclr, font=self.fntText)
					draw.text((x+summa+offset+wa+wspa+wt+wsp, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=tclr, font=promfnt)
				elif self.pds.pds[idx].prom >= primdirs.PrimDir.TERM and self.pds.pds[idx].prom < primdirs.PrimDir.FIXSTAR:
					signs = common.common.Signs1
					if not self.options.signs:
						signs = common.common.Signs2
					promtxt = signs[self.pds.pds[idx].prom-primdirs.PrimDir.TERM]
					prom2txt = common.common.Planets[self.pds.pds[idx].prom2]

					wp,hp = draw.textsize(promtxt, self.fntMorinus)
					wsp,hsp = draw.textsize(' ', self.fntText)
					wp2,hp2 = draw.textsize(prom2txt, self.fntMorinus)
					offset = (offs[i]-(wp+wsp+wp2))/2
					sclr = (0,0,0)
					if not self.bw:
						sclr = self.options.clrsigns
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=sclr, font=self.fntMorinus)
					tclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom2
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].prom2)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hp2)/2), prom2txt, fill=tclr, font=self.fntMorinus)
				elif self.pds.pds[idx].prom >= primdirs.PrimDir.FIXSTAR:
					promtxt = self.chart.fixstars.data[self.pds.pds[idx].prom-primdirs.PrimDir.FIXSTAR][fixstars.FixStars.NOMNAME]
					if self.options.usetradfixstarnamespdlist:
						tradname = self.chart.fixstars.data[self.pds.pds[idx].prom-primdirs.PrimDir.FIXSTAR][fixstars.FixStars.NAME].strip()
						if tradname != '':
							promtxt = tradname
					w,h = draw.textsize(promtxt, self.fntText)
					draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), promtxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].prom == primdirs.PrimDir.LOF:
					lofclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							lofclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1]
						else:
							lofclr = self.options.clrperegrin

					promtxt = common.common.fortune
					wp,hp = draw.textsize(promtxt, self.fntMorinus)
					offset = (offs[i]-wp)/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=lofclr, font=self.fntMorinus)
				elif self.pds.pds[idx].prom == primdirs.PrimDir.CUSTOMERPD:
					promtxt = mtexts.txts['Customer2']
					wp,hp = draw.textsize(promtxt, self.fntText)
					offset = (offs[i]-wp)/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].prom == primdirs.PrimDir.ASC or self.pds.pds[idx].prom == primdirs.PrimDir.MC:
					promasptxt = ''
					if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO:
						promasptxt += common.common.Aspects[self.pds.pds[idx].promasp]
					promtxt = mtexts.txts['Asc']
					if self.pds.pds[idx].prom == primdirs.PrimDir.MC:
						promtxt = mtexts.txts['MC']
					wa,ha = draw.textsize(promasptxt, self.fntAspects)
					wsp,hsp = draw.textsize(' ', self.fntText)
					ws,hs = draw.textsize(promtxt, self.fntText)
					offset = (offs[i]-(wa+wsp+ws))/2
					clrasp = (0,0,0)
					if not self.bw:
						if self.pds.pds[idx].promasp == chart.Chart.PARALLEL or self.pds.pds[idx].promasp == chart.Chart.CONTRAPARALLEL:
							clrasp = self.options.clrperegrin
						else:
							clrasp = self.options.clraspect[self.pds.pds[idx].promasp]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)/2), promasptxt, fill=clrasp, font=self.fntAspects)
					draw.text((x+summa+offset+wa+wsp, y+(self.LINE_HEIGHT-hs)/2), promtxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].prom >= primdirs.PrimDir.HC2 and self.pds.pds[idx].prom < primdirs.PrimDir.LOF:#Sig is HC
					HCs = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])
					hctxt = HCs[self.pds.pds[idx].sig-primdirs.PrimDir.HC2]
					ws,hs = draw.textsize(hctxt, self.fntText)
					offset = (offs[i]-ws)/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hs)/2), hctxt, fill=txtclr, font=self.fntText)
				else:
					promtxt = common.common.Planets[self.pds.pds[idx].prom]
					promasptxt = ''
					if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO:
						promasptxt += common.common.Aspects[self.pds.pds[idx].promasp]
	
					wp,hp = draw.textsize(promtxt, self.fntMorinus)
					wa,ha = draw.textsize(promasptxt, self.fntAspects)
					wsp,hsp = draw.textsize(' ', self.fntText)
					wspa = 0
					if promasptxt != '':
						wspa = wsp
					offset = (offs[i]-(wa+wspa+wp+wsp))/2
					tclr = (0,0,0)
					if promasptxt != '':
						clrasp = (0,0,0)
						if not self.bw:
							if self.pds.pds[idx].promasp == chart.Chart.PARALLEL or self.pds.pds[idx].promasp == chart.Chart.CONTRAPARALLEL:
								clrasp = self.options.clrperegrin
							else:
								clrasp = self.options.clraspect[self.pds.pds[idx].promasp]
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)/2), promasptxt, fill=clrasp, font=self.fntAspects)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].prom)]
					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-hp)/2), promtxt, fill=tclr, font=self.fntMorinus)
			elif i == 3:#D/C
				dirtxt = mtexts.txts['D']
				if not self.pds.pds[idx].direct:
					dirtxt = mtexts.txts['C']
				
				w,h = draw.textsize(dirtxt, self.fntText)
				wsp,hsp = draw.textsize(' ', self.fntText)
				warr,harr = draw.textsize('-', self.fntSymbol)
				offset = (offs[i]-(w+wsp+warr))/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), dirtxt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-harr)/2), '-', fill=txtclr, font=self.fntSymbol)
			elif i == 4:#Sig
				#AscMC(+asp), HC, Planet, Asp of a planet, parallel, contraparallel, raptparallel
				#Display aspect(conjuntio also!!) except for Asc,MC,HC
				if self.pds.pds[idx].sigasp == chart.Chart.PARALLEL or self.pds.pds[idx].sigasp == chart.Chart.CONTRAPARALLEL:
					#Par Sig(Asc,Desc,MC,IC)
					partxt = 'X'
					if self.pds.pds[idx].parallelaxis == 0 and self.pds.pds[idx].sigasp == chart.Chart.CONTRAPARALLEL:
						partxt = 'Y'
					wp,hp = draw.textsize(partxt, self.fntAspects)
					sigtxt = common.common.Planets[self.pds.pds[idx].sig]
					ws,hs = draw.textsize(sigtxt, self.fntMorinus)
					wsp,hsp = draw.textsize(' ', self.fntText)
					angles = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')
					angletxt = ''
					if self.pds.pds[idx].parallelaxis != 0:
						angletxt = angles[self.pds.pds[idx].parallelaxis-primdirs.PrimDir.OFFSANGLES]
					wa,ha = draw.textsize(angletxt, self.fntText)
					offset = (offs[i]-(wp+wsp+ws+wsp+wa))/2
					pclr = (0,0,0)
					if not self.bw:
						pclr = self.options.clrperegrin
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), partxt, fill=pclr, font=self.fntAspects)
					tclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].sig
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].sig)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hs)/2), sigtxt, fill=tclr, font=self.fntMorinus)
					draw.text((x+summa+offset+wp+wsp+ws+wsp, y+(self.LINE_HEIGHT-ha)/2), angletxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].sigasp == chart.Chart.RAPTPAR or self.pds.pds[idx].sigasp == chart.Chart.RAPTCONTRAPAR:
					#R Par (Asc,Desc,MC,IC)
					rapttxt = 'R'
					partxt = 'X'
					wr,hr = draw.textsize(rapttxt, self.fntText)
					wp,hp = draw.textsize(partxt, self.fntAspects)
					wsp,hsp = draw.textsize(' ', self.fntText)
					angles = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')
					angletxt = angles[self.pds.pds[idx].parallelaxis-primdirs.PrimDir.OFFSANGLES]
					wa,ha = draw.textsize(angletxt, self.fntText)
					offset = (offs[i]-(wr+wp+wsp+wsp+wa))/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hr)/2), rapttxt, fill=txtclr, font=self.fntText)
					pclr = (0,0,0)
					if not self.bw:
						pclr = self.options.clrperegrin
					draw.text((x+summa+offset+wr, y+(self.LINE_HEIGHT-hp)/2), partxt, fill=pclr, font=self.fntAspects)
					draw.text((x+summa+offset+wr+wp+wsp, y+(self.LINE_HEIGHT-ha)/2), angletxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].sig == primdirs.PrimDir.LOF:
					lofclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							lofclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1]
						else:
							lofclr = self.options.clrperegrin

					sigtxt = common.common.fortune
					wp,hp = draw.textsize(sigtxt, self.fntMorinus)

					extra = 0
					offset = (offs[i]-(wp+extra))/2

					if self.pds.pds[idx].mundane:
						sigasptxt = common.common.Aspects[self.pds.pds[idx].sigasp]
						wa,ha = draw.textsize(sigasptxt, self.fntAspects)
						wsp,hsp = draw.textsize(' ', self.fntText)
						extra = wa+wsp
						offset = (offs[i]-(wp+extra))/2
						clrasp = (0,0,0)
						if not self.bw:
							clrasp = self.options.clraspect[self.pds.pds[idx].sigasp]
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)/2), sigasptxt, fill=clrasp, font=self.fntAspects)

					draw.text((x+summa+offset+extra, y+(self.LINE_HEIGHT-hp)/2), sigtxt, fill=lofclr, font=self.fntMorinus)
				elif self.pds.pds[idx].sig == primdirs.PrimDir.SYZ:
					sigtxt = mtexts.txts['Syzygy']
					wp,hp = draw.textsize(sigtxt, self.fntText)
					offset = (offs[i]-wp)/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), sigtxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].sig == primdirs.PrimDir.CUSTOMERPD:
					sigtxt = mtexts.txts['User2']
					wp,hp = draw.textsize(sigtxt, self.fntText)
					offset = (offs[i]-wp)/2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)/2), sigtxt, fill=txtclr, font=self.fntText)
				elif self.pds.pds[idx].sig >= primdirs.PrimDir.OFFSANGLES and self.pds.pds[idx].sig < primdirs.PrimDir.LOF:#Sig is Asc,MC or HC
					if self.pds.pds[idx].sig <= primdirs.PrimDir.IC:
						angles = (mtexts.txts['Asc'], mtexts.txts['Dsc'], mtexts.txts['MC'], mtexts.txts['IC'])
						anglestxt = angles[self.pds.pds[idx].sig-primdirs.PrimDir.OFFSANGLES]
						ws,hs = draw.textsize(anglestxt, self.fntText)
						offset = (offs[i]-ws)/2
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hs)/2), anglestxt, fill=txtclr, font=self.fntText)
					else: #=>HC
						HCs = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])
						hctxt = HCs[self.pds.pds[idx].sig-primdirs.PrimDir.HC2]
						ws,hs = draw.textsize(hctxt, self.fntText)
						offset = (offs[i]-ws)/2
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hs)/2), hctxt, fill=txtclr, font=self.fntText)
				else:#interplanetary
					sigasptxt = ''
					if self.pds.pds[idx].sigasp != chart.Chart.CONJUNCTIO:
						sigasptxt = common.common.Aspects[self.pds.pds[idx].sigasp]
					wa,ha = draw.textsize(sigasptxt, self.fntAspects)
					wsp,hsp = draw.textsize(' ', self.fntText)
					wspa = 0
					if sigasptxt != '':
						wspa = wsp
					sigtxt = common.common.Planets[self.pds.pds[idx].sig]
					ws,hs = draw.textsize(sigtxt, self.fntMorinus)
					offset = (offs[i]-(wa+wspa+ws))/2
					clrasp = (0,0,0)
					if not self.bw:
						clrasp = self.options.clraspect[self.pds.pds[idx].sigasp]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)/2), sigasptxt, fill=clrasp, font=self.fntAspects)
					tclr = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].sig
							if objidx > astrology.SE_MEAN_NODE:
								objidx = astrology.SE_MEAN_NODE
							tclr = self.options.clrindividual[objidx]
						else:
							tclr = self.clrs[self.chart.dignity(self.pds.pds[idx].sig)]
					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-hs)/2), sigtxt, fill=tclr, font=self.fntMorinus)
			elif i == 5:#Arc
				arc = (int(self.pds.pds[idx].arc*1000))/1000.0
				arctxt = str(arc)
				w,h = draw.textsize(arctxt, self.fntText)
				offset = (offs[i]-w)/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), arctxt, fill=txtclr, font=self.fntText)
			elif i == 6:#Date
				year, month, day, h = astrology.swe_revjul(self.pds.pds[idx].time, 1)
#				ho, mi, se = util.decToDeg(h)
#				year, month, day, extraday = util.revConvDate(self.pds.pds[idx].time)
				txt = (str(year)).rjust(4)+'.'+(str(month)).zfill(2)+'.'+(str(day)).zfill(2)
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-w)/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			summa += offs[i]




 
