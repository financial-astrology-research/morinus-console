import wx
import mtexts
import secdir
import chart


class StepperDlg(wx.Dialog):
	def __init__(self, parent, chrt, age, direct, soltime, options, caption):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['SecondaryDirs'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)

		self.parent = parent
		self.chart = chrt
		self.age = age
		if not direct:
			self.age *= -1
#		self.direct = direct
		self.soltime = soltime
		self.options = options
		self.caption = caption

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		ID_Incr = wx.NewId()
		ID_Decr = wx.NewId()
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		sdays =wx.StaticBox(self, label=mtexts.txts['Days'])
		dayssizer = wx.StaticBoxSizer(sdays, wx.HORIZONTAL)
		self.daytxt = wx.TextCtrl(self, -1, '', size=(50,-1), style=wx.TE_READONLY)
		self.daytxt.SetValue(str(self.age))
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(self.daytxt, 0, wx.ALIGN_CENTER)
		btnIncr = wx.Button(self, ID_Incr, '++', size=(60,40))
		hsizer.Add(btnIncr, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		btnDecr = wx.Button(self, ID_Decr, '--', size=(60,40))
		hsizer.Add(btnDecr, 0, wx.ALIGN_CENTER|wx.ALL, 5)
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

		self.Bind(wx.EVT_BUTTON, self.onIncr, id=ID_Incr)
		self.Bind(wx.EVT_BUTTON, self.onDecr, id=ID_Decr)
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)

		self.zt = chart.Time.LOCALMEAN
		if self.soltime:
			self.zt = chart.Time.LOCALAPPARENT
		self.zh = 0
		self.zm = 0


	def onIncr(self, event):
		self.age += 1
		self.daytxt.SetValue(str(self.age))
		direct = True
		age = self.age
		if self.age < 0:
			age *= -1
			direct = False
		sdir = secdir.SecDir(self.chart, age, direct, self.soltime)
		y, m, d, hour, minute, second = sdir.compute()

		time = chart.Time(y, m, d, hour, minute, second, False, self.chart.time.cal, self.zt, self.chart.time.plus, self.zh, self.zm, False, self.chart.place, False)
		chrt = chart.Chart(self.chart.name, self.chart.male, time, self.chart.place, chart.Chart.TRANSIT, '', self.options, False)
		self.parent.change(chrt, self.caption)


	def onDecr(self, event):
		self.age -= 1
		self.daytxt.SetValue(str(self.age))
		direct = True
		age = self.age
		if self.age < 0:
			age *= -1
			direct = False
		sdir = secdir.SecDir(self.chart, age, direct, self.soltime)
		y, m, d, hour, minute, second = sdir.compute()

		time = chart.Time(y, m, d, hour, minute, second, False, self.chart.time.cal, self.zt, self.chart.time.plus, self.zh, self.zm, False, self.chart.place, False)
		chrt = chart.Chart(self.chart.name, self.chart.male, time, self.chart.place, chart.Chart.TRANSIT, '', self.options, False)
		self.parent.change(chrt, self.caption)


	def onClose(self, event):
		self.Close()






