import wx
import mtexts
import chart
import profections
import munprofections
import util


class ProfectionStepperDlg(wx.Dialog):
	def __init__(self, parent, chrt, y, m, d, t, options, caption):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Profections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)

		self.parent = parent
		self.chart = chrt
		self.y = y
		self.m = m
		self.d = d
		self.t = t
		self.cnt = 0 #added because of a Bug in the zodiacalProfs: longitude fluctuates, use AUX_DATES instead
		self.options = options
		self.caption = caption
		self.zodprofs = options.zodprof
		self.usezodprojs = options.usezodprojsprof

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		ID_IncrYear = wx.NewId()
		ID_DecrYear = wx.NewId()
		ID_IncrMonth = wx.NewId()
		ID_DecrMonth = wx.NewId()
		ID_IncrDay = wx.NewId()
		ID_DecrDay = wx.NewId()
		sb = wx.StaticBox(self, label='')
		sbsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

		if self.zodprofs or self.usezodprojs:
			gsizer = wx.FlexGridSizer(3, 2)
		else:
			gsizer = wx.FlexGridSizer(2, 2)

		self.yeartxt = wx.TextCtrl(self, -1, '', size=(50,-1), style=wx.TE_READONLY)
		self.yeartxt.SetValue(str(self.y))
		gsizer.Add(self.yeartxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrYear = wx.Button(self, ID_IncrYear, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrYear, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrYear = wx.Button(self, ID_DecrYear, '--', size=(40,30))
		hsizer.Add(btnDecrYear, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.monthtxt = wx.TextCtrl(self, -1, '', size=(50,-1), style=wx.TE_READONLY)
		self.monthtxt.SetValue(str(self.m))
		gsizer.Add(self.monthtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrMonth = wx.Button(self, ID_IncrMonth, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrMonth, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrMonth = wx.Button(self, ID_DecrMonth, '--', size=(40,30))
		hsizer.Add(btnDecrMonth, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		if self.zodprofs or self.usezodprojs:
			self.daytxt = wx.TextCtrl(self, -1, '', size=(50,-1), style=wx.TE_READONLY)
			self.daytxt.SetValue(str(self.d))
			gsizer.Add(self.daytxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
			btnIncrDay = wx.Button(self, ID_IncrDay, '++', size=(40,30))
			hsizer = wx.BoxSizer(wx.HORIZONTAL)
			hsizer.Add(btnIncrDay, 0, wx.ALIGN_CENTER|wx.ALL, 2)
			btnDecrDay = wx.Button(self, ID_DecrDay, '--', size=(40,30))
			hsizer.Add(btnDecrDay, 0, wx.ALIGN_CENTER|wx.ALL, 2)
			gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		sbsizer.Add(gsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
    
		mvsizer.Add(sbsizer, 0, wx.ALIGN_CENTER)

		btnsizer = wx.StdDialogButtonSizer()

		btn = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnsizer.AddButton(btn)
		btn.SetDefault()

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btn.SetFocus()

		self.Bind(wx.EVT_BUTTON, self.onIncrYear, id=ID_IncrYear)
		self.Bind(wx.EVT_BUTTON, self.onDecrYear, id=ID_DecrYear)
		self.Bind(wx.EVT_BUTTON, self.onIncrMonth, id=ID_IncrMonth)
		self.Bind(wx.EVT_BUTTON, self.onDecrMonth, id=ID_DecrMonth)
		if self.zodprofs or self.usezodprojs:
			self.Bind(wx.EVT_BUTTON, self.onIncrDay, id=ID_IncrDay)
			self.Bind(wx.EVT_BUTTON, self.onDecrDay, id=ID_DecrDay)
			self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)


	def onIncrYear(self, event):
		self.cnt += 1
		self.show(self.y, self.m, self.d, self.t, self.cnt)

	def onDecrYear(self, event):
		h, mi, s = util.decToDeg(self.t)
		tim = chart.Time(self.y+self.cnt-1, self.m, self.d, h, mi, s, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.daylightsaving, self.chart.place, False)
		if tim.jd > self.chart.time.jd:
			self.cnt -= 1
			self.show(self.y, self.m, self.d, self.t, self.cnt)


	def onIncrMonth(self, event):
		y, self.m = util.incrMonth(self.y+self.cnt, self.m)
		if y != self.y+self.cnt:
			self.cnt +=1
		
		self.show(self.y, self.m, self.d, self.t, self.cnt)


	def onDecrMonth(self, event):
		h, mi, s = util.decToDeg(self.t)
		yt, mt = util.decrMonth(self.y+self.cnt, self.m)
		tim = chart.Time(yt, mt, self.d, h, mi, s, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.daylightsaving, self.chart.place, False)
		if tim.jd > self.chart.time.jd:
			y, self.m = util.decrMonth(self.y+self.cnt, self.m)

			if y != self.y+self.cnt:
				self.cnt -=1
			self.show(self.y, self.m, self.d, self.t, self.cnt)


	def onIncrDay(self, event):
		y, self.m, self.d = util.incrDay(self.y+self.cnt, self.m, self.d)
		if y != self.y+self.cnt:
			self.cnt +=1
		self.show(self.y, self.m, self.d, self.t, self.cnt)


	def onDecrDay(self, event):
		h, mi, s = util.decToDeg(self.t)
		yt, mt, dt = util.decrDay(self.y+self.cnt, self.m, self.d)
		tim = chart.Time(yt, mt, dt, h, mi, s, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.daylightsaving, self.chart.place, False)
		if tim.jd > self.chart.time.jd:
			y, self.m, self.d = util.decrDay(self.y+self.cnt, self.m, self.d)
			if y != self.y+self.cnt:
				self.cnt -=1
			self.show(self.y, self.m, self.d, self.t, self.cnt)


	def show(self, y, m, d, t, cnt):
		proftype = chart.Chart.YEAR
		if self.zodprofs:
			prof = profections.Profections(self.chart, y, m, d, t, cnt)
			pchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PROFECTION, '', self.options, False, proftype)
			pchart.calcProfPos(prof)
		else:
			if not self.usezodprojs and (y+cnt == self.chart.time.year or (y+cnt-self.chart.time.year) % 12 == 0) and m == self.chart.time.month and d == self.chart.time.day:
				pchart = self.chart
			else:
				prof = munprofections.MunProfections(self.chart, y, m, d, t, cnt)
				proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
				profplace = chart.Place(mtexts.txts['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.chart.place.deglat, self.chart.place.minlat, self.chart.place.seclat, self.chart.place.north, self.chart.place.altitude)
				pchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, profplace, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
				pchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
				#modify planets, ...
				pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])

				#modify lof
				pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.chart.place.lat, self.chart.obl[0])

				#recalc AspMatrix
				pchart.calcAspMatrix()

		self.parent.change(pchart, self.caption, y+cnt, m, d, t)
		self.yeartxt.SetValue(str(y+cnt))
		self.monthtxt.SetValue(str(m))
		if self.zodprofs or self.usezodprojs:
			self.daytxt.SetValue(str(d))


	def onClose(self, event):
		self.Close()






