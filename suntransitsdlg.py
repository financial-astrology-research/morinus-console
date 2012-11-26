import  wx
import intvalidator
import util
import rangechecker
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class SunTransitsDlg(wx.Dialog):
	def __init__(self, parent):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['SunTransits'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Target
		self.starget =wx.StaticBox(self, label='')
		targetsizer = wx.StaticBoxSizer(self.starget, wx.VERTICAL)
		self.ascrb = wx.RadioButton(self, -1, mtexts.txts['Ascendant'], style=wx.RB_GROUP)
		targetsizer.Add(self.ascrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.mcrb = wx.RadioButton(self, -1, mtexts.txts['MediumCoeli'])
		targetsizer.Add(self.mcrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.sunrb = wx.RadioButton(self, -1, mtexts.txts['Sun'])
		targetsizer.Add(self.sunrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.moonrb = wx.RadioButton(self, -1, mtexts.txts['Moon'])
		targetsizer.Add(self.moonrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.mercuryrb = wx.RadioButton(self, -1, mtexts.txts['Mercury'])
		targetsizer.Add(self.mercuryrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.venusrb = wx.RadioButton(self, -1, mtexts.txts['Venus'])
		targetsizer.Add(self.venusrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.marsrb = wx.RadioButton(self, -1, mtexts.txts['Mars'])
		targetsizer.Add(self.marsrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.jupiterrb = wx.RadioButton(self, -1, mtexts.txts['Jupiter'])
		targetsizer.Add(self.jupiterrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.saturnrb = wx.RadioButton(self, -1, mtexts.txts['Saturn'])
		targetsizer.Add(self.saturnrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.uranusrb = wx.RadioButton(self, -1, mtexts.txts['Uranus'])
		targetsizer.Add(self.uranusrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.neptunerb = wx.RadioButton(self, -1, mtexts.txts['Neptune'])
		targetsizer.Add(self.neptunerb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.plutorb = wx.RadioButton(self, -1, mtexts.txts['Pluto'])
		targetsizer.Add(self.plutorb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(targetsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 0)

		#Time
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000
		self.stime =wx.StaticBox(self, label='')
		timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['StartingDate'])
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		vsubsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer = wx.FlexGridSizer(2, 3)
		label = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)
		vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Day']+':')
		vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.day.SetHelpText(mtexts.txts['HelpDay'])
		self.day.SetMaxLength(2)
		vsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsubsizer.Add(fgsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
		timesizer.Add(vsubsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		mhsizer.Add(timesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 5)
		mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
        
		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnsizer.AddButton(btnOk)
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btn.SetHelpText(mtexts.txts['HelpCancel'])

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()


	def onOK(self, event):
		if (self.Validate() and self.stime.Validate()):

			if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
				self.Close()
				self.SetReturnCode(wx.ID_OK)
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['InvalidDate']+' ('+self.year.GetValue()+'.'+self.month.GetValue()+'.'+self.day.GetValue()+'.)', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()		
				dlgm.Destroy()


	def initialize(self, chrt):
		year = chrt.time.year
		month = chrt.time.month
		day = chrt.time.day

		year, month, day = util.incrDay(year, month, day)

		self.ascrb.SetFocus()
		self.year.SetValue(str(year))
		self.month.SetValue(str(month))
		self.day.SetValue(str(day))







