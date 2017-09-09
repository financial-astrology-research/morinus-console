import wx
import chart
import intvalidator
import rangechecker
import mtexts
import util


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class ProfDlg(wx.Dialog):

	def __init__(self, parent, radixjd, radixplace):

		self.radixjd = radixjd
		self.radixplace = radixplace

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['Profections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

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
		vsizer = wx.BoxSizer(wx.VERTICAL)
#		self.dateckb = wx.CheckBox(self, -1, mtexts.txts['BC'])
#		vsizer.Add(self.dateckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5)

		fgsizer = wx.FlexGridSizer(1, 3)
		self.yeartxt = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vsizer.Add(self.yeartxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.monthtxt = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vsizer.Add(self.monthtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)
		vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.daytxt = wx.StaticText(self, -1, mtexts.txts['Day']+':')
		vsizer.Add(self.daytxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.day.SetHelpText(mtexts.txts['HelpDay'])
		self.day.SetMaxLength(2)
		vsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		datesizer.Add(fgsizer, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5)###

		#time
		self.stime = wx.StaticBox(self, label='')
		timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(1, 3)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.hourtxt = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vsizer.Add(self.hourtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,-1))
		self.hour.SetHelpText(mtexts.txts['HelpHour'])
		vsizer.Add(self.hour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour.SetMaxLength(2)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.minutetxt = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vsizer.Add(self.minutetxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.minute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.minute.SetHelpText(mtexts.txts['HelpMin'])
		self.minute.SetMaxLength(2)
		vsizer.Add(self.minute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.secondtxt = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vsizer.Add(self.secondtxt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.second = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.second.SetHelpText(mtexts.txts['HelpMin'])
		self.second.SetMaxLength(2)
		vsizer.Add(self.second, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		timesizer.Add(fgsizer, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5)###

		mvsizer.Add(datesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		mvsizer.Add(timesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
        
		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btn.SetHelpText(mtexts.txts['HelpCancel'])
		btnsizer.AddButton(btn)

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		self.year.SetFocus()


	def onOK(self, event):
		if (self.Validate() and self.sdate.Validate()):
			if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
				y = int(self.year.GetValue())
				m = int(self.month.GetValue())
				d = int(self.day.GetValue())
				h = int(self.hour.GetValue())
				mi = int(self.minute.GetValue())
				s = int(self.second.GetValue())
				tim = chart.Time(y, m, d, h, mi, s, False, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, self.radixplace, False)

				if self.radixjd >= tim.jd:
					dlgm = wx.MessageDialog(None, mtexts.txts['TimeSmallerThanBirthTime'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
					dlgm.ShowModal()		
					dlgm.Destroy()
					return False

				self.Close()
				self.SetReturnCode(wx.ID_OK)
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['InvalidDate']+' ('+self.year.GetValue()+'.'+self.month.GetValue()+'.'+self.day.GetValue()+'.)', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()		
				dlgm.Destroy()


	def initialize(self, y, m, d, h, mi, s):
		self.year.SetValue(str(y))
		self.month.SetValue(str(m))
		self.day.SetValue(str(d))

		self.hour.SetValue(str(h))
		self.minute.SetValue(str(mi))
		self.second.SetValue(str(s))




