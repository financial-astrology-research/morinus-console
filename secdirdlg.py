import  wx
import intvalidator
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class SecondaryDirsDlg(wx.Dialog):
	def __init__(self, parent):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['SecondaryDirs'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Age
		sage =wx.StaticBox(self, label=mtexts.txts['Age'])
		agesizer = wx.StaticBoxSizer(sage, wx.VERTICAL)
		self.age = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 100), size=(40,-1))
		agesizer.Add(self.age, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.age.SetMaxLength(2)

		mhsizer.Add(agesizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 0)

		#Direction
		sdir =wx.StaticBox(self, label='')
		dirsizer = wx.StaticBoxSizer(sdir, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.directrb = wx.RadioButton(self, -1, mtexts.txts['Direct'], style=wx.RB_GROUP)
		vsizer.Add(self.directrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.converserb = wx.RadioButton(self, -1, mtexts.txts['Converse'])
		vsizer.Add(self.converserb, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		dirsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mhsizer.Add(dirsizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 5)
		mvsizer.Add(mhsizer, 1, wx.GROW|wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 5)

		#Time
		stime =wx.StaticBox(self, label='')
		timesizer = wx.StaticBoxSizer(stime, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.solartimerb = wx.RadioButton(self, -1, mtexts.txts['ApparentSolarTime'], style=wx.RB_GROUP)
		vsizer.Add(self.solartimerb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.meantimerb = wx.RadioButton(self, -1, mtexts.txts['MeanTime'])
		vsizer.Add(self.meantimerb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		timesizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(timesizer, 0, wx.GROW|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		btnsizer = wx.StdDialogButtonSizer()

		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
        
		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnsizer.AddButton(btnOk)
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btn.SetHelpText(mtexts.txts['HelpCancel'])

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()


	def onOK(self, event):
		if (self.Validate()):
			self.Close()
			self.SetReturnCode(wx.ID_OK)


	def initialize(self):
		self.age.SetValue(str(0))
		self.age.SetFocus()







