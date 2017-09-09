import copy
import wx
import chart
import mtexts


class DecansDlg(wx.Dialog):

	def __init__(self, parent, options):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Decans'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		self.decans = [[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None]]

		self.decansval = copy.deepcopy(options.decans)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		self.cb = wx.ComboBox(self, -1, mtexts.decanList[options.seldecan], size=(150, -1), choices=mtexts.decanList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.cb.SetSelection(options.seldecan)
		mvsizer.Add(self.cb, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 5)

		sdecans =wx.StaticBox(self, label='')
		decanssizer = wx.StaticBoxSizer(sdecans, wx.VERTICAL)
		num = len(self.decans)
		subnum = len(self.decans[0])
		gsizer = wx.FlexGridSizer(num, 2, 0, 0)
		for i in range(num):
			label = wx.StaticText(self, -1, mtexts.signs[i]+':')
			gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
			hsizer = wx.BoxSizer(wx.HORIZONTAL)
			for j in range(subnum):
				self.decans[i][j] = wx.ComboBox(self, -1, mtexts.pls[self.decansval[options.seldecan][i][j]], size=(90, -1), choices=mtexts.pls, style=wx.CB_DROPDOWN|wx.CB_READONLY)
				self.decans[i][j].SetSelection(self.decansval[options.seldecan][i][j])
				hsizer.Add(self.decans[i][j], 0, wx.ALIGN_LEFT|wx.ALL, 5)

			gsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		decanssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		mvsizer.Add(decanssizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

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

		self.Bind(wx.EVT_COMBOBOX, self.onSelect, id=self.cb.GetId())
		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		btnOk.SetFocus()


	def onSelect(self, event):
		idx = event.GetSelection()
		oldidx = 0
		if idx == 0:
			oldidx = 1
		#save the old and display the new
		num = len(self.decans)
		subnum = len(self.decans[0])
		for i in range(num):
			for j in range(subnum):
				self.decansval[oldidx][i][j] = self.decans[i][j].GetCurrentSelection()

				self.decans[i][j].SetSelection(self.decansval[idx][i][j])


	def onOK(self, event):
		num = len(self.decans)
		subnum = len(self.decans[0])
		curridx = self.cb.GetCurrentSelection()
		#save
		for i in range(num):
			for j in range(subnum):
				self.decansval[curridx][i][j] = self.decans[i][j].GetCurrentSelection()

		self.Close()
		self.SetReturnCode(wx.ID_OK)


	def check(self, options):
		changed = False

		if options.seldecan != self.cb.GetCurrentSelection():
			options.seldecan = self.cb.GetCurrentSelection()
			changed = True

		typnum = len(mtexts.decanList)

		num = len(self.decans)
		subnum = len(self.decans[0])
		for typ in range(typnum):
			for i in range(num):
				for j in range(subnum):
					if self.decansval[typ][i][j] != options.decans[typ][i][j]:
						options.decans[typ][i][j] = self.decansval[typ][i][j] 
						changed = True
						
		return changed






