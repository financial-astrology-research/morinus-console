import copy
import string
import wx
import chart
import util
import mtexts


class IntValidator(wx.PyValidator):
	def __init__(self, minim=None, maxim=None):
		wx.PyValidator.__init__(self)
		self.minim = minim
		self.maxim = maxim
		self.Bind(wx.EVT_CHAR, self.OnChar)

	def Clone(self):
 		return IntValidator(self.minim, self.maxim)

	def TransferToWindow(self):
		return True

	def TransferFromWindow(self):
		return True

	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()

		if (val == ''):
			dlgm = wx.MessageDialog(None, mtexts.txts['NumFieldsCannotBeEmpty'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()		
			dlgm.Destroy()
			return False

		if ((self.minim != None and int(val) < self.minim) or (self.maxim != None and int(val) >= self.maxim)):
			s = mtexts.txts['RangeError2']
			if (self.maxim != None):
				s = mtexts.txts['RangeError3'] + '%2d' % self.maxim
			dlgm = wx.MessageDialog(None, s, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
			return False	

		return True

	def OnChar(self, event):
		# FIXME: something is wrong with this code, KeyCode
		# behavior has been changed in wxPython 2.8.1?
		#print event, type(event), event.KeyCode
		key = event.KeyCode

		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			event.Skip()
			return

		if chr(key) in string.digits:
			event.Skip()
			return

		if not wx.Validator_IsSilent():
			wx.Bell()


class TermsDlg(wx.Dialog):

	OFFS = 2

	def __init__(self, parent, options):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Terms'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		self.terms = [[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]]]

		self.termsval = copy.deepcopy(options.terms)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		self.cb = wx.ComboBox(self, -1, mtexts.termList[options.selterm], size=(150, -1), choices=mtexts.termList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.cb.SetSelection(options.selterm)
		mvsizer.Add(self.cb, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 5)

		#Terms
		sterms =wx.StaticBox(self, label='')
		termssizer = wx.StaticBoxSizer(sterms, wx.VERTICAL)
		num = len(self.terms)
		subnum = len(self.terms[0])
		gsizer = wx.FlexGridSizer(num, 2, 0, 0)
		for i in range(num):
			label = wx.StaticText(self, -1, mtexts.signs[i]+':')
			gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
			hsizer = wx.BoxSizer(wx.HORIZONTAL)
			for j in range(subnum):
				hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
				self.terms[i][j][0] = wx.ComboBox(self, -1, mtexts.pls2[self.termsval[options.selterm][i][j][0]-TermsDlg.OFFS], size=(90, -1), choices=mtexts.pls2, style=wx.CB_DROPDOWN|wx.CB_READONLY)
				self.terms[i][j][0].SetSelection(self.termsval[options.selterm][i][j][0]-TermsDlg.OFFS)
				hsubsizer.Add(self.terms[i][j][0], 0, wx.ALIGN_LEFT)
				self.terms[i][j][1] = wx.TextCtrl(self, -1, str(self.termsval[options.selterm][i][j][1]), validator=IntValidator(0, 20), size=(30,-1))
				self.terms[i][j][1].SetMaxLength(2)
				hsubsizer.Add(self.terms[i][j][1], 0, wx.ALIGN_LEFT)
				hsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

			gsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		termssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		mvsizer.Add(termssizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

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
		if (self.Validate()):
			#save the old and display the new
			num = len(self.terms)
			subnum = len(self.terms[0])
			for i in range(num):
				for j in range(subnum):
					self.termsval[oldidx][i][j][0] = self.terms[i][j][0].GetCurrentSelection()+TermsDlg.OFFS
					self.termsval[oldidx][i][j][1] = int(self.terms[i][j][1].GetValue())

					self.terms[i][j][0].SetSelection(self.termsval[idx][i][j][0]-TermsDlg.OFFS)
					self.terms[i][j][1].SetValue(str(self.termsval[idx][i][j][1]))
		else:
			self.cb.SetSelection(oldidx)


	def onOK(self, event):
		if (self.Validate()):
			#check multiplanetselections, 30deg
			num = len(self.terms)
			subnum = len(self.terms[0])
			curridx = self.cb.GetCurrentSelection()
			#save
			for i in range(num):
				for j in range(subnum):
					self.termsval[curridx][i][j][0] = self.terms[i][j][0].GetCurrentSelection()+TermsDlg.OFFS
					self.termsval[curridx][i][j][1] = int(self.terms[i][j][1].GetValue())

			#check
			typnum = len(mtexts.termList)
			OK = 0
			MULTIPLANETS = 1
			NOT30 = 2
			errcode = OK
			for typ in range(typnum):
				for i in range(num):
					summa = 0
					pls = [False, False, False, False, False, False, False]
					for j in range(subnum):
						if not pls[self.termsval[typ][i][j][0]]:
							pls[self.termsval[typ][i][j][0]] = True
						else:
							errcode = 1
							summa = chart.Chart.SIGN_DEG
							break
						summa += self.termsval[typ][i][j][1]

					if summa != chart.Chart.SIGN_DEG:
						errcode = 2
					if errcode != 0:
						break
				if errcode != 0:
					break

			if errcode == OK:
				self.Close()
				self.SetReturnCode(wx.ID_OK)
			else:
				txt = mtexts.txts['MultiPlanets']+'('+mtexts.termList[typ]+','+mtexts.signs[i]+')'
				if errcode == NOT30:
					txt = mtexts.txts['NOT30']+'('+mtexts.termList[typ]+','+mtexts.signs[i]+')'
				dlgm = wx.MessageDialog(None, txt, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()
				dlgm.Destroy()


	def check(self, options):
		changed = False

		if options.selterm != self.cb.GetCurrentSelection():
			options.selterm = self.cb.GetCurrentSelection()
			changed = True

		typnum = len(mtexts.termList)
		num = len(self.terms)
		subnum = len(self.terms[0])
		for typ in range(typnum):
			for i in range(num):
				for j in range(subnum):
					if self.termsval[typ][i][j][0] != options.terms[typ][i][j][0] or self.termsval[typ][i][j][1] != options.terms[typ][i][j][1]:
						options.terms[typ][i][j][0] = self.termsval[typ][i][j][0] 
						options.terms[typ][i][j][1] = self.termsval[typ][i][j][1] 
						changed = True
						
		return changed






