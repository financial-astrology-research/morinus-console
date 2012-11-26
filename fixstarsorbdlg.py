import  wx
import astrology
import floatvalidator
import chart
import fixstars
import util
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class FixStarsOrbDlg(wx.Dialog):
	def __init__(self, parent, fixstrs):

		self.fixstars = fixstrs.copy()
		self.prevselection = 0

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['Orbis'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		#Orbs
		sorbs =wx.StaticBox(self, label='')
		orbssizer = wx.StaticBoxSizer(sorbs, wx.HORIZONTAL)
		self.fsnames = self.fixstars.keys()
		self.fscb = wx.ComboBox(self, -1, self.fsnames[0], size=(100, -1), choices=self.fsnames, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		orbssizer.Add(self.fscb, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.fsorbstxt = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, 6.0), size=(50, -1))
		self.fsorbstxt.SetValue(str(self.fixstars[self.fsnames[0]]))
		orbssizer.Add(self.fsorbstxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		mvsizer.Add(orbssizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		sallorbs =wx.StaticBox(self, label='')
		allorbssizer = wx.StaticBoxSizer(sallorbs, wx.HORIZONTAL)
		ID_All = wx.NewId()
		self.btnAll = wx.Button(self, ID_All, mtexts.txts['All'])
		allorbssizer.Add(self.btnAll, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.maxval = 6.0
		self.fsorbtxt = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, self.maxval), size=(50, -1))
		self.fsorbtxt.SetValue(str(chart.Chart.def_fixstarsorb))
		allorbssizer.Add(self.fsorbtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		mvsizer.Add(allorbssizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

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

		self.Bind(wx.EVT_COMBOBOX, self.onSelect, id=self.fscb.GetId())
		self.Bind(wx.EVT_BUTTON, self.onAll, id=ID_All)
		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		btnOk.SetFocus()


	def onOK(self, event):
		if (self.Validate()):
			self.fixstars[self.fsnames[self.prevselection]] = float(self.fsorbstxt.GetValue())

			self.Close()
			self.SetReturnCode(wx.ID_OK)


	def onSelect(self, evnt):
		if float(self.fsorbstxt.GetValue()) >= self.maxval:
			s = mtexts.txts['RangeError3'] + '%2.1f' % self.maxval
			dlgm = wx.MessageDialog(None, s, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
		else:
			self.fixstars[self.fsnames[self.prevselection]] = float(self.fsorbstxt.GetValue())

		idx = evnt.GetSelection()
		self.fsorbstxt.SetValue(str(self.fixstars[self.fsnames[idx]]))

		self.prevselection = idx


	def onAll(self, evnt):
		if float(self.fsorbtxt.GetValue()) >= self.maxval:
			s = mtexts.txts['RangeError3'] + '%2.1f' % self.maxval
			dlgm = wx.MessageDialog(None, s, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
			return

		dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
		val = dlg.ShowModal()
		if val == wx.ID_YES:
			for name in self.fsnames:
				self.fixstars[name] = float(self.fsorbtxt.GetValue())

			self.fsorbstxt.SetValue(str(float(self.fsorbtxt.GetValue())))

		self.fsorbtxt.SetValue(str(float(self.fsorbtxt.GetValue())))

		dlg.Destroy()


	def getFixstars(self):
		return self.fixstars.copy()







