import math
import datetime
import wx
import astrology
import planets
import chart
import houses
import fortune
import transits
import pdsinchart
import pdsinchartdlgopts
import intvalidator
import floatvalidator
import rangechecker
import primdirs
import mtexts
import util


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class PDsInChartStepperDlg(wx.Dialog):

	def __init__(self, parent, chrt, y, m, d, t, direct, arc, opts, terrestrial):

		self.parent = parent
		self.chart = chrt
		self.y = y
		self.m = m
		self.d = d
		self.t = t
		self.direct = direct
		self.arc = arc
		self.options = opts
		self.terrestrial = terrestrial

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PDsInChart'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Date
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000
		self.sdate =wx.StaticBox(self, label='')
		datesizer = wx.StaticBoxSizer(self.sdate, wx.VERTICAL)
		self.daterb = wx.RadioButton(self, -1, '', style=wx.RB_GROUP)
		datesizer.Add(self.daterb, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)###
		vsizer = wx.BoxSizer(wx.VERTICAL)
#		self.dateckb = wx.CheckBox(self, -1, mtexts.txts['BC'])
#		vsizer.Add(self.dateckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5)

		fgsizer = wx.FlexGridSizer(2, 3)
		self.yeartxt = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vsizer.Add(self.yeartxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		self.year.SetValue(str(self.y))
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.monthtxt = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vsizer.Add(self.monthtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)
		self.month.SetValue(str(self.m))
		vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.daytxt = wx.StaticText(self, -1, mtexts.txts['Day']+':')
		vsizer.Add(self.daytxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.day.SetHelpText(mtexts.txts['HelpDay'])
		self.day.SetMaxLength(2)
		self.day.SetValue(str(self.d))
		vsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		#time
		ho, mi, se = util.decToDeg(self.t)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.hourtxt = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vsizer.Add(self.hourtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,-1))
		self.hour.SetHelpText(mtexts.txts['HelpHour'])
		vsizer.Add(self.hour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour.SetMaxLength(2)
		self.hour.SetValue(str(ho))
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.minutetxt = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vsizer.Add(self.minutetxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.minute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.minute.SetHelpText(mtexts.txts['HelpMin'])
		self.minute.SetMaxLength(2)
		self.minute.SetValue(str(mi))
		vsizer.Add(self.minute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.secondtxt = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vsizer.Add(self.secondtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.second = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.second.SetHelpText(mtexts.txts['HelpMin'])
		self.second.SetMaxLength(2)
		self.second.SetValue(str(se))
		vsizer.Add(self.second, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		datesizer.Add(fgsizer, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5)###

		#DA
		self.sda = wx.StaticBox(self, label='')
		dasizer = wx.StaticBoxSizer(self.sda, wx.VERTICAL)

		self.arcrb = wx.RadioButton(self, -1, '')
		dasizer.Add(self.arcrb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.datxt = wx.StaticText(self, -1, mtexts.txts['Arc']+':')
		hsizer.Add(self.datxt, 0, wx.ALIGN_CENTER|wx.LEFT, 0)
		self.da = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 100.0), size=(100,-1))
		self.da.SetMaxLength(10)
		hsizer.Add(self.da, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)

		dasizer.Add(vsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		self.da.SetValue(str(self.arc))

		#Direction
		self.sdir = wx.StaticBox(self, label='')
		dirsizer = wx.StaticBoxSizer(self.sdir, wx.VERTICAL)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.positiverb = wx.RadioButton(self, -1, mtexts.txts['Direct'], style=wx.RB_GROUP)
		self.negativerb = wx.RadioButton(self, -1, mtexts.txts['Converse'])
		vsizer.Add(self.positiverb, 0, wx.LEFT, 0)
		vsizer.Add(self.negativerb, 0, wx.LEFT, 0)

		if self.direct:
			self.positiverb.SetValue(True)
		else:
			self.negativerb.SetValue(True)

		dirsizer.Add(vsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)

		#ShowBtn
		self.sshow = wx.StaticBox(self, label='')
		showsizer = wx.StaticBoxSizer(self.sshow, wx.VERTICAL)
		ID_SHOWBTN = wx.NewId()
		self.btnShow = wx.Button(self, ID_SHOWBTN, mtexts.txts['Show'])
		showsizer.Add(self.btnShow, 0, wx.ALIGN_CENTER|wx.ALL, 10)


		mvsizer.Add(datesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		mvsizer.Add(dasizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		mvsizer.Add(dirsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		mvsizer.Add(showsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
        
		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)
		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		self.Bind(wx.EVT_RADIOBUTTON, self.onDate, id=self.daterb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onArc, id=self.arcrb.GetId())
		self.Bind(wx.EVT_BUTTON, self.onShowBtn, id=ID_SHOWBTN)

		self.enableDate(True)
		self.enableArc(False)
#		self.enablePosNeg(False)

		self.da.SetFocus()


	def onDate(self, event):
		val = self.daterb.GetValue()
		self.enableDate(val)
		self.enableArc(not val)
#		self.enablePosNeg(not val)


	def enableDate(self, val):
		self.yeartxt.Enable(val)
		self.year.Enable(val)
		self.month.Enable(val)
		self.monthtxt.Enable(val)
		self.day.Enable(val)
		self.daytxt.Enable(val)

		self.hourtxt.Enable(val)
		self.hour.Enable(val)
		self.minutetxt.Enable(val)
		self.minute.Enable(val)
		self.secondtxt.Enable(val)
		self.second.Enable(val)


	def onArc(self, event):
		val = self.arcrb.GetValue()
		self.enableArc(val)
#		self.enablePosNeg(val)
		self.enableDate(not val)


	def enableArc(self, val):
		self.datxt.Enable(val)
		self.da.Enable(val)


#	def enablePosNeg(self, val):
#		self.positiverb.Enable(val)
#		self.negativerb.Enable(val)


	def onShowBtn(self, event):
		if (self.Validate() and self.sdate.Validate()):
			if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
				arc = 0.0
				date = 2000.5				

				direct = self.positiverb.GetValue()
				if (self.arcrb.GetValue()):
					arc = float(self.da.GetValue())
					jd, age = self.calcTime(arc, direct)
					y, m, d, h = astrology.swe_revjul(jd, 1)
					ho, mi, se = util.decToDeg(h)
					self.year.SetValue(str(y))
					self.month.SetValue(str(m))
					self.day.SetValue(str(d))

					self.hour.SetValue(str(ho))
					self.minute.SetValue(str(mi))
					self.second.SetValue(str(se))
				else:
					y = int(self.year.GetValue())
					m = int(self.month.GetValue())
					d = int(self.day.GetValue())
					ho = int(self.hour.GetValue())
					mi = int(self.minute.GetValue())
					se = int(self.second.GetValue())
					t = float(ho)+float(mi)/60.0+float(se)/3600.0
					calflag = astrology.SE_GREG_CAL
					if self.chart.time.cal == chart.Time.JULIAN:
						calflag = astrology.SE_JUL_CAL
					jd = astrology.swe_julday(y, m, d, t, calflag)
					if self.chart.time.jd >= jd:
						dlgm = wx.MessageDialog(None, mtexts.txts['TimeSmallerThanBirthTime'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
						dlgm.ShowModal()		
						dlgm.Destroy()
						return False

					arc = self.calcArc(jd, direct)
					self.da.SetValue(str(arc))

				da = arc
				if not direct:
					da *= -1

				pdinch = pdsinchart.PDsInChart(self.chart, da) #self.yz, mz, dz, tz ==> chart
				pdh, pdm, pds = util.decToDeg(pdinch.tz)
				cal = chart.Time.GREGORIAN
				if self.chart.time.cal == chart.Time.JULIAN:
					cal = chart.Time.JULIAN
				tim = chart.Time(pdinch.yz, pdinch.mz, pdinch.dz, pdh, pdm, pds, self.chart.time.bc, cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)

				if not self.terrestrial:
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
				txtdir = mtexts.txts['D']
				if not direct:
					txtdir = mtexts.txts['C']

				self.parent.change(pdchart, y, m, d, ho, mi, se, mtexts.typeListDirs[self.options.primarydir], keytxt, txtdir, math.fabs(da))
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['InvalidDate']+' ('+self.year.GetValue()+'.'+self.month.GetValue()+'.'+self.day.GetValue()+'.)', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()		
				dlgm.Destroy()


	def calcTime(self, arc, direct):
		'''Calculates time from arc according to the selected key (dynamic or static)'''

		ti = 0.0

		if self.options.pdkeydyn:
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLAREQUATORIALARC or self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				if not direct and self.options.useregressive:
					ti = self.calcTrueSolarArcRegressive(arc)
				else:
					ti = self.calcTrueSolarArc(arc)
			else:
				ti = self.calcBirthSolarArc(arc)
		else:
			if self.options.pdkeys == primdirs.PrimDirs.CUSTOMER:
				val = (self.options.pdkeydeg+self.options.pdkeymin/60.0+self.options.pdkeysec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
					ti = arc*coeff
			else:
				ti = arc*primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.COEFF]

		return self.chart.time.jd+ti*365.2421904, ti


	def calcTrueSolarArc(self, arc):
		LIM = 120.0 #arbitrary value
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		h, mi, s = util.decToDeg(self.chart.time.time)
		tt = 0.0

		#Add arc to Suns's pos (long or ra)
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		prSunPosEnd = prSunPos+arc
		transition = False #Pisces-Aries
		if prSunPosEnd >= 360.0:
			transition = True

#		Find day in ephemeris
		while (prSunPos <= prSunPosEnd):
			y, m, d = util.incrDay(y, m, d)
			ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			sun = planets.Planet(ti.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
			
			pos = sun.dataEqu[planets.Planet.RAEQU]
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				pos = sun.data[planets.Planet.LONG]

			if transition and pos < LIM:
				pos += 360.0
			prSunPos = pos

		if (prSunPos != prSunPosEnd):
			y, m, d = util.decrDay(y, m, d)

			if transition:
				prSunPosEnd -= 360.0

			trlon = 0.0
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				trlon = prSunPosEnd
			else:
				#to Longitude...
				trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])

			trans = transits.Transits()
			trans.day(y, m, d, self.chart, astrology.SE_SUN, trlon)

			if len(trans.transits) > 0:
				tt = trans.transits[0].time
		else:
			#the time is midnight
			tt = 0.0

		#difference
		d1 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s) #in GMT
		th, tm, ts = util.decToDeg(tt)
		d2 = datetime.datetime(y, m, d, th, tm, ts) #in GMT
		diff = d2-d1
		ddays = diff.days
		dtime = diff.seconds/3600.0
		#dtime to days
		dtimeindays = dtime/24.0

		tt = ddays+dtimeindays

		return tt


	def calcTrueSolarArcRegressive(self, arc):
		LIM = 120.0 #arbitrary value
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		h, mi, s = util.decToDeg(self.chart.time.time)
		tt = 0.0

		#Subtract arc from Suns's pos (long or ra)
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		prSunPosEnd = prSunPos-arc
		transition = False #Pisces-Aries
		if prSunPosEnd < 0.0:
			prSunPos += 360.0
			prSunPosEnd += 360.0
			transition = True

#		Find day in ephemeris
		while (prSunPos >= prSunPosEnd):
			y, m, d = util.decrDay(y, m, d)
			ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			sun = planets.Planet(ti.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
			
			pos = sun.dataEqu[planets.Planet.RAEQU]
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				pos = sun.data[planets.Planet.LONG]
			if transition and pos < LIM:
				pos += 360.0
			prSunPos = pos

		if (prSunPos != prSunPosEnd):
			if transition:
				prSunPosEnd -= 360.0

			trlon = 0.0
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				trlon = prSunPosEnd
			else:
				#to Longitude...
				trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])

			trans = transits.Transits()
			trans.day(y, m, d, self.chart, astrology.SE_SUN, trlon)

			if len(trans.transits) > 0:
				tt = trans.transits[0].time
		else:
			#the time is midnight
			tt = 0.0

		#difference
		th, tm, ts = util.decToDeg(tt)
		d1 = datetime.datetime(y, m, d, th, tm, ts) #in GMT
		d2 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s) #in GMT
		diff = d2-d1
		ddays = diff.days
		dtime = diff.seconds/3600.0
		#dtime to days
		dtimeindays = dtime/24.0

		tt = ddays+dtimeindays

		return tt


	def calcBirthSolarArc(self, arc):
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		yn, mn, dn = util.incrDay(y, m, d)

		ti1 = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
		ti2 = chart.Time(yn, mn, dn, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)

		sun1 = planets.Planet(ti1.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
		sun2 = planets.Planet(ti2.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)

		diff = 0.0
		if self.options.pdkeyd == primdirs.PrimDirs.BIRTHDAYSOLAREQUATORIALARC:
			diff = sun2.dataEqu[planets.Planet.RAEQU]-sun1.dataEqu[planets.Planet.RAEQU]
		elif self.options.pdkeyd == primdirs.PrimDirs.BIRTHDAYSOLARECLIPTICALARC:
			diff = sun2.data[planets.Planet.LONG]-sun1.data[planets.Planet.LONG]

		coeff = 0.0
		if diff != 0.0:
			coeff = 1.0/diff

		return arc*coeff


	def calcArc(self, jd, direct):
		'''Calculates Arc from DateTime according to the selected key (dynamic or static)'''

		arc = 0.0
		ti = math.fabs(self.chart.time.jd-jd)/365.2421904

		if self.options.pdkeydyn:
			if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLAREQUATORIALARC or self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
				if not direct and self.options.useregressive:
					arc = self.calcTrueSolarArcRegressiveRev(ti)
				else:
					arc = self.calcTrueSolarArcRev(ti)
			else:
				arc = self.calcBirthSolarArcRev(ti)
		else:
			if self.options.pdkeys == primdirs.PrimDirs.CUSTOMER:
				val = (self.options.pdkeydeg+self.options.pdkeymin/60.0+self.options.pdkeysec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
					if coeff != 0.0:
						arc = ti/coeff
			else:
				if primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.COEFF] != 0.0:
					arc = ti/primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.COEFF]

		direct = True
		if arc < 0.0:
			arc *= -1
			direct = False
		if arc > 180.0:
			arc = 360.0-arc 
			direct = not direct

		return arc


	def calcTrueSolarArcRev(self, ti):
		#Sun's natal position
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		#Calculate new JD from ti
		jdArc = self.chart.time.jd+ti#*365.2421904
		sun = planets.Planet(jdArc, astrology.SE_SUN, astrology.SEFLG_SWIEPH)

		#The difference in RA or Long will be the arc
		prSunPosEnd = sun.dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPosEnd = sun.data[planets.Planet.LONG]

		#The arc
		return prSunPosEnd-prSunPos


	def calcTrueSolarArcRegressiveRev(self, ti):
		#Sun's natal position
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		#Calculate new JD from ti
		jdArc = self.chart.time.jd-ti#*365.2421904
		sun = planets.Planet(jdArc, astrology.SE_SUN, astrology.SEFLG_SWIEPH)

		#The difference in RA or Long will be the arc
		prSunPosEnd = sun.dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == primdirs.PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPosEnd = sun.data[planets.Planet.LONG]

		#The arc
		return math.fabs(prSunPosEnd-prSunPos)


	def calcBirthSolarArcRev(self, ti):
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		yn, mn, dn = util.incrDay(y, m, d)

		ti1 = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
		ti2 = chart.Time(yn, mn, dn, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)

		sun1 = planets.Planet(ti1.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
		sun2 = planets.Planet(ti2.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)

		diff = 0.0
		if self.options.pdkeyd == primdirs.PrimDirs.BIRTHDAYSOLAREQUATORIALARC:
			diff = sun2.dataEqu[planets.Planet.RAEQU]-sun1.dataEqu[planets.Planet.RAEQU]
		elif self.options.pdkeyd == primdirs.PrimDirs.BIRTHDAYSOLARECLIPTICALARC:
			diff = sun2.data[planets.Planet.LONG]-sun1.data[planets.Planet.LONG]

		coeff = 1.0
		if diff != 0.0:
			coeff = 1.0/diff

		return ti/coeff






