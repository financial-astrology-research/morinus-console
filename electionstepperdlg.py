import wx
import mtexts
import chart
import util


class ElectionStepperDlg(wx.Dialog):
	def __init__(self, parent, chrt, options, caption):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Elections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)

		self.parent = parent
		self.chart = chrt
		self.options = options
		self.caption = caption

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		ID_IncrYear = wx.NewId()
		ID_DecrYear = wx.NewId()
		ID_IncrMonth = wx.NewId()
		ID_DecrMonth = wx.NewId()
		ID_IncrDay = wx.NewId()
		ID_DecrDay = wx.NewId()
		ID_IncrHour = wx.NewId()
		ID_DecrHour = wx.NewId()
		ID_IncrMin = wx.NewId()
		ID_DecrMin = wx.NewId()
		ID_IncrSec = wx.NewId()
		ID_DecrSec = wx.NewId()
		sb = wx.StaticBox(self, label='')
		sbsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

		gsizer = wx.FlexGridSizer(6, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Year'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrYear = wx.Button(self, ID_IncrYear, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrYear, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrYear = wx.Button(self, ID_DecrYear, '--', size=(40,30))
		hsizer.Add(btnDecrYear, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Month'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrMonth = wx.Button(self, ID_IncrMonth, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrMonth, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrMonth = wx.Button(self, ID_DecrMonth, '--', size=(40,30))
		hsizer.Add(btnDecrMonth, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Day'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrDay = wx.Button(self, ID_IncrDay, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrDay, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrDay = wx.Button(self, ID_DecrDay, '--', size=(40,30))
		hsizer.Add(btnDecrDay, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Hour'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrHour = wx.Button(self, ID_IncrHour, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrHour, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrHour = wx.Button(self, ID_DecrHour, '--', size=(40,30))
		hsizer.Add(btnDecrHour, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Min'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrMin = wx.Button(self, ID_IncrMin, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrMin, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrMin = wx.Button(self, ID_DecrMin, '--', size=(40,30))
		hsizer.Add(btnDecrMin, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Sec'])
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		btnIncrSec = wx.Button(self, ID_IncrSec, '++', size=(40,30))
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(btnIncrSec, 0, wx.ALIGN_CENTER|wx.ALL, 2)
		btnDecrSec = wx.Button(self, ID_DecrSec, '--', size=(40,30))
		hsizer.Add(btnDecrSec, 0, wx.ALIGN_CENTER|wx.ALL, 2)
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
		self.Bind(wx.EVT_BUTTON, self.onIncrDay, id=ID_IncrDay)
		self.Bind(wx.EVT_BUTTON, self.onDecrDay, id=ID_DecrDay)
		self.Bind(wx.EVT_BUTTON, self.onIncrHour, id=ID_IncrHour)
		self.Bind(wx.EVT_BUTTON, self.onDecrHour, id=ID_DecrHour)
		self.Bind(wx.EVT_BUTTON, self.onIncrMin, id=ID_IncrMin)
		self.Bind(wx.EVT_BUTTON, self.onDecrMin, id=ID_DecrMin)
		self.Bind(wx.EVT_BUTTON, self.onIncrSec, id=ID_IncrSec)
		self.Bind(wx.EVT_BUTTON, self.onDecrSec, id=ID_DecrSec)
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)


	def onIncrYear(self, event):
		y = self.chart.time.origyear+1
		self.show(y, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecrYear(self, event):
		y = self.chart.time.origyear-1
		self.show(y, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncrMonth(self, event):
		y, m = util.incrMonth(self.chart.time.origyear, self.chart.time.origmonth)
		self.show(y, m, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecrMonth(self, event):
		y, m = util.decrMonth(self.chart.time.origyear, self.chart.time.origmonth)
		self.show(y, m, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncrDay(self, event):
		y, m, d = util.incrDay(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday)
		self.show(y, m, d, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecrDay(self, event):
		y, m, d = util.decrDay(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday)
		self.show(y, m, d, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncrHour(self, event):
		y, m, d, h = util.addHour(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour)
		self.show(y, m, d, h, self.chart.time.minute, self.chart.time.second)


	def onDecrHour(self, event):
		y, m, d, h = util.subtractHour(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour)
		self.show(y, m, d, h, self.chart.time.minute, self.chart.time.second)


	def onIncrMin(self, event):
		y, m, d, h, mi = util.addMins(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, 1)
		self.show(y, m, d, h, mi, self.chart.time.second)


	def onDecrMin(self, event):
		y, m, d, h, mi = util.subtractMins(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, 1)
		self.show(y, m, d, h, mi, self.chart.time.second)


	def onIncrSec(self, event):
		y, m, d, h, mi, s = util.addSecs(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second, 1)
		self.show(y, m, d, h, mi, s)


	def onDecrSec(self, event):
		y, m, d, h, mi, s = util.subtractSecs(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second, 1)
		self.show(y, m, d, h, mi, s)


	def show(self, y, m, d, h, mi, s):
		time = chart.Time(y, m, d, h, mi, s, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.daylightsaving, self.chart.place, False)
		chrt = chart.Chart(self.chart.name, self.chart.male, time, self.chart.place, chart.Chart.TRANSIT, '', self.options, False)
		self.parent.change(chrt, self.caption)
		del self.chart
		self.chart = chrt


	def onClose(self, event):
		self.Close()






