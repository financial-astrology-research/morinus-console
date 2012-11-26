import wx
import primdirs
import customerdlg
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class PrimDirsDlgSmall(wx.Dialog):
	def __init__(self, parent, options, ephepath):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PrimaryDirs'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		self.parent = parent
		self.options = options
		self.ephepath = ephepath

		self.cpdlons = options.pdcustomerlon[:]
		self.cpdlats = options.pdcustomerlat[:]
		self.southern = options.pdcustomersouthern

		self.cpd2lons = options.pdcustomer2lon[:]
		self.cpd2lats = options.pdcustomer2lat[:]
		self.southern2 = options.pdcustomer2southern

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Type
		stype = wx.StaticBox(self, label='')
		typesizer = wx.StaticBoxSizer(stype, wx.VERTICAL)
		self.placidiansemiarcrb = wx.RadioButton(self, -1, mtexts.txts['PlacidianSemiArc'], style=wx.RB_GROUP)
		typesizer.Add(self.placidiansemiarcrb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
		self.placidiansemiarcrb.SetHelpText(mtexts.txts['HelpPlacidianSemiArc'])
		self.placidianutprb = wx.RadioButton(self, -1, mtexts.txts['PlacidianUnderThePole'])
		typesizer.Add(self.placidianutprb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
		self.placidianutprb.SetHelpText(mtexts.txts['HelpPlacidianUnderThePole'])
		self.regiomontanrb = wx.RadioButton(self, -1, mtexts.txts['Regiomontan'])
		typesizer.Add(self.regiomontanrb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
		self.regiomontanrb.SetHelpText(mtexts.txts['HelpRegiomontan'])
		self.Bind(wx.EVT_RADIOBUTTON, self.onPlacidian, id=self.placidiansemiarcrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onPlacidianUTP, id=self.placidianutprb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onRegiomontan, id=self.regiomontanrb.GetId())

#		self.placidianutprb.Enable(False)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(typesizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.TOP, 5)

		#Subtype
		vzodsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['UseSZ']+':')
		vzodsizer.Add(label, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.szneitherrb = wx.RadioButton(self, -1, mtexts.txts['SZNeither'], style=wx.RB_GROUP)
		self.szneitherrb.SetHelpText(mtexts.txts['HelpSZNeither'])
		vzodsizer.Add(self.szneitherrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.szpromissorrb = wx.RadioButton(self, -1, mtexts.txts['SZPromissor'])
		self.szpromissorrb.SetHelpText(mtexts.txts['HelpSZPromissor'])
		vzodsizer.Add(self.szpromissorrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.szsignificatorrb = wx.RadioButton(self, -1, mtexts.txts['SZSignificator'])
		self.szsignificatorrb.SetHelpText(mtexts.txts['HelpSZSignificator'])
		vzodsizer.Add(self.szsignificatorrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.szbothrb = wx.RadioButton(self, -1, mtexts.txts['SZBoth'])
		self.szbothrb.SetHelpText(mtexts.txts['HelpSZBoth'])
		vzodsizer.Add(self.szbothrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		hzodsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.szbianchinickb = wx.CheckBox(self, -1, mtexts.txts['Bianchini'])
		hzodsizer.Add(self.szbianchinickb, 0, wx.ALIGN_LEFT|wx.LEFT, 20)
		vzodsizer.Add(hzodsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		ssubtype = wx.StaticBox(self, label='')
		subtypesizer = wx.StaticBoxSizer(ssubtype, wx.VERTICAL)
		self.mundanerb = wx.RadioButton(self, -1, mtexts.txts['Mundane'], style=wx.RB_GROUP)
		subtypesizer.Add(self.mundanerb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
		self.mundanerb.SetHelpText(mtexts.txts['HelpMundane'])
		self.zodiacalrb = wx.RadioButton(self, -1, mtexts.txts['Zodiacal'])
		self.zodiacalrb.SetHelpText(mtexts.txts['HelpZodiacal'])
		subtypesizer.Add(self.zodiacalrb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
		subtypesizer.Add(vzodsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 20)
#		self.bothrb = wx.RadioButton(self, -1, mtexts.txts['Both'])
#		subtypesizer.Add(self.bothrb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)

		self.Bind(wx.EVT_RADIOBUTTON, self.onMundane, id=self.mundanerb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onZodiacal, id=self.zodiacalrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onSZNeither, id=self.szneitherrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onSZPromissor, id=self.szpromissorrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onSZSignificator, id=self.szsignificatorrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.onSZBoth, id=self.szbothrb.GetId())
#		self.Bind(wx.EVT_RADIOBUTTON, self.onBoth, id=self.bothrb.GetId())

		vsizer.Add(subtypesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.BOTTOM, 5)

		self.zodopt = wx.StaticBox(self, label=mtexts.txts['ZodiacalOpts'])
		zodoptsizer = wx.StaticBoxSizer(self.zodopt, wx.VERTICAL)
		self.aspspromstosigsckb = wx.CheckBox(self, -1, mtexts.txts['ZodAspsPromsToSigs1'])
		zodoptsizer.Add(self.aspspromstosigsckb, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.labelzodopt1 = wx.StaticText(self, -1, mtexts.txts['ZodAspsPromsToSigs2'])
		vsubsizer.Add(self.labelzodopt1, 0, wx.ALIGN_LEFT|wx.LEFT, 30)
		zodoptsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.promstosigaspsckb = wx.CheckBox(self, -1, mtexts.txts['ZodPromsToSigAsps1'])
		zodoptsizer.Add(self.promstosigaspsckb, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.labelzodopt2 = wx.StaticText(self, -1, mtexts.txts['ZodPromsToSigAsps2'])
		vsubsizer.Add(self.labelzodopt2, 0, wx.ALIGN_LEFT|wx.LEFT, 30)
		zodoptsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.ascmchcsaqspromsckb = wx.CheckBox(self, -1, mtexts.txts['ZodAscMCHCsAsProms'])
		zodoptsizer.Add(self.ascmchcsaqspromsckb, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)

		vsizer.Add(zodoptsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.BOTTOM, 5)
		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 0)

		#Apply
		sapply = wx.StaticBox(self, label='')
		applysizer = wx.StaticBoxSizer(sapply, wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(2, 3)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Promissors'])
		vsizer.Add(label, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promsunckb = wx.CheckBox(self, -1, mtexts.txts['Sun'])
		vsizer.Add(self.promsunckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.prommoonckb = wx.CheckBox(self, -1, mtexts.txts['Moon'])
		vsizer.Add(self.prommoonckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.secmotionckb = wx.CheckBox(self, -1, mtexts.txts['SecondaryMotion'])
		vsubsizer.Add(self.secmotionckb, 0)#, wx.ALIGN_LEFT|wx.LEFT, 15)
		self.secmotionitercb = wx.ComboBox(self, -1, mtexts.smiterList[0], size=(100, -1), choices=mtexts.smiterList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		vsubsizer.Add(self.secmotionitercb, 0)#, wx.ALIGN_LEFT|wx.LEFT, 15)
		hsubsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 15)
		vsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.prommercuryckb = wx.CheckBox(self, -1, mtexts.txts['Mercury'])
		vsizer.Add(self.prommercuryckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promvenusckb = wx.CheckBox(self, -1, mtexts.txts['Venus'])
		vsizer.Add(self.promvenusckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.prommarsckb = wx.CheckBox(self, -1, mtexts.txts['Mars'])
		vsizer.Add(self.prommarsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promjupiterckb = wx.CheckBox(self, -1, mtexts.txts['Jupiter'])
		vsizer.Add(self.promjupiterckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promsaturnckb = wx.CheckBox(self, -1, mtexts.txts['Saturn'])
		vsizer.Add(self.promsaturnckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promuranusckb = wx.CheckBox(self, -1, mtexts.txts['Uranus'])
		vsizer.Add(self.promuranusckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promneptuneckb = wx.CheckBox(self, -1, mtexts.txts['Neptune'])
		vsizer.Add(self.promneptuneckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promplutockb = wx.CheckBox(self, -1, mtexts.txts['Pluto'])
		vsizer.Add(self.promplutockb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promanodeckb = wx.CheckBox(self, -1, mtexts.txts['AscNode'])
		vsizer.Add(self.promanodeckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promdnodeckb = wx.CheckBox(self, -1, mtexts.txts['DescNode'])
		vsizer.Add(self.promdnodeckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promantsckb = wx.CheckBox(self, -1, mtexts.txts['Antiscia'])
		vsizer.Add(self.promantsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
#		self.prommidpointsckb = wx.CheckBox(self, -1, mtexts.txts['MidPoints'])
#		vsizer.Add(self.prommidpointsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promlofckb = wx.CheckBox(self, -1, mtexts.txts['LoF'])
		vsizer.Add(self.promlofckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.promtermsckb = wx.CheckBox(self, -1, mtexts.txts['Terms2'])
		vsizer.Add(self.promtermsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)

		self.Bind(wx.EVT_CHECKBOX, self.onPromMoon, id=self.prommoonckb.GetId())

		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.conjunctiockb = wx.CheckBox(self, -1, mtexts.txts['Conjunctio'])
		vsizer.Add(self.conjunctiockb, 0, wx.ALIGN_LEFT|wx.TOP, 20)
		self.semisextilckb = wx.CheckBox(self, -1, mtexts.txts['Semisextil'])
		vsizer.Add(self.semisextilckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.semiquadratckb = wx.CheckBox(self, -1, mtexts.txts['Semiquadrat'])
		vsizer.Add(self.semiquadratckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.sextilckb = wx.CheckBox(self, -1, mtexts.txts['Sextil'])
		vsizer.Add(self.sextilckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.quintileckb = wx.CheckBox(self, -1, mtexts.txts['Quintile'])
		vsizer.Add(self.quintileckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.quadratckb = wx.CheckBox(self, -1, mtexts.txts['Quadrat'])
		vsizer.Add(self.quadratckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.trigonckb = wx.CheckBox(self, -1, mtexts.txts['Trigon'])
		vsizer.Add(self.trigonckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.sesquiquadratckb = wx.CheckBox(self, -1, mtexts.txts['Sesquiquadrat'])
		vsizer.Add(self.sesquiquadratckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.biquintileckb = wx.CheckBox(self, -1, mtexts.txts['Biquintile'])
		vsizer.Add(self.biquintileckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.quinqunxckb = wx.CheckBox(self, -1, mtexts.txts['Quinqunx'])
		vsizer.Add(self.quinqunxckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.oppositiockb = wx.CheckBox(self, -1, mtexts.txts['Oppositio'])
		vsizer.Add(self.oppositiockb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.mundaneparckb = wx.CheckBox(self, -1, mtexts.txts['Parallel'])
		vsizer.Add(self.mundaneparckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.raptparckb = wx.CheckBox(self, -1, mtexts.txts['RaptParallel'])
		vsizer.Add(self.raptparckb, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		scustomer = wx.StaticBox(self, label=mtexts.txts['Promissors'])
		customersizer = wx.StaticBoxSizer(scustomer, wx.VERTICAL)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.customerckb = wx.CheckBox(self, -1, '')
		hsizer.Add(self.customerckb, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		ID_Customer = wx.NewId()
		self.btnCustomer = wx.Button(self, ID_Customer, mtexts.txts['Customer2'])
		self.Bind(wx.EVT_BUTTON, self.onCustomer, id=ID_Customer)
		self.Bind(wx.EVT_CHECKBOX, self.onCustomerCheck, id=self.customerckb.GetId())
		hsizer.Add(self.btnCustomer, 0, wx.ALIGN_LEFT)
		vsubsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM, 2)
		customersizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		vsizer.Add(customersizer, 0, wx.ALIGN_LEFT|wx.TOP, 10)

		scustomer2 = wx.StaticBox(self, label=mtexts.txts['Significators'])
		customer2sizer = wx.StaticBoxSizer(scustomer2, wx.VERTICAL)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.customer2ckb = wx.CheckBox(self, -1, '')
		hsizer.Add(self.customer2ckb, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		ID_Customer2 = wx.NewId()
		self.btnCustomer2 = wx.Button(self, ID_Customer2, mtexts.txts['User2'])
		self.Bind(wx.EVT_BUTTON, self.onCustomer2, id=ID_Customer2)
		self.Bind(wx.EVT_CHECKBOX, self.onCustomer2Check, id=self.customer2ckb.GetId())
		hsizer.Add(self.btnCustomer2, 0, wx.ALIGN_LEFT)
		vsubsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM, 2)
		customer2sizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		vsizer.Add(customer2sizer, 0, wx.ALIGN_LEFT|wx.TOP, 5)

		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Significators'])
		vsizer.Add(label, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigascckb = wx.CheckBox(self, -1, 'Asc')
		vsizer.Add(self.sigascckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigmcckb = wx.CheckBox(self, -1, 'MC')
		vsizer.Add(self.sigmcckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sighousecuspsckb = wx.CheckBox(self, -1, mtexts.txts['HouseCusps'])
		vsizer.Add(self.sighousecuspsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)

		self.sigsunckb = wx.CheckBox(self, -1, mtexts.txts['Sun'])
		vsizer.Add(self.sigsunckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigmoonckb = wx.CheckBox(self, -1, mtexts.txts['Moon'])
		vsizer.Add(self.sigmoonckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigmercuryckb = wx.CheckBox(self, -1, mtexts.txts['Mercury'])
		vsizer.Add(self.sigmercuryckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigvenusckb = wx.CheckBox(self, -1, mtexts.txts['Venus'])
		vsizer.Add(self.sigvenusckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigmarsckb = wx.CheckBox(self, -1, mtexts.txts['Mars'])
		vsizer.Add(self.sigmarsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigjupiterckb = wx.CheckBox(self, -1, mtexts.txts['Jupiter'])
		vsizer.Add(self.sigjupiterckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigsaturnckb = wx.CheckBox(self, -1, mtexts.txts['Saturn'])
		vsizer.Add(self.sigsaturnckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.siguranusckb = wx.CheckBox(self, -1, mtexts.txts['Uranus'])
		vsizer.Add(self.siguranusckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.signeptuneckb = wx.CheckBox(self, -1, mtexts.txts['Neptune'])
		vsizer.Add(self.signeptuneckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigplutockb = wx.CheckBox(self, -1, mtexts.txts['Pluto'])
		vsizer.Add(self.sigplutockb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.siganodeckb = wx.CheckBox(self, -1, mtexts.txts['AscNode'])
		vsizer.Add(self.siganodeckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigdnodeckb = wx.CheckBox(self, -1, mtexts.txts['DescNode'])
		vsizer.Add(self.sigdnodeckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.siglofckb = wx.CheckBox(self, -1, mtexts.txts['LoF'])
		vsizer.Add(self.siglofckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.sigsyzckb = wx.CheckBox(self, -1, mtexts.txts['Syzygy'])
		vsizer.Add(self.sigsyzckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)

		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		applysizer.Add(fgsizer, 0, wx.ALIGN_LEFT, 5)
		mhsizer.Add(applysizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 5)

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
		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()


	def onPlacidian(self, event):
		self.mundanerb.Enable(True)
#		self.bothrb.Enable(True)

		mun = self.mundanerb.GetValue()
		bianchini = False
		if not mun:
			if self.szbothrb.GetValue():
				bianchini = True
		if mun:
			self.enableSubZods(False, bianchini)
			self.enableZodOpts(False)
			self.enableZods(False)
			self.siglofckb.Enable(True)
			self.raptparckb.Enable(True)


	def onPlacidianUTP(self, event):
		self.mundanerb.Enable(False)
#		self.bothrb.Enable(False)
		self.zodiacalrb.SetValue(True)
		bianchini = False
		if self.szbothrb.GetValue():
			bianchini = True
		self.enableSubZods(True, bianchini)
		self.enableZodOpts(True)
		self.enableZods(True)
		self.siglofckb.Enable(True)
		self.raptparckb.Enable(False)


	def onRegiomontan(self, event):
		self.mundanerb.Enable(True)
#		self.bothrb.Enable(True)
		mun = self.mundanerb.GetValue()
		self.siglofckb.Enable(not mun)
		bianchini = False
		if not mun:
			if self.szbothrb.GetValue():
				bianchini = True
		if mun:
			self.enableSubZods(False, bianchini)
			self.enableZodOpts(False)
			self.enableZods(False)
			self.siglofckb.Enable(True)
		self.raptparckb.Enable(False)


	def onMundane(self, event):
		self.enableSubZods(False)
		self.enableZodOpts(False)
		self.enableZods(False)
		plac = self.placidiansemiarcrb.GetValue()
		self.siglofckb.Enable(plac)
		self.raptparckb.Enable(plac)


	def onZodiacal(self, event):
		bianchini = False
		if self.szbothrb.GetValue():
			bianchini = True

		self.enableSubZods(True, bianchini)
		self.enableZodOpts(True)
		self.enableZods(True)
		self.siglofckb.Enable(True)
		self.raptparckb.Enable(False)


	def onSZNeither(self, event):
		self.szbianchinickb.Enable(False)


	def onSZPromissor(self, event):
		self.szbianchinickb.Enable(False)
		self.szbianchinickb.SetValue(False)#The code of the PDs was designed acc. to Bianchini belonging to Promissor-only


	def onSZSignificator(self, event):
		self.szbianchinickb.Enable(False)
		self.szbianchinickb.SetValue(False)#The code of the PDs was designed acc. to Bianchini belonging to Promissor-only


	def onSZBoth(self, event):
		self.szbianchinickb.Enable(True)


	def onBoth(self, event):
		bianchini = False
		if self.szbothrb.GetValue():
			bianchini = True
		self.enableSubZods(True, bianchini)
		self.enableZodOpts(True)
		self.enableZods(True)
		plac = self.placidiansemiarcrb.GetValue()
		self.raptparckb.Enable(plac)


	def onPromMoon(self, event):
		self.secmotionckb.Enable(self.prommoonckb.GetValue())
		self.secmotionitercb.Enable(self.prommoonckb.GetValue())


	def enableSubZods(self, val, bianchini = False):
		self.szneitherrb.Enable(val)
		self.szpromissorrb.Enable(val)
		self.szsignificatorrb.Enable(val)
		self.szbothrb.Enable(val)
		self.szbianchinickb.Enable(bianchini)


	def enableZodOpts(self, val):
		self.zodopt.Enable(val)
		self.aspspromstosigsckb.Enable(val)
		self.promstosigaspsckb.Enable(val)
		self.ascmchcsaqspromsckb.Enable(val)
		self.labelzodopt1.Enable(val)
		self.labelzodopt2.Enable(val)


	def enableZods(self, val):
		self.promlofckb.Enable(val)
		self.promtermsckb.Enable(val)
		self.sigsyzckb.Enable(val)


	def onCustomerCheck(self, event):
		self.btnCustomer.Enable(self.customerckb.GetValue())


	def onCustomer(self, event):
		dlg = customerdlg.CustomerDlg(self, mtexts.txts['Customer2'])
		dlg.CenterOnParent()
		dlg.initialize(self.cpdlons, self.cpdlats, self.southern)

		val = dlg.ShowModal()
		if val == wx.ID_OK:	
			if dlg.check(self.cpdlons, self.cpdlats, self.southern):
				self.cpdlons[0] = int(dlg.londeg.GetValue())
				self.cpdlons[1] = int(dlg.lonmin.GetValue())
				self.cpdlons[2] = int(dlg.lonsec.GetValue())
				self.cpdlats[0] = int(dlg.latdeg.GetValue())
				self.cpdlats[1] = int(dlg.latmin.GetValue())
				self.cpdlats[2] = int(dlg.latsec.GetValue())
				self.southern = dlg.southernckb.GetValue()

		dlg.Destroy()


	def onCustomer2Check(self, event):
		self.btnCustomer2.Enable(self.customer2ckb.GetValue())


	def onCustomer2(self, event):
		dlg = customerdlg.CustomerDlg(self, mtexts.txts['User2'])
		dlg.CenterOnParent()
		dlg.initialize(self.cpd2lons, self.cpd2lats, self.southern2)

		val = dlg.ShowModal()
		if val == wx.ID_OK:	
			if dlg.check(self.cpd2lons, self.cpd2lats, self.southern2):
				self.cpd2lons[0] = int(dlg.londeg.GetValue())
				self.cpd2lons[1] = int(dlg.lonmin.GetValue())
				self.cpd2lons[2] = int(dlg.lonsec.GetValue())
				self.cpd2lats[0] = int(dlg.latdeg.GetValue())
				self.cpd2lats[1] = int(dlg.latmin.GetValue())
				self.cpd2lats[2] = int(dlg.latsec.GetValue())
				self.southern2 = dlg.southernckb.GetValue()

		dlg.Destroy()


	def fill(self, options):
		self.secmotionckb.SetValue(options.pdsecmotion)
		self.secmotionitercb.SetStringSelection(mtexts.smiterList[options.pdsecmotioniter])

		#Significators
		ckbs = [self.sigascckb, self.sigmcckb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.sigascmc[i])

		self.sighousecuspsckb.SetValue(options.sighouses)

		ckbs = [self.sigsunckb, self.sigmoonckb, self.sigmercuryckb, self.sigvenusckb, self.sigmarsckb, self.sigjupiterckb, self.sigsaturnckb, self.siguranusckb, self.signeptuneckb, self.sigplutockb, self.siganodeckb, self.sigdnodeckb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.sigplanets[i])

		self.siglofckb.SetValue(options.pdlof[1])

		self.sigsyzckb.SetValue(options.pdsyzygy)

		#Promissors
		ckbs = [self.promsunckb, self.prommoonckb, self.prommercuryckb, self.promvenusckb, self.prommarsckb, self.promjupiterckb, self.promsaturnckb, self.promuranusckb, self.promneptuneckb, self.promplutockb, self.promanodeckb, self.promdnodeckb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.promplanets[i])

		self.promlofckb.SetValue(options.pdlof[0])

		self.promtermsckb.SetValue(options.pdterms)

		self.promantsckb.SetValue(options.pdantiscia)

#		self.prommidpointsckb.SetValue(options.pdmidpoints)

		self.secmotionckb.Enable(self.prommoonckb.GetValue())
		self.secmotionitercb.Enable(self.prommoonckb.GetValue())

		#Aspects
		ckbs = [self.conjunctiockb, self.semisextilckb, self.semiquadratckb, self.sextilckb, self.quintileckb, self.quadratckb, self.trigonckb, self.sesquiquadratckb, self.biquintileckb, self.quinqunxckb, self.oppositiockb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.pdaspects[i])

		ckbs = [self.mundaneparckb, self.raptparckb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.pdparallels[i])

		self.customerckb.SetValue(options.pdcustomer)
		self.btnCustomer.Enable(options.pdcustomer)

		self.customer2ckb.SetValue(options.pdcustomer2)
		self.btnCustomer2.Enable(options.pdcustomer2)

		if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
			self.placidiansemiarcrb.SetValue(True)
		elif options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
			self.placidianutprb.SetValue(True)
			self.mundanerb.Enable(False)
#			self.bothrb.Enable(False)
		elif options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
			self.regiomontanrb.SetValue(True)
		elif options.primarydir == primdirs.PrimDirs.CAMPANIAN:
			self.placidiansemiarcrb.SetValue(True)

		if options.subprimarydir == primdirs.PrimDirs.MUNDANE:
			self.mundanerb.SetValue(True)
			self.enableSubZods(False, False)
			self.enableZodOpts(False)
			self.enableZods(False)
			if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
				self.raptparckb.Enable(True)
				self.siglofckb.Enable(True)
			else:
				self.siglofckb.Enable(False)
				self.raptparckb.Enable(False)
		elif options.subprimarydir == primdirs.PrimDirs.ZODIACAL:
			self.zodiacalrb.SetValue(True)
			self.enableZods(True)
			self.enableZodOpts(True)
			self.raptparckb.Enable(False)
			self.siglofckb.Enable(True)
		elif options.subprimarydir == primdirs.PrimDirs.BOTH:
#			self.bothrb.SetValue(True)
			self.enableZods(True)
			self.enableZodOpts(True)
			if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
				self.raptparckb.Enable(True)
			else:
				self.raptparckb.Enable(False)
			self.siglofckb.Enable(True)

		if options.subzodiacal == primdirs.PrimDirs.SZNEITHER:
			self.szneitherrb.SetValue(True)
			self.szbianchinickb.Enable(False)
		elif options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR:
			self.szpromissorrb.SetValue(True)
			self.szbianchinickb.Enable(False)
		elif options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR:
			self.szsignificatorrb.SetValue(True)
			self.szbianchinickb.Enable(False)
		elif options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			self.szbothrb.SetValue(True)

		self.szbianchinickb.SetValue(options.bianchini)

		ckbs = [self.aspspromstosigsckb, self.promstosigaspsckb]
		for i in range(len(ckbs)):
			ckbs[i].SetValue(options.zodpromsigasps[i])

		self.ascmchcsaqspromsckb.SetValue(options.ascmchcsasproms)


	def check(self, options):
		changed = False
		changedU1 = False
		changedU2 = False

		#save to options
		if self.placidiansemiarcrb.GetValue():
			if options.primarydir != primdirs.PrimDirs.PLACIDIANSEMIARC:
				options.primarydir = primdirs.PrimDirs.PLACIDIANSEMIARC
				changed = True
		elif self.placidianutprb.GetValue():
			if options.primarydir != primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
				options.primarydir = primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE
				changed = True
		elif self.regiomontanrb.GetValue():
			if options.primarydir != primdirs.PrimDirs.REGIOMONTAN:
				options.primarydir = primdirs.PrimDirs.REGIOMONTAN
				changed = True

		if self.mundanerb.GetValue():
			if options.subprimarydir != primdirs.PrimDirs.MUNDANE:
				options.subprimarydir = primdirs.PrimDirs.MUNDANE
				changed = True
		elif self.zodiacalrb.GetValue():
			if options.subprimarydir != primdirs.PrimDirs.ZODIACAL:
				options.subprimarydir = primdirs.PrimDirs.ZODIACAL
				changed = True
#		elif self.bothrb.GetValue():
#			if options.subprimarydir != primdirs.PrimDirs.BOTH:
#				options.subprimarydir = primdirs.PrimDirs.BOTH
#				changed = True

		if self.szneitherrb.GetValue():
			if options.subzodiacal != primdirs.PrimDirs.SZNEITHER:
				options.subzodiacal = primdirs.PrimDirs.SZNEITHER
				changed = True
		elif self.szpromissorrb.GetValue():
			if options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR:
				options.subzodiacal = primdirs.PrimDirs.SZPROMISSOR
				changed = True
		elif self.szsignificatorrb.GetValue():
			if options.subzodiacal != primdirs.PrimDirs.SZSIGNIFICATOR:
				options.subzodiacal = primdirs.PrimDirs.SZSIGNIFICATOR
				changed = True
		elif self.szbothrb.GetValue():
			if options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				options.subzodiacal = primdirs.PrimDirs.SZBOTH
				changed = True

		if options.bianchini != self.szbianchinickb.GetValue():
			options.bianchini = self.szbianchinickb.GetValue()
			changed = True

		ckbs = [self.aspspromstosigsckb, self.promstosigaspsckb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.zodpromsigasps[i]:
				options.zodpromsigasps[i] = ckbs[i].GetValue()
				changed = True

		if self.ascmchcsaqspromsckb.GetValue() != options.ascmchcsasproms:
			options.ascmchcsasproms = self.ascmchcsaqspromsckb.GetValue()
			changed = True

		ckbs = [self.sigascckb, self.sigmcckb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.sigascmc[i]:
				options.sigascmc[i] = ckbs[i].GetValue()
				changed = True

		if self.sighousecuspsckb.GetValue() != options.sighouses:
			options.sighouses = self.sighousecuspsckb.GetValue()
			changed = True

		ckbs = [self.sigsunckb, self.sigmoonckb, self.sigmercuryckb, self.sigvenusckb, self.sigmarsckb, self.sigjupiterckb, self.sigsaturnckb, self.siguranusckb, self.signeptuneckb, self.sigplutockb, self.siganodeckb, self.sigdnodeckb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.sigplanets[i]:
				options.sigplanets[i] = ckbs[i].GetValue()
				changed = True

		if options.pdlof[1] != self.siglofckb.GetValue():
			options.pdlof[1] = self.siglofckb.GetValue()
			changed = True

		if options.pdsyzygy != self.sigsyzckb.GetValue():
			options.pdsyzygy = self.sigsyzckb.GetValue()
			changed = True

		ckbs = [self.promsunckb, self.prommoonckb, self.prommercuryckb, self.promvenusckb, self.prommarsckb, self.promjupiterckb, self.promsaturnckb, self.promuranusckb, self.promneptuneckb, self.promplutockb, self.promanodeckb, self.promdnodeckb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.promplanets[i]:
				options.promplanets[i] = ckbs[i].GetValue()
				changed = True

#		if self.prommidpointsckb.GetValue() != options.pdmidpoints:
#			options.pdmidpoints = self.prommidpointsckb.GetValue()
#			changed = True

		if options.pdantiscia != self.promantsckb.GetValue():
			options.pdantiscia = self.promantsckb.GetValue()
			changed = True

		if options.pdlof[0] != self.promlofckb.GetValue():
			options.pdlof[0] = self.promlofckb.GetValue()
			changed = True

		if options.pdterms != self.promtermsckb.GetValue():
			options.pdterms = self.promtermsckb.GetValue()
			changed = True

		ckbs = [self.conjunctiockb, self.semisextilckb, self.semiquadratckb, self.sextilckb, self.quintileckb, self.quadratckb, self.trigonckb, self.sesquiquadratckb, self.biquintileckb, self.quinqunxckb, self.oppositiockb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.pdaspects[i]:
				options.pdaspects[i] = ckbs[i].GetValue()
				changed = True

		ckbs = [self.mundaneparckb, self.raptparckb]
		for i in range(len(ckbs)):
			if ckbs[i].GetValue() != options.pdparallels[i]:
				options.pdparallels[i] = ckbs[i].GetValue()
				changed = True

		if self.secmotionckb.GetValue() != options.pdsecmotion:
			options.pdsecmotion = self.secmotionckb.GetValue()
			changed = True

		if self.secmotionitercb.GetCurrentSelection() != options.pdsecmotioniter:
			options.pdsecmotioniter = self.secmotionitercb.GetCurrentSelection()
			changed = True

		if self.customerckb.GetValue() != options.pdcustomer:
			options.pdcustomer = self.customerckb.GetValue()
			changed = True
			changedU1 = True

		for i in range(3):
			if options.pdcustomerlon[i] != self.cpdlons[i]:
				options.pdcustomerlon[i] = self.cpdlons[i]
				changed = True
				changedU1 = True

			if options.pdcustomerlat[i] != self.cpdlats[i]:
				options.pdcustomerlat[i] = self.cpdlats[i]
				changed = True
				changedU1 = True

		if self.options.pdcustomersouthern != self.southern:
			options.pdcustomersouthern = self.southern
			changed = True
			changedU1 = True

		if self.customer2ckb.GetValue() != options.pdcustomer2:
			options.pdcustomer2 = self.customer2ckb.GetValue()
			changed = True
			changedU2 = True

		for i in range(3):
			if options.pdcustomer2lon[i] != self.cpd2lons[i]:
				options.pdcustomer2lon[i] = self.cpd2lons[i]
				changed = True
				changedU2 = True

			if options.pdcustomer2lat[i] != self.cpd2lats[i]:
				options.pdcustomer2lat[i] = self.cpd2lats[i]
				changed = True
				changedU2 = True

		if self.options.pdcustomer2southern != self.southern2:
			options.pdcustomer2southern = self.southern2
			changed = True
			changedU2 = True

		return changed, changedU1, changedU2




