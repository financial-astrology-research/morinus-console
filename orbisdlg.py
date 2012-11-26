import  wx
import copy
import chart
import floatvalidator
import planets
import fixstarsorbdlg
import mtexts


class OrbisDlg(wx.Dialog):
	def __init__(self, parent, options):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Orbis'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		self.parent = parent
		self.options = options

		self.orbis = copy.deepcopy(self.options.orbis)

		self.orbisplanetspar = copy.deepcopy(self.options.orbisplanetspar)

		self.orbisH = copy.deepcopy(self.options.orbisH)

		self.orbisparH = copy.deepcopy(self.options.orbisparH)

		self.orbisAscMC = copy.deepcopy(self.options.orbisAscMC)

		self.orbisparAscMC = copy.deepcopy(self.options.orbisparAscMC)

		self.baseid = wx.NewId()

		self.ID_Sun = self.baseid
		self.ID_Moon = wx.NewId()
		self.ID_Mercury = wx.NewId()
		self.ID_Venus = wx.NewId()
		self.ID_Mars = wx.NewId()
		self.ID_Jupiter = wx.NewId()
		self.ID_Saturnus = wx.NewId()
		self.ID_Uranus = wx.NewId()
		self.ID_Neptune = wx.NewId()
		self.ID_Pluto = wx.NewId()
		self.ID_Nodes = wx.NewId()		
		self.ID_AscMC = wx.NewId()		
		self.ID_Houses = wx.NewId()		

		self.fixstars = self.options.fixstars.copy()

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Planets
		splanets =wx.StaticBox(self, label='')
		splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
		self.sun = wx.RadioButton(self, self.ID_Sun, mtexts.txts['Sun'], style=wx.RB_GROUP)
		splanetssizer.Add(self.sun, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.moon = wx.RadioButton(self, self.ID_Moon, mtexts.txts['Moon'])
		splanetssizer.Add(self.moon, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.mercury = wx.RadioButton(self, self.ID_Mercury, mtexts.txts['Mercury'])
		splanetssizer.Add(self.mercury, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.venus = wx.RadioButton(self, self.ID_Venus, mtexts.txts['Venus'])
		splanetssizer.Add(self.venus, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.mars = wx.RadioButton(self, self.ID_Mars, mtexts.txts['Mars'])
		splanetssizer.Add(self.mars, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.jupiter = wx.RadioButton(self, self.ID_Jupiter, mtexts.txts['Jupiter'])
		splanetssizer.Add(self.jupiter, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.saturnus = wx.RadioButton(self, self.ID_Saturnus, mtexts.txts['Saturn'])
		splanetssizer.Add(self.saturnus, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.uranus = wx.RadioButton(self, self.ID_Uranus, mtexts.txts['Uranus'])
		splanetssizer.Add(self.uranus, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.neptune = wx.RadioButton(self, self.ID_Neptune, mtexts.txts['Neptune'])
		splanetssizer.Add(self.neptune, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.pluto = wx.RadioButton(self, self.ID_Pluto, mtexts.txts['Pluto'])
		splanetssizer.Add(self.pluto, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.nodes = wx.RadioButton(self, self.ID_Nodes, mtexts.txts['Nodes'])
		splanetssizer.Add(self.nodes, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.ascmc = wx.RadioButton(self, self.ID_AscMC, mtexts.txts['AscMC'])
		splanetssizer.Add(self.ascmc, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.houses = wx.RadioButton(self, self.ID_Houses, mtexts.txts['Houses'])
		splanetssizer.Add(self.houses, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(splanetssizer, 1, wx.GROW)

		#Cusps
		self.scusps = wx.StaticBox(self, label='')
		scuspssizer = wx.StaticBoxSizer(self.scusps, wx.VERTICAL)
		gsizer = wx.GridSizer(1, 2)
		label = wx.StaticText(self, -1, mtexts.txts['AscMC2']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.cuspascmc = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.cuspascmc, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 2)
		self.cuspascmc.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Interm']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.cuspinter = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.cuspinter, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.cuspinter.SetMaxLength(4)
		scuspssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 2)

		vsizer.Add(scuspssizer, 0, wx.GROW|wx.TOP, 0)

		#Exact
		self.sexact =wx.StaticBox(self, label='')
		sexactsizer = wx.StaticBoxSizer(self.sexact, wx.VERTICAL)
		gsizer = wx.GridSizer(1, 2)
		label = wx.StaticText(self, -1, mtexts.txts['Exact']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.exact = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.exact, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		sexactsizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vsizer.Add(sexactsizer, 0, wx.GROW|wx.TOP, 0)
		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)

		#Aspects
		self.saspects =wx.StaticBox(self, label=mtexts.txts['Aspects'])
		saspectssizer = wx.StaticBoxSizer(self.saspects, wx.VERTICAL)
		gsizer = wx.GridSizer(13, 2)
		label = wx.StaticText(self, -1, mtexts.txts['Conjunctio']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.conjunctio = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.conjunctio, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.conjunctio.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Semisextil']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.semisextil = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.semisextil, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.semisextil.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Semiquadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.semiquadrat = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.semiquadrat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.semiquadrat.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Sextil']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sextil = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.sextil, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sextil.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Quintile']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quintile = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.quintile, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quintile.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Quadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quadrat = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.quadrat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quadrat.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Trigon']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.trigon = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.trigon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.trigon.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Sesquiquadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sesquiquadrat = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.sesquiquadrat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sesquiquadrat.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Biquintile']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.biquintile = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.biquintile, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.biquintile.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Quinqunx']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quinqunx = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.quinqunx, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.quinqunx.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Oppositio']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.oppositio = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.oppositio, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.oppositio.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Parallel']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.parallel = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.parallel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.parallel.SetMaxLength(4)
		label = wx.StaticText(self, -1, mtexts.txts['Contraparallel']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.contraparallel = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 10.0), size=(50, -1))
		gsizer.Add(self.contraparallel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.contraparallel.SetMaxLength(4)

		saspectssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(saspectssizer, 1, wx.GROW|wx.TOP, 0)

		self.sfixstars =wx.StaticBox(self, label='')
		sfixstarssizer = wx.StaticBoxSizer(self.sfixstars, wx.VERTICAL)	
		ID_FixStars = wx.NewId()
		btnFixStars = wx.Button(self, ID_FixStars, mtexts.txts['FixStars'])
		self.Bind(wx.EVT_BUTTON, self.onFixStars, id=ID_FixStars)
		sfixstarssizer.Add(btnFixStars, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		vsizer.Add(sfixstarssizer, 0, wx.GROW|wx.TOP, 0)

		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()

		self.sun.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.moon.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.mercury.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.venus.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.mars.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.jupiter.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.saturnus.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.uranus.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.neptune.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.pluto.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.nodes.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.ascmc.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.houses.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
	
		self.arasps = [self.conjunctio, self.semisextil, self.semiquadrat, self.sextil, self.quintile, self.quadrat, self.trigon, self.sesquiquadrat, self.biquintile, self.quinqunx, self.oppositio]

		self.currid = self.ID_Sun-self.baseid

		#Load
		self.cuspascmc.SetValue(str(self.options.orbiscuspAscMC))
		self.cuspinter.SetValue(str(self.options.orbiscuspH))

		self.exact.SetValue(str(self.options.exact))
		
		for i in range(chart.Chart.ASPECT_NUM):
			self.arasps[i].SetValue(str(self.orbis[self.currid][i]))

		self.parallel.SetValue(str(self.orbisplanetspar[self.currid][0]))
		self.contraparallel.SetValue(str(self.orbisplanetspar[self.currid][1]))

		self.sun.SetValue(True)

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)


	def onOK(self, event):
		if (self.Validate() and self.scusps.Validate() and self.sexact.Validate() and self.saspects.Validate()):
			self.Close()
			self.SetReturnCode(wx.ID_OK)


	def onBtn(self, event):
		rid = event.GetId()-self.baseid
		
		if rid == self.currid:
			return

		bValidated = False
		if (self.Validate() and self.scusps.Validate() and self.sexact.Validate() and self.saspects.Validate()):
			bValidated = True

		if rid <= self.ID_Nodes-self.baseid: # planets
			if bValidated:
				self.save(self.currid)

			for i in range(chart.Chart.ASPECT_NUM):
				self.arasps[i].SetValue(str(self.orbis[rid][i]))

			self.parallel.SetValue(str(self.orbisplanetspar[rid][0]))
			self.contraparallel.SetValue(str(self.orbisplanetspar[rid][1]))

		elif rid == self.ID_AscMC-self.baseid: #AscMC
			if bValidated:
				self.save(self.currid)

			for i in range(chart.Chart.ASPECT_NUM):
				self.arasps[i].SetValue(str(self.orbisAscMC[i]))
			self.parallel.SetValue(str(self.orbisparAscMC[0]))
			self.contraparallel.SetValue(str(self.orbisparAscMC[1]))
		else: # Houses
			if bValidated:
				self.save(self.currid)

			for i in range(chart.Chart.ASPECT_NUM):
				self.arasps[i].SetValue(str(self.orbisH[i]))
			self.parallel.SetValue(str(self.orbisparH[0]))
			self.contraparallel.SetValue(str(self.orbisparH[1]))

		self.currid = rid


	def save(self, currid):
		if currid <= self.ID_Nodes-self.baseid:
			for i in range(chart.Chart.ASPECT_NUM):
				self.orbis[currid][i] = float(self.arasps[i].GetValue())
			self.orbisplanetspar[currid][0] = float(self.parallel.GetValue())
			self.orbisplanetspar[currid][1] = float(self.contraparallel.GetValue())
		elif self.currid == self.ID_AscMC-self.baseid:
			for i in range(chart.Chart.ASPECT_NUM):
				self.orbisAscMC[i] = float(self.arasps[i].GetValue())
			self.orbisparAscMC[0] = float(self.parallel.GetValue())
			self.orbisparAscMC[1] = float(self.contraparallel.GetValue())
		else:
			for i in range(chart.Chart.ASPECT_NUM):
				self.orbisH[i] = float(self.arasps[i].GetValue())			
			self.orbisparH[0] = float(self.parallel.GetValue())
			self.orbisparH[1] = float(self.contraparallel.GetValue())


	def onFixStars(self, evt):
		if not self.parent.checkFixStars():
			return

		if len(self.options.fixstars) == 0:
			dlgm = wx.MessageDialog(self, mtexts.txts['NoSelFixStars'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
			return	

		dlg = fixstarsorbdlg.FixStarsOrbDlg(self, self.fixstars)
		dlg.CenterOnParent()

		val = dlg.ShowModal()
		if val == wx.ID_OK:	
			self.fixstars = dlg.getFixstars()
			# and check it in OK-btn

		dlg.Destroy()


	def check(self, options):
		changed = False

		#copy selforbs to options-orbs
		for a in range(chart.Chart.ASPECT_NUM):
			for i in range(planets.Planets.PLANETS_NUM-1):
				if options.orbis[i][a] != self.orbis[i][a]:
					options.orbis[i][a] = self.orbis[i][a]
					changed = True
		for i in range(planets.Planets.PLANETS_NUM-1):
			for j in range(2):
				if options.orbisplanetspar[i][j] != self.orbisplanetspar[i][j]:
					options.orbisplanetspar[i][j] = self.orbisplanetspar[i][j]
					changed = True
		for i in range(chart.Chart.ASPECT_NUM):
			if options.orbisH[i] != self.orbisH[i]:
				options.orbisH[i] = self.orbisH[i]
				changed = True
		for i in range(2):
			if options.orbisparH[i] != self.orbisparH[i]:
				options.orbisparH[i] = self.orbisparH[i]
				changed = True
		for i in range(chart.Chart.ASPECT_NUM):
			if options.orbisAscMC[i] != self.orbisAscMC[i]:
				options.orbisAscMC[i] = self.orbisAscMC[i]
				changed = True
		for i in range(2):
			if options.orbisparAscMC[i] != self.orbisparAscMC[i]:
				options.orbisparAscMC[i] = self.orbisparAscMC[i]
				changed = True

		if options.orbiscuspAscMC != float(self.cuspascmc.GetValue()):
			options.orbiscuspAscMC = float(self.cuspascmc.GetValue())
			changed = True

		if options.orbiscuspH != float(self.cuspinter.GetValue()):
			options.orbiscuspH = float(self.cuspinter.GetValue())
			changed = True

		if options.exact != float(self.exact.GetValue()):
			options.exact = float(self.exact.GetValue())
			changed = True

		for k in self.fixstars.iterkeys():
			if self.fixstars[k] != options.fixstars[k]:
				options.fixstars[k] = self.fixstars[k]
				changed = True

		return changed


