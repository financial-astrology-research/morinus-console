import wx
import astrology
import chart
import mtexts


class ColorsDlg(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Colors'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#In Chart
		schart = wx.StaticBox(self, label=mtexts.txts["Chart"])
		chartsizer = wx.StaticBoxSizer(schart, wx.VERTICAL)
		gsizer = wx.GridSizer(5, 2)
		ID_BTN_Frame = wx.NewId()
		self.baseid = ID_BTN_Frame
		label = wx.StaticText(self, -1, mtexts.txts['Frame']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnFrame = wx.Button(self, ID_BTN_Frame, '', size=(60, -1))
		gsizer.Add(self.btnFrame, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Signs = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Signs']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSigns = wx.Button(self, ID_BTN_Signs, '', size=(60, -1))
		gsizer.Add(self.btnSigns, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_AscMC = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['AscMC']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnAscMC = wx.Button(self, ID_BTN_AscMC, '', size=(60, -1))
		gsizer.Add(self.btnAscMC, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Houses = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Houses']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnHouses = wx.Button(self, ID_BTN_Houses, '', size=(60, -1))
		gsizer.Add(self.btnHouses, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_HouseNumbers = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Housenames']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnHouseNumbers = wx.Button(self, ID_BTN_HouseNumbers, '', size=(60, -1))
		gsizer.Add(self.btnHouseNumbers, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['Positions']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		ID_BTN_Positions = wx.NewId()
		self.btnPositions = wx.Button(self, ID_BTN_Positions, '', size=(60, -1))
		gsizer.Add(self.btnPositions, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		chartsizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(chartsizer, 1, wx.GROW|wx.TOP, 5)

		#Dignities
		dignities = wx.StaticBox(self, label=mtexts.txts["Dignities"])
		digsizer = wx.StaticBoxSizer(dignities, wx.VERTICAL)
		gsizer = wx.GridSizer(5, 2)

		self.digtxts = []

		ID_BTN_Domicil = wx.NewId()
		self.digtxts.append(wx.StaticText(self, -1, mtexts.txts['Domicil']+':'))
		gsizer.Add(self.digtxts[0], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnDomicil = wx.Button(self, ID_BTN_Domicil, '', size=(60, -1))
		gsizer.Add(self.btnDomicil, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Exal = wx.NewId()
		self.digtxts.append(wx.StaticText(self, -1, mtexts.txts['Exal']+':'))
		gsizer.Add(self.digtxts[1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnExal = wx.Button(self, ID_BTN_Exal, '', size=(60, -1))
		gsizer.Add(self.btnExal, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Peregrin = wx.NewId()
		self.digtxts.append(wx.StaticText(self, -1, mtexts.txts['Peregrin']+':'))
		gsizer.Add(self.digtxts[2], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnPeregrin = wx.Button(self, ID_BTN_Peregrin, '', size=(60, -1))
		gsizer.Add(self.btnPeregrin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Casus = wx.NewId()
		self.digtxts.append(wx.StaticText(self, -1, mtexts.txts['Casus']+':'))
		gsizer.Add(self.digtxts[3], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnCasus = wx.Button(self, ID_BTN_Casus, '', size=(60, -1))
		gsizer.Add(self.btnCasus, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Exil = wx.NewId()
		self.digtxts.append(wx.StaticText(self, -1, mtexts.txts['Exil']+':'))
		gsizer.Add(self.digtxts[4], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnExil = wx.Button(self, ID_BTN_Exil, '', size=(60, -1))
		gsizer.Add(self.btnExil, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		digsizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 2)
		vsizer.Add(digsizer, 0, wx.GROW|wx.TOP, 5)
		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)

		#Individuals
		planetsbox = wx.StaticBox(self, label=mtexts.txts["Individual"])
		planetssizer = wx.StaticBoxSizer(planetsbox, wx.VERTICAL)
		gsizer = wx.GridSizer(10, 2)

		self.pltxts = []

		ID_BTN_Sun = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Sun']+':'))
		gsizer.Add(self.pltxts[0], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSun = wx.Button(self, ID_BTN_Sun, '', size=(60, -1))
		gsizer.Add(self.btnSun, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Moon = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Moon']+':'))
		gsizer.Add(self.pltxts[1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnMoon = wx.Button(self, ID_BTN_Moon, '', size=(60, -1))
		gsizer.Add(self.btnMoon, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Mercury = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Mercury']+':'))
		gsizer.Add(self.pltxts[2], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnMercury = wx.Button(self, ID_BTN_Mercury, '', size=(60, -1))
		gsizer.Add(self.btnMercury, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Venus = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Venus']+':'))
		gsizer.Add(self.pltxts[3], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnVenus = wx.Button(self, ID_BTN_Venus, '', size=(60, -1))
		gsizer.Add(self.btnVenus, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Mars = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Mars']+':'))
		gsizer.Add(self.pltxts[4], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnMars = wx.Button(self, ID_BTN_Mars, '', size=(60, -1))
		gsizer.Add(self.btnMars, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Jupiter = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Jupiter']+':'))
		gsizer.Add(self.pltxts[5], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnJupiter = wx.Button(self, ID_BTN_Jupiter, '', size=(60, -1))
		gsizer.Add(self.btnJupiter, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Saturn = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Saturn']+':'))
		gsizer.Add(self.pltxts[6], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSaturn = wx.Button(self, ID_BTN_Saturn, '', size=(60, -1))
		gsizer.Add(self.btnSaturn, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Uranus = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Uranus']+':'))
		gsizer.Add(self.pltxts[7], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnUranus = wx.Button(self, ID_BTN_Uranus, '', size=(60, -1))
		gsizer.Add(self.btnUranus, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Neptune = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Neptune']+':'))
		gsizer.Add(self.pltxts[8], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnNeptune = wx.Button(self, ID_BTN_Neptune, '', size=(60, -1))
		gsizer.Add(self.btnNeptune, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Pluto = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Pluto']+':'))
		gsizer.Add(self.pltxts[9], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnPluto = wx.Button(self, ID_BTN_Pluto, '', size=(60, -1))
		gsizer.Add(self.btnPluto, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_Nodes = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['Nodes']+':'))
		gsizer.Add(self.pltxts[10], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnNodes = wx.Button(self, ID_BTN_Nodes, '', size=(60, -1))
		gsizer.Add(self.btnNodes, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		ID_BTN_LoF = wx.NewId()
		self.pltxts.append(wx.StaticText(self, -1, mtexts.txts['LoF']+':'))
		gsizer.Add(self.pltxts[11], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnLoF = wx.Button(self, ID_BTN_LoF, '', size=(60, -1))
		gsizer.Add(self.btnLoF, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		planetssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(planetssizer, 1, wx.GROW|wx.TOP, 5)
		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)

		#Aspects
		aspects = wx.StaticBox(self, label=mtexts.txts["Aspects"])
		aspectsizer = wx.StaticBoxSizer(aspects, wx.VERTICAL)
		gsizer = wx.GridSizer(11, 2)
		ID_BTN_Conjunctio = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Conjunctio']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnConjunctio = wx.Button(self, ID_BTN_Conjunctio, '', size=(60, -1))
		gsizer.Add(self.btnConjunctio, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Semisextil = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Semisextil']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSemisextil = wx.Button(self, ID_BTN_Semisextil, '', size=(60, -1))
		gsizer.Add(self.btnSemisextil, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Semiquadrat = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Semiquadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSemiquadrat = wx.Button(self, ID_BTN_Semiquadrat, '', size=(60, -1))
		gsizer.Add(self.btnSemiquadrat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Sextil = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Sextil']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSextil = wx.Button(self, ID_BTN_Sextil, '', size=(60, -1))
		gsizer.Add(self.btnSextil, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Quintile = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Quintile']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnQuintile = wx.Button(self, ID_BTN_Quintile, '', size=(60, -1))
		gsizer.Add(self.btnQuintile, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Quadrat = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Quadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnQuadrat = wx.Button(self, ID_BTN_Quadrat, '', size=(60, -1))
		gsizer.Add(self.btnQuadrat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Trigon = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Trigon']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnTrigon = wx.Button(self, ID_BTN_Trigon, '', size=(60, -1))
		gsizer.Add(self.btnTrigon, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Sesquiquadrat = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Sesquiquadrat']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnSesquiquadrat = wx.Button(self, ID_BTN_Sesquiquadrat, '', size=(60, -1))
		gsizer.Add(self.btnSesquiquadrat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Biquintile = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Biquintile']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnBiquintile = wx.Button(self, ID_BTN_Biquintile, '', size=(60, -1))
		gsizer.Add(self.btnBiquintile, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Quinqunx = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Quinqunx']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnQuinqunx = wx.Button(self, ID_BTN_Quinqunx, '', size=(60, -1))
		gsizer.Add(self.btnQuinqunx, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
		ID_BTN_Oppositio = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Oppositio']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnOppositio = wx.Button(self, ID_BTN_Oppositio, '', size=(60, -1))
		gsizer.Add(self.btnOppositio, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		aspectsizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(aspectsizer, 1, wx.GROW|wx.TOP, 5)
		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		#General
		general = wx.StaticBox(self, label=mtexts.txts["General"])
		horsizer = wx.StaticBoxSizer(general, wx.HORIZONTAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		ID_BTN_Background = wx.NewId()
		label = wx.StaticText(self, -1, mtexts.txts['Background']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnBackground = wx.Button(self, ID_BTN_Background, '', size=(60, -1))
		hsizer.Add(self.btnBackground, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)

		horsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		ID_BTN_Table = wx.NewId()
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Table']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnTable = wx.Button(self, ID_BTN_Table, '', size=(60, -1))
		hsizer.Add(self.btnTable, 0, wx.ALIGN_RIGHT|wx.ALL, 2)

		horsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)

		ID_BTN_Texts = wx.NewId()
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Texts']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.btnTexts = wx.Button(self, ID_BTN_Texts, '', size=(60, -1))
		hsizer.Add(self.btnTexts, 0, wx.ALIGN_RIGHT|wx.ALL, 2)

		horsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.useplanetcolorsckb = wx.CheckBox(self, -1, mtexts.txts['UseIndividual'])
		self.Bind(wx.EVT_CHECKBOX, self.onUsePlanetColors, id=self.useplanetcolorsckb.GetId())
		hsizer.Add(self.useplanetcolorsckb, 0, wx.ALIGN_RIGHT|wx.ALL, 2)

		horsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)

		mvsizer.Add(horsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.arBtn = [self.btnFrame, self.btnSigns, self.btnAscMC, self.btnHouses, self.btnHouseNumbers, self.btnPositions, self.btnDomicil, self.btnExal, self.btnPeregrin, self.btnCasus, self.btnExil, self.btnSun, self.btnMoon, self.btnMercury, self.btnVenus, self.btnMars, self.btnJupiter, self.btnSaturn, self.btnUranus, self.btnNeptune, self.btnPluto, self.btnNodes, self.btnLoF, self.btnConjunctio, self.btnSemisextil, self.btnSemiquadrat, self.btnSextil, self.btnQuintile, self.btnQuadrat, self.btnTrigon, self.btnSesquiquadrat, self.btnBiquintile, self.btnQuinqunx, self.btnOppositio, self.btnBackground, self.btnTable, self.btnTexts]

		wx.EVT_BUTTON(self, ID_BTN_Frame, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Signs, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_AscMC, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Houses, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_HouseNumbers, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Positions, self.onBtn)

		wx.EVT_BUTTON(self, ID_BTN_Domicil, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Exal, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Peregrin, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Casus, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Exil, self.onBtn)

		wx.EVT_BUTTON(self, ID_BTN_Sun, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Moon, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Mercury, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Venus, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Mars, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Jupiter, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Saturn, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Uranus, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Neptune, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Pluto, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Nodes, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_LoF, self.onBtn)

		wx.EVT_BUTTON(self, ID_BTN_Conjunctio, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Semisextil, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Semiquadrat, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Sextil, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Quintile, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Quadrat, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Trigon, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Sesquiquadrat, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Biquintile, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Quinqunx, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Oppositio, self.onBtn)

		wx.EVT_BUTTON(self, ID_BTN_Background, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Table, self.onBtn)
		wx.EVT_BUTTON(self, ID_BTN_Texts, self.onBtn)

		btnsizer = wx.StdDialogButtonSizer()

		okbtn = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		okbtn.SetDefault()
		btnsizer.AddButton(okbtn)

		cancelbtn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(cancelbtn)
		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		okbtn.SetFocus()


	def onBtn(self, event):
		btnid = event.GetId()-self.baseid
		data = wx.ColourData()
		data.SetChooseFull(True)
		data.SetColour((self.arBtn[btnid].GetBackgroundColour()))
		dlg = wx.ColourDialog(self, data)

		if dlg.ShowModal() == wx.ID_OK:
			data = dlg.GetColourData()
			self.arBtn[btnid].SetBackgroundColour(data.GetColour())

		dlg.Destroy()


	def onUsePlanetColors(self, event):
		self.changeState(self.useplanetcolorsckb.GetValue())


	def changeState(self, enable):
		arplanets = [self.btnSun, self.btnMoon, self.btnMercury, self.btnVenus, self.btnMars, self.btnJupiter, self.btnSaturn, self.btnUranus, self.btnNeptune, self.btnPluto, self.btnNodes, self.btnLoF]
		ardignities = [self.btnDomicil, self.btnExal, self.btnPeregrin, self.btnCasus, self.btnExil]

		for it in self.pltxts:
			it.Enable(enable)

		for it in arplanets:
			it.Enable(enable)

		for it in self.digtxts:
			it.Enable(not enable)

		for it in ardignities:
			it.Enable(not enable)


	def fill(self, options):
		self.btnFrame.SetBackgroundColour(options.clrframe)
		self.btnSigns.SetBackgroundColour(options.clrsigns)
		self.btnAscMC.SetBackgroundColour(options.clrAscMC)
		self.btnHouses.SetBackgroundColour(options.clrhouses)
		self.btnHouseNumbers.SetBackgroundColour(options.clrhousenumbers)
		self.btnPositions.SetBackgroundColour(options.clrpositions)

		self.btnPeregrin.SetBackgroundColour(options.clrperegrin)
		self.btnDomicil.SetBackgroundColour(options.clrdomicil)
		self.btnExil.SetBackgroundColour(options.clrexil)
		self.btnExal.SetBackgroundColour(options.clrexal)
		self.btnCasus.SetBackgroundColour(options.clrcasus)

		self.btnSun.SetBackgroundColour(options.clrindividual[astrology.SE_SUN])
		self.btnMoon.SetBackgroundColour(options.clrindividual[astrology.SE_MOON])
		self.btnMercury.SetBackgroundColour(options.clrindividual[astrology.SE_MERCURY])
		self.btnVenus.SetBackgroundColour(options.clrindividual[astrology.SE_VENUS])
		self.btnMars.SetBackgroundColour(options.clrindividual[astrology.SE_MARS])
		self.btnJupiter.SetBackgroundColour(options.clrindividual[astrology.SE_JUPITER])
		self.btnSaturn.SetBackgroundColour(options.clrindividual[astrology.SE_SATURN])
		self.btnUranus.SetBackgroundColour(options.clrindividual[astrology.SE_URANUS])
		self.btnNeptune.SetBackgroundColour(options.clrindividual[astrology.SE_NEPTUNE])
		self.btnPluto.SetBackgroundColour(options.clrindividual[astrology.SE_PLUTO])
		self.btnNodes.SetBackgroundColour(options.clrindividual[astrology.SE_PLUTO+1])
		self.btnLoF.SetBackgroundColour(options.clrindividual[astrology.SE_PLUTO+2])

		self.btnConjunctio.SetBackgroundColour(options.clraspect[chart.Chart.CONJUNCTIO])
		self.btnSemisextil.SetBackgroundColour(options.clraspect[chart.Chart.SEMISEXTIL])
		self.btnSemiquadrat.SetBackgroundColour(options.clraspect[chart.Chart.SEMIQUADRAT])
		self.btnSextil.SetBackgroundColour(options.clraspect[chart.Chart.SEXTIL])
		self.btnQuintile.SetBackgroundColour(options.clraspect[chart.Chart.QUINTILE])
		self.btnQuadrat.SetBackgroundColour(options.clraspect[chart.Chart.QUADRAT])
		self.btnTrigon.SetBackgroundColour(options.clraspect[chart.Chart.TRIGON])
		self.btnSesquiquadrat.SetBackgroundColour(options.clraspect[chart.Chart.SESQUIQUADRAT])
		self.btnBiquintile.SetBackgroundColour(options.clraspect[chart.Chart.BIQUINTILE])
		self.btnQuinqunx.SetBackgroundColour(options.clraspect[chart.Chart.QUINQUNX])
		self.btnOppositio.SetBackgroundColour(options.clraspect[chart.Chart.OPPOSITIO])

		self.btnBackground.SetBackgroundColour(options.clrbackground)
		self.btnTable.SetBackgroundColour(options.clrtable)
		self.btnTexts.SetBackgroundColour(options.clrtexts)

		self.useplanetcolorsckb.SetValue(options.useplanetcolors)

		self.changeState(self.useplanetcolorsckb.GetValue())


	def check(self, options):
		changed = False

		if options.clrframe != self.btnFrame.GetBackgroundColour().Get(False):
			options.clrframe = self.btnFrame.GetBackgroundColour().Get(False)
			changed = True
		if options.clrsigns != self.btnSigns.GetBackgroundColour().Get(False):
			options.clrsigns = self.btnSigns.GetBackgroundColour().Get(False)
			changed = True
		if options.clrAscMC != self.btnAscMC.GetBackgroundColour().Get(False):
			options.clrAscMC = self.btnAscMC.GetBackgroundColour().Get(False)
			changed = True
		if options.clrhouses != self.btnHouses.GetBackgroundColour().Get(False):
			options.clrhouses = self.btnHouses.GetBackgroundColour().Get(False)
			changed = True
		if options.clrhousenumbers != self.btnHouseNumbers.GetBackgroundColour().Get(False):
			options.clrhousenumbers = self.btnHouseNumbers.GetBackgroundColour().Get(False)
			changed = True
		if options.clrpositions != self.btnPositions.GetBackgroundColour().Get(False):
			options.clrpositions = self.btnPositions.GetBackgroundColour().Get(False)
			changed = True

		if options.clrperegrin != self.btnPeregrin.GetBackgroundColour().Get(False):
			options.clrperegrin = self.btnPeregrin.GetBackgroundColour().Get(False)
			changed = True
		if options.clrdomicil != self.btnDomicil.GetBackgroundColour().Get(False):
			options.clrdomicil = self.btnDomicil.GetBackgroundColour().Get(False)
			changed = True
		if options.clrexil != self.btnExil.GetBackgroundColour().Get(False):
			options.clrexil = self.btnExil.GetBackgroundColour().Get(False)
			changed = True
		if options.clrexal != self.btnExal.GetBackgroundColour().Get(False):
			options.clrexal = self.btnExal.GetBackgroundColour().Get(False)
			changed = True
		if options.clrcasus != self.btnCasus.GetBackgroundColour().Get(False):
			options.clrcasus = self.btnCasus.GetBackgroundColour().Get(False)
			changed = True

		if options.clrindividual[astrology.SE_SUN] != self.btnSun.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_SUN] = self.btnSun.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_MOON] != self.btnMoon.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_MOON] = self.btnMoon.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_MERCURY] != self.btnMercury.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_MERCURY] = self.btnMercury.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_VENUS] != self.btnVenus.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_VENUS] = self.btnVenus.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_MARS] != self.btnMars.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_MARS] = self.btnMars.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_JUPITER] != self.btnJupiter.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_JUPITER] = self.btnJupiter.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_SATURN] != self.btnSaturn.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_SATURN] = self.btnSaturn.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_URANUS] != self.btnUranus.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_URANUS] = self.btnUranus.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_NEPTUNE] != self.btnNeptune.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_NEPTUNE] = self.btnNeptune.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_PLUTO] != self.btnPluto.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_PLUTO] = self.btnPluto.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_PLUTO+1] != self.btnNodes.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_PLUTO+1] = self.btnNodes.GetBackgroundColour().Get(False)
			changed = True
		if options.clrindividual[astrology.SE_PLUTO+2] != self.btnLoF.GetBackgroundColour().Get(False):
			options.clrindividual[astrology.SE_PLUTO+2] = self.btnLoF.GetBackgroundColour().Get(False)
			changed = True

		if options.clraspect[chart.Chart.CONJUNCTIO] != self.btnConjunctio.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.CONJUNCTIO] = self.btnConjunctio.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.SEMISEXTIL] != self.btnSemisextil.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.SEMISEXTIL] = self.btnSemisextil.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.SEMIQUADRAT] != self.btnSemiquadrat.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.SEMIQUADRAT] = self.btnSemiquadrat.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.SEXTIL] != self.btnSextil.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.SEXTIL] = self.btnSextil.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.QUINTILE] != self.btnQuintile.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.QUINTILE] = self.btnQuintile.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.QUADRAT] != self.btnQuadrat.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.QUADRAT] = self.btnQuadrat.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.TRIGON] != self.btnTrigon.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.TRIGON] = self.btnTrigon.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.SESQUIQUADRAT] != self.btnSesquiquadrat.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.SESQUIQUADRAT] = self.btnSesquiquadrat.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.BIQUINTILE] != self.btnBiquintile.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.BIQUINTILE] = self.btnBiquintile.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.QUINQUNX] != self.btnQuinqunx.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.QUINQUNX] = self.btnQuinqunx.GetBackgroundColour().Get(False)
			changed = True
		if options.clraspect[chart.Chart.OPPOSITIO] != self.btnOppositio.GetBackgroundColour().Get(False):
			options.clraspect[chart.Chart.OPPOSITIO] = self.btnOppositio.GetBackgroundColour().Get(False)
			changed = True

		if options.clrbackground != self.btnBackground.GetBackgroundColour().Get(False):
			options.clrbackground = self.btnBackground.GetBackgroundColour().Get(False)
			changed = True
		if options.clrtable != self.btnTable.GetBackgroundColour().Get(False):
			options.clrtable = self.btnTable.GetBackgroundColour().Get(False)
			changed = True
		if options.clrtexts != self.btnTexts.GetBackgroundColour().Get(False):
			options.clrtexts = self.btnTexts.GetBackgroundColour().Get(False)
			changed = True

		if options.useplanetcolors != self.useplanetcolorsckb.GetValue():
			options.useplanetcolors = self.useplanetcolorsckb.GetValue()
			changed = True

		return changed

