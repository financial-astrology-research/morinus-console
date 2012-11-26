import  wx
import copy
import planets
import chart
import mtexts


class DignitiesDlg(wx.Dialog):

	def __init__(self, parent, options):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Dignities'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		self.parent = parent
		self.options = options

		self.dignities = copy.deepcopy(self.options.dignities)

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

		self.dombaseid = wx.NewId()
		self.ID_Domicile = self.dombaseid
		self.ID_Exaltatio = wx.NewId()

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Planets
		splanets =wx.StaticBox(self, label='')
		splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
		self.sunrb = wx.RadioButton(self, self.ID_Sun, mtexts.txts['Sun'], style=wx.RB_GROUP)
		splanetssizer.Add(self.sunrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.moonrb = wx.RadioButton(self, self.ID_Moon, mtexts.txts['Moon'])
		splanetssizer.Add(self.moonrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.mercuryrb = wx.RadioButton(self, self.ID_Mercury, mtexts.txts['Mercury'])
		splanetssizer.Add(self.mercuryrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.venusrb = wx.RadioButton(self, self.ID_Venus, mtexts.txts['Venus'])
		splanetssizer.Add(self.venusrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.marsrb = wx.RadioButton(self, self.ID_Mars, mtexts.txts['Mars'])
		splanetssizer.Add(self.marsrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.jupiterrb = wx.RadioButton(self, self.ID_Jupiter, mtexts.txts['Jupiter'])
		splanetssizer.Add(self.jupiterrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.saturnusrb = wx.RadioButton(self, self.ID_Saturnus, mtexts.txts['Saturn'])
		splanetssizer.Add(self.saturnusrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.uranusrb = wx.RadioButton(self, self.ID_Uranus, mtexts.txts['Uranus'])
		splanetssizer.Add(self.uranusrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.neptunerb = wx.RadioButton(self, self.ID_Neptune, mtexts.txts['Neptune'])
		splanetssizer.Add(self.neptunerb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.plutorb = wx.RadioButton(self, self.ID_Pluto, mtexts.txts['Pluto'])
		splanetssizer.Add(self.plutorb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(splanetssizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)

		#Domicile
		sdomicile =wx.StaticBox(self, label='')
		sdomicilesizer = wx.StaticBoxSizer(sdomicile, wx.VERTICAL)
		self.domicilerb = wx.RadioButton(self, self.ID_Domicile, mtexts.txts['Domicil'], style=wx.RB_GROUP)
		sdomicilesizer.Add(self.domicilerb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.exaltatiorb = wx.RadioButton(self, self.ID_Exaltatio, mtexts.txts['Exal'])
		sdomicilesizer.Add(self.exaltatiorb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(sdomicilesizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)

		#Signs
		self.arsigns = []
		ssigns =wx.StaticBox(self, label='')
		ssignssizer = wx.StaticBoxSizer(ssigns, wx.VERTICAL)
		for i in range(chart.Chart.SIGN_NUM):
			ckb = wx.CheckBox(self, -1, mtexts.signs[i])
			self.arsigns.append(ckb)
			ssignssizer.Add(ckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		mhsizer.Add(ssignssizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)

		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

		btnsizer = wx.StdDialogButtonSizer()

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()

		self.sunrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.moonrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.mercuryrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.venusrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.marsrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.jupiterrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.saturnusrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.uranusrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.neptunerb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
		self.plutorb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)

		self.plid = self.ID_Sun-self.baseid

		self.domicilerb.Bind(wx.EVT_RADIOBUTTON, self.onDomicile)
		self.exaltatiorb.Bind(wx.EVT_RADIOBUTTON, self.onDomicile)

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		self.domid = self.ID_Domicile-self.dombaseid

		#Load
		self.sunrb.SetValue(True)
		self.domicilerb.SetValue(True)
		for i in range(chart.Chart.SIGN_NUM):
			self.arsigns[i].SetValue(self.dignities[self.plid][0][i])


	def onBtn(self, event):
		rid = event.GetId()-self.baseid
		
		if rid == self.plid:
			return

		#save
		for i in range(chart.Chart.SIGN_NUM):
			self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()

		#Load
		for i in range(chart.Chart.SIGN_NUM):
			self.arsigns[i].SetValue(self.dignities[rid][self.domid][i])

		self.plid = rid


	def onDomicile(self, event):
		rid = event.GetId()-self.dombaseid
		
		if rid == self.domid:
			return

		#save
		for i in range(chart.Chart.SIGN_NUM):
			self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()

		#Load
		for i in range(chart.Chart.SIGN_NUM):
			self.arsigns[i].SetValue(self.dignities[self.plid][rid][i])

		self.domid = rid


	def onOK(self, event):
		#Save currently selected
		for i in range(chart.Chart.SIGN_NUM):
			self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()
		
		self.Close()
		self.SetReturnCode(wx.ID_OK)


	def check(self, options):
		changed = False

		NODES = 2
		for i in range(planets.Planets.PLANETS_NUM-NODES):
			for d in range(2):
				for s in range(chart.Chart.SIGN_NUM):
					if options.dignities[i][d][s] != self.dignities[i][d][s]:
						options.dignities[i][d][s] = self.dignities[i][d][s]
						changed = True

		return changed


