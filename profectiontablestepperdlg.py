import wx
import chart
import profections
import munprofections
import mtexts
import util


class ProfectionTableStepperDlg(wx.Dialog):
	def __init__(self, parent, chrt, opts, proftype):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Profections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)

		self.parent = parent
		self.chart = chrt
		self.options = opts
		self.zodiacalprofs = opts.zodprof
		self.usezodprojs = opts.usezodprojsprof
		self.proftype = proftype
		self.age = 0

		#Feb29?
		self.feb29 = self.chart.time.month == 2 and self.chart.time.day == 29

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		ID_Incr = wx.NewId()
		ID_Decr = wx.NewId()
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		sdays =wx.StaticBox(self, label=mtexts.txts['Dozen'])
		dayssizer = wx.StaticBoxSizer(sdays, wx.HORIZONTAL)
		self.agetxt = wx.TextCtrl(self, -1, '', size=(50,-1), style=wx.TE_READONLY)
		self.agetxt.SetValue(str(self.age))
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(self.agetxt, 0, wx.ALIGN_CENTER)
		self.btnIncr = wx.Button(self, ID_Incr, '++', size=(60,40))
		hsizer.Add(self.btnIncr, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.btnDecr = wx.Button(self, ID_Decr, '--', size=(60,40))
		hsizer.Add(self.btnDecr, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		vsizer.Add(hsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		dayssizer.Add(vsizer, 0, wx.ALIGN_CENTER|wx.TOP, 5)
        
		mvsizer.Add(dayssizer, 0, wx.ALIGN_CENTER)

		btnsizer = wx.StdDialogButtonSizer()

		btn = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnsizer.AddButton(btn)
		btn.SetDefault()

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btn.SetFocus()

		self.Bind(wx.EVT_BUTTON, self.onIncrDozen, id=ID_Incr)
		self.Bind(wx.EVT_BUTTON, self.onDecrDozen, id=ID_Decr)
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)

		self.btnDecr.Enable(False)


	def onIncrDozen(self, event):
		if self.age+12 >= 100:
			return
		self.age += 12
		self.btnDecr.Enable(True)
		self.show(self.age)


	def onDecrDozen(self, event):
		self.age -= 12
		if self.age == 0:
			self.btnDecr.Enable(False)
		self.show(self.age)


	def show(self, age):
		wait = wx.BusyCursor()
		y = self.chart.time.year#+age
		m = self.chart.time.month
		d = self.chart.time.day
		t = self.chart.time.time

		if self.feb29:
			d -= 1

		self.agetxt.SetValue(str(age))

		pcharts = []

		cyc = 0
		while(cyc < 12):
			if self.zodiacalprofs:
				prof = profections.Profections(self.chart, y, m, d, t, age+cyc)
				pchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PROFECTION, '', self.options, False, self.proftype)
				pchart.calcProfPos(prof)
			else:
				if not self.usezodprojs and (y+age+cyc == self.chart.time.year or (y+age+cyc-self.chart.time.year) % 12 == 0) and m == self.chart.time.month and d == self.chart.time.day:
					pchart = self.chart
				else:
					prof = munprofections.MunProfections(self.chart, y+age+cyc, m, d, t)
					proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
					profplace = chart.Place(mtexts.txts['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.chart.place.deglat, self.chart.place.minlat, self.chart.place.seclat, self.chart.place.north, self.chart.place.altitude)
					pchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, profplace, chart.Chart.PROFECTION, '', self.options, False, self.proftype, self.options.usezodprojsprof)
					pchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PROFECTION, '', self.options, False, self.proftype, self.options.usezodprojsprof)
					#modify planets, ...
					pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])
	
					#modify lof
					pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
	
			pcharts.append((pchart, y+age+cyc, m, d, t))
			cyc += 1

		self.parent.change(age, pcharts, self.options)


	def onClose(self, event):
		self.Close()






