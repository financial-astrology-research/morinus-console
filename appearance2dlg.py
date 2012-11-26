import  wx
import planets
import chart
import mtexts

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class Appearance2Dlg(wx.Dialog):
	def __init__(self, parent):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['Appearance2'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Placidian
		placidian = wx.StaticBox(self, label=mtexts.txts["Placidian"])
		placidiansizer = wx.StaticBoxSizer(placidian, wx.VERTICAL)

		self.longckb = wx.CheckBox(self, -1, mtexts.txts['Longitude'])
		placidiansizer.Add(self.longckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.latckb = wx.CheckBox(self, -1, mtexts.txts['Latitude'])
		placidiansizer.Add(self.latckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.rectascckb = wx.CheckBox(self, -1, mtexts.txts['Rectascension'])
		placidiansizer.Add(self.rectascckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.declckb = wx.CheckBox(self, -1, mtexts.txts['Declination'])
		placidiansizer.Add(self.declckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.ascdifflatckb = wx.CheckBox(self, -1, mtexts.txts['AscDiffLat'])
		placidiansizer.Add(self.ascdifflatckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.semiarcusckb = wx.CheckBox(self, -1, mtexts.txts['Semiarcus'])
		placidiansizer.Add(self.semiarcusckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.meridiandistckb = wx.CheckBox(self, -1, mtexts.txts['Meridiandist'])
		placidiansizer.Add(self.meridiandistckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.horizondistckb = wx.CheckBox(self, -1, mtexts.txts['Horizondist'])
		placidiansizer.Add(self.horizondistckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.temporalhourckb = wx.CheckBox(self, -1, mtexts.txts['TemporalHour'])
		placidiansizer.Add(self.temporalhourckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.hourlydistckb = wx.CheckBox(self, -1, mtexts.txts['HourlyDist'])
		placidiansizer.Add(self.hourlydistckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.pmpckb = wx.CheckBox(self, -1, mtexts.txts['PMP'])
		self.pmpckb.SetHelpText(mtexts.txts['HelpPMP'])
		placidiansizer.Add(self.pmpckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.ascdiffpoleckb = wx.CheckBox(self, -1, mtexts.txts['AscDiffPole'])
		placidiansizer.Add(self.ascdiffpoleckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.poleheightckb = wx.CheckBox(self, -1, mtexts.txts['PoleHeight'])
		placidiansizer.Add(self.poleheightckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.ascdescoblckb = wx.CheckBox(self, -1, mtexts.txts['AscDescObl'])
		placidiansizer.Add(self.ascdescoblckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(placidiansizer, 0, wx.ALIGN_TOP|wx.RIGHT, 5)

		#Regiomontan
		regiomontan = wx.StaticBox(self, label=mtexts.txts["Regiomontan"])
		regiomontansizer = wx.StaticBoxSizer(regiomontan, wx.VERTICAL)

		self.reglongckb = wx.CheckBox(self, -1, mtexts.txts['Longitude'])
		regiomontansizer.Add(self.reglongckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		self.reglatckb = wx.CheckBox(self, -1, mtexts.txts['Latitude'])
		regiomontansizer.Add(self.reglatckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regrectascckb = wx.CheckBox(self, -1, mtexts.txts['Rectascension'])
		regiomontansizer.Add(self.regrectascckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regdeclckb = wx.CheckBox(self, -1, mtexts.txts['Declination'])
		regiomontansizer.Add(self.regdeclckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regmeridiandistckb = wx.CheckBox(self, -1, mtexts.txts['Meridiandist'])
		regiomontansizer.Add(self.regmeridiandistckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.reghorizondistckb = wx.CheckBox(self, -1, mtexts.txts['Horizondist'])
		regiomontansizer.Add(self.reghorizondistckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regzdckb = wx.CheckBox(self, -1, mtexts.txts['ZD'])
		self.regzdckb.SetHelpText(mtexts.txts['HelpZD'])
		regiomontansizer.Add(self.regzdckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regpoleckb = wx.CheckBox(self, -1, mtexts.txts['Pole'])
		regiomontansizer.Add(self.regpoleckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regqckb = wx.CheckBox(self, -1, mtexts.txts['Q'])
		self.regqckb.SetHelpText(mtexts.txts['HelpQ'])
		regiomontansizer.Add(self.regqckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.regwckb = wx.CheckBox(self, -1, mtexts.txts['WReg'])
		self.regwckb.SetHelpText(mtexts.txts['HelpW'])
		regiomontansizer.Add(self.regwckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.cmpckb = wx.CheckBox(self, -1, mtexts.txts['CMP'])
		self.cmpckb.SetHelpText(mtexts.txts['HelpCMP'])
		regiomontansizer.Add(self.cmpckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.rmpckb = wx.CheckBox(self, -1, mtexts.txts['RMP'])
		self.rmpckb.SetHelpText(mtexts.txts['HelpRMP'])
		regiomontansizer.Add(self.rmpckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(regiomontansizer, 1, wx.GROW|wx.RIGHT, 5)

		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		#RA
		ra = wx.StaticBox(self, label=mtexts.txts["Rectascension"])
		rasizer = wx.StaticBoxSizer(ra, wx.VERTICAL)
		self.intimeckb = wx.CheckBox(self, -1, mtexts.txts['InTime'])
		rasizer.Add(self.intimeckb, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		mvsizer.Add(rasizer, 0, wx.GROW|wx.ALIGN_TOP|wx.RIGHT, 5)

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

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()


	def fill(self, options):
		self.longckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LONG]) 
		self.latckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LAT])  
		self.rectascckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.RA])  
		self.declckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.DECL])
		self.ascdifflatckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADLAT])  
		self.semiarcusckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.SA])
		self.meridiandistckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.MD])  
		self.horizondistckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HD])  
		self.temporalhourckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.TH])  
		self.hourlydistckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HOD])  
		self.pmpckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP])  
		self.ascdiffpoleckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADPH])  
		self.poleheightckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.POH])  
		self.ascdescoblckb.SetValue(options.speculums[chart.Chart.PLACIDIAN][planets.Planet.AODO])

		self.reglongckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LONG]) 
		self.reglatckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LAT])  
		self.regrectascckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RA])  
		self.regdeclckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.DECL])
		self.regmeridiandistckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMD])
		self.reghorizondistckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RHD])
		self.regzdckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.ZD])  
		self.regpoleckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.POLE])
		self.regqckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.Q])  
		self.regwckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.W])   
		self.cmpckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP])
		self.rmpckb.SetValue(options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP])

		self.intimeckb.SetValue(options.intime)  


	def check(self, options):
		changed = False

		#Placidian
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LONG] != self.longckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LONG] = self.longckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LAT] != self.latckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.LAT] = self.latckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.RA] != self.rectascckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.RA] = self.rectascckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.DECL] != self.declckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.DECL] = self.declckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADLAT] != self.ascdifflatckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADLAT] = self.ascdifflatckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.SA] != self.semiarcusckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.SA] = self.semiarcusckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.MD] != self.meridiandistckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.MD] = self.meridiandistckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HD] != self.horizondistckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HD] = self.horizondistckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.TH] != self.temporalhourckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.TH] = self.temporalhourckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HOD] != self.hourlydistckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.HOD] = self.hourlydistckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP] != self.pmpckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP] = self.pmpckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADPH] != self.ascdiffpoleckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.ADPH] = self.ascdiffpoleckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.POH] != self.poleheightckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.POH] = self.poleheightckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.PLACIDIAN][planets.Planet.AODO] != self.ascdescoblckb.GetValue():
			options.speculums[chart.Chart.PLACIDIAN][planets.Planet.AODO] = self.ascdescoblckb.GetValue()
			changed = True

		#Regiomontan
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LONG] != self.reglongckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LONG] = self.reglongckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LAT] != self.reglatckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.LAT] = self.reglatckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RA] != self.regrectascckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RA] = self.regrectascckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.DECL] != self.regdeclckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.DECL] = self.regdeclckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMD] != self.regmeridiandistckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMD] = self.regmeridiandistckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RHD] != self.reghorizondistckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RHD] = self.reghorizondistckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.ZD] != self.regzdckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.ZD] = self.regzdckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.POLE] != self.regpoleckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.POLE] = self.regpoleckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.Q] != self.regqckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.Q] = self.regqckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.W] != self.regwckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.W] = self.regwckb.GetValue()
			changed = True
		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP] != self.cmpckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP] = self.cmpckb.GetValue()
			changed = True

		if options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP] != self.rmpckb.GetValue():
			options.speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP] = self.rmpckb.GetValue()
			changed = True

		if options.intime != self.intimeckb.GetValue():
			options.intime = self.intimeckb.GetValue()  
			changed = True

		return changed

