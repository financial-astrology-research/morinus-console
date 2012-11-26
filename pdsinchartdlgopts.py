import wx
import chart
import mtexts
import util


class PDsInChartsDlgOpts(wx.Dialog):

	FROMMUNDANEPOS = 0
	FROMZODIACALPOS = 1
	PSEUDOASTRONOMICAL = 2

	def __init__(self, parent):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
#		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PDsInChart'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Zodiacal/Mundane Selection
		sselection =wx.StaticBox(self, label='')
		selectionsizer = wx.StaticBoxSizer(sselection, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.mundanerb = wx.RadioButton(self, -1, mtexts.txts['FromMundanePos'], style=wx.RB_GROUP)
		vsizer.Add(self.mundanerb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.zodiacalrb = wx.RadioButton(self, -1, mtexts.txts['FromZodiacalPos'])
		vsizer.Add(self.zodiacalrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.fullrb = wx.RadioButton(self, -1, mtexts.txts['PseudoAstronomical'])
		vsizer.Add(self.fullrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		vfullsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.secondaryckb = wx.CheckBox(self, -1, mtexts.txts['SecondaryMotion'])
		vfullsubsizer.Add(self.secondaryckb, 0, wx.ALL, 2)
		vsizer.Add(vfullsubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 12)

		selectionsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(selectionsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		self.Bind(wx.EVT_RADIOBUTTON, self.onMundane, id=self.mundanerb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onZodiacal, id=self.zodiacalrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onFull, id=self.fullrb.GetId())

		btnsizer = wx.StdDialogButtonSizer()

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


	def onMundane(self, event):
		self.secondaryckb.Enable(self.fullrb.GetValue())


	def onZodiacal(self, event):
		self.secondaryckb.Enable(self.fullrb.GetValue())


	def onFull(self, event):
		self.secondaryckb.Enable(self.fullrb.GetValue())


	def fill(self, opts):
		if opts.pdincharttyp == PDsInChartsDlgOpts.FROMMUNDANEPOS:
			self.mundanerb.SetValue(True)
		elif opts.pdincharttyp == PDsInChartsDlgOpts.FROMZODIACALPOS:
			self.zodiacalrb.SetValue(True)
		elif opts.pdincharttyp == PDsInChartsDlgOpts.PSEUDOASTRONOMICAL:
			self.fullrb.SetValue(True)
		
		self.secondaryckb.SetValue(opts.pdinchartsecmotion)
		self.secondaryckb.Enable(self.fullrb.GetValue())


	def check(self, opts):
		changed = False

		if opts.pdincharttyp != PDsInChartsDlgOpts.FROMMUNDANEPOS and self.mundanerb.GetValue():
			opts.pdincharttyp = PDsInChartsDlgOpts.FROMMUNDANEPOS
			changed = True
		if opts.pdincharttyp != PDsInChartsDlgOpts.FROMZODIACALPOS and self.zodiacalrb.GetValue():
			opts.pdincharttyp = PDsInChartsDlgOpts.FROMZODIACALPOS
			changed = True
		if opts.pdincharttyp != PDsInChartsDlgOpts.PSEUDOASTRONOMICAL and self.fullrb.GetValue():
			opts.pdincharttyp = PDsInChartsDlgOpts.PSEUDOASTRONOMICAL
			changed = True

		if opts.pdinchartsecmotion != self.secondaryckb.GetValue():
			opts.pdinchartsecmotion = self.secondaryckb.GetValue()
			changed = True

		return changed



