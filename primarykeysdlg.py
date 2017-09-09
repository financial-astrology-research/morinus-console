import  wx
import intvalidator
import primdirs
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class PrimaryKeysDlg(wx.Dialog):
	DEG = 0
	MIN = 1
	SEC = 2

	def __init__(self, parent, options):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PrimaryKeys'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		self.dynsel = options.pdkeyd
		self.statsel = options.pdkeys

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		#Type
		self.stype =wx.StaticBox(self, label=mtexts.txts['Keys'])
		typesizer = wx.StaticBoxSizer(self.stype, wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.dynamicrb = wx.RadioButton(self, -1, mtexts.txts['Dynamic'], style=wx.RB_GROUP)
		hsizer.Add(self.dynamicrb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.staticrb = wx.RadioButton(self, -1, mtexts.txts['Static'])
		hsizer.Add(self.staticrb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		typesizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(typesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		#Selections
		self.svalues =wx.StaticBox(self, label='')
		valuessizer = wx.StaticBoxSizer(self.svalues, wx.VERTICAL)
		typeList = mtexts.typeListDyn
		self.dyn = True
		if not options.pdkeydyn:
			typeList = mtexts.typeListStat
			self.dyn = False

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.cb = wx.ComboBox(self, -1, typeList[0], choices=typeList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		hsizer.Add(self.cb, 1, wx.ALIGN_LEFT|wx.ALL, 5)
		valuessizer.Add(hsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Deg'])
		vsizer.Add(label, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.deg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 9), size=(40,-1))
		vsizer.Add(self.deg, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.deg.SetMaxLength(1)
		hsizer.Add(vsizer, 1, wx.LEFT, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Min'])
		vsizer.Add(label, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		self.minu = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.minu.SetMaxLength(2)
		self.minu.SetHelpText(mtexts.txts['HelpMin'])
		vsizer.Add(self.minu, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		hsizer.Add(vsizer, 1, wx.LEFT, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Sec'])
		vsizer.Add(label, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		self.sec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.sec.SetMaxLength(2)
		self.sec.SetHelpText(mtexts.txts['HelpMin'])
		vsizer.Add(self.sec, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		hsizer.Add(vsizer, 0, wx.LEFT, 5)

		fgsizer = wx.FlexGridSizer(1, 2)
		fgsizer.Add(hsizer, 1, wx.LEFT|wx.ALL, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Coefficient'])
		vsizer.Add(label, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		self.coeff = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
		vsizer.Add(self.coeff, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5)
		fgsizer.Add(vsizer, 0, wx.ALL, 5)
#		fgsizer.AddGrowableCol(1, 0)

		valuessizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		mvsizer.Add(valuessizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		self.sregr =wx.StaticBox(self, label='')
		regrsizer = wx.StaticBoxSizer(self.sregr, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.useregrckb = wx.CheckBox(self, -1, mtexts.txts['UseRegrSun1'])
		vsizer.Add(self.useregrckb, 1, wx.ALIGN_LEFT|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['UseRegrSun2'])
		vsizer.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 2)
		regrsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(regrsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

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

		self.Bind(wx.EVT_RADIOBUTTON, self.dynamicbtn, id=self.dynamicrb.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.staticbtn, id=self.staticrb.GetId())

		self.Bind(wx.EVT_COMBOBOX, self.onselect, id=self.cb.GetId())

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		self.coeff.Enable(False)

		btnOk.SetFocus()


	def staticbtn(self, event):
		self.tostatic()


	def dynamicbtn(self, event):
		self.todynamic()


	def onselect(self, event):
		idx = event.GetSelection()

		if self.staticrb.GetValue():
			self.statsel = idx

			if idx != primdirs.PrimDirs.CUSTOMER and self.deg.IsEnabled():
				if self.deg.GetValue() == '':
					self.custom[PrimaryKeysDlg.DEG] = 0
				else:
					self.custom[PrimaryKeysDlg.DEG] = int(self.deg.GetValue())

				if self.minu.GetValue() == '':
					self.custom[PrimaryKeysDlg.MIN] = 0
				else:
					self.custom[PrimaryKeysDlg.MIN] = int(self.minu.GetValue())

				if self.sec.GetValue() == '':
					self.custom[PrimaryKeysDlg.SEC] = 0
				else:
					self.custom[PrimaryKeysDlg.SEC] = int(self.sec.GetValue())

			customer = False
			if idx == primdirs.PrimDirs.CUSTOMER:
				customer = True

			self.deg.Enable(customer)
			self.minu.Enable(customer)
			self.sec.Enable(customer)
			deg = minu = sec = 0
			coeff = 0.0
			if not customer:
				deg = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.COEFF]
			else:
				deg = self.custom[PrimaryKeysDlg.DEG]
				minu = self.custom[PrimaryKeysDlg.MIN]
				sec = self.custom[PrimaryKeysDlg.SEC]
				val = (deg+minu/60.0+sec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.SetValue(str(deg))
			self.minu.SetValue(str(minu))
			self.sec.SetValue(str(sec))
			self.coeff.SetValue(str(coeff))
		else:
			self.dynsel = idx


	def tostatic(self):
		if self.dyn:
			self.dyn = False
			self.staticrb.SetValue(True)
			self.cb.SetItems(mtexts.typeListStat)
			self.cb.SetStringSelection(mtexts.typeListStat[self.statsel])
			idx = self.statsel

			customer = False
			if idx == primdirs.PrimDirs.CUSTOMER:
				customer = True

			self.deg.Enable(customer)
			self.minu.Enable(customer)
			self.sec.Enable(customer)
			deg = minu = sec = 0
			coeff = 0.0
			if not customer:
				deg = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[idx][primdirs.PrimDirs.COEFF]
			else:
				deg = self.custom[PrimaryKeysDlg.DEG]
				minu = self.custom[PrimaryKeysDlg.MIN]
				sec = self.custom[PrimaryKeysDlg.SEC]
				val = (deg+minu/60.0+sec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.SetValue(str(deg))
			self.minu.SetValue(str(minu))
			self.sec.SetValue(str(sec))
			self.coeff.SetValue(str(coeff))


	def todynamic(self):
		if not self.dyn:
			self.dyn = True
			self.cb.SetItems(mtexts.typeListDyn)
			self.cb.SetStringSelection(mtexts.typeListDyn[self.dynsel])
			if self.statsel == primdirs.PrimDirs.CUSTOMER:
				if self.deg.GetValue() == '':
					self.custom[PrimaryKeysDlg.DEG] = 0
				else:
					self.custom[PrimaryKeysDlg.DEG] = int(self.deg.GetValue())

				if self.minu.GetValue() == '':
					self.custom[PrimaryKeysDlg.MIN] = 0
				else:
					self.custom[PrimaryKeysDlg.MIN] = int(self.minu.GetValue())

				if self.sec.GetValue() == '':
					self.custom[PrimaryKeysDlg.SEC] = 0
				else:
					self.custom[PrimaryKeysDlg.SEC] = int(self.sec.GetValue())

			self.dynamicrb.SetValue(True)
			self.deg.Enable(False)
			self.minu.Enable(False)
			self.sec.Enable(False)
			self.deg.SetValue('')
			self.minu.SetValue('')
			self.sec.SetValue('')
			self.coeff.SetValue('')


	def onOK(self, event):

		doovalidate = False
		if not self.dyn and self.statsel == primdirs.PrimDirs.CUSTOMER:
			doovalidate = True

		validated = False
		if doovalidate:
			if (self.Validate() and self.svalues.Validate()):
				validated = True
		else:
			if self.custom[PrimaryKeysDlg.MIN] <= 59 and self.custom[PrimaryKeysDlg.SEC] <= 59:
				validated = True
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['RangeError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()
				dlgm.Destroy()

		if validated:
			self.Close()
			self.SetReturnCode(wx.ID_OK)


	def fill(self, options):
		if options.pdkeydyn:
			self.cb.SetStringSelection(mtexts.typeListDyn[options.pdkeyd])
		else:
			self.cb.SetStringSelection(mtexts.typeListStat[options.pdkeys])

		if options.pdkeydyn:
			self.dynamicrb.SetValue(True)
			self.deg.Enable(False)
			self.minu.Enable(False)
			self.sec.Enable(False)
			self.deg.SetValue('')
			self.minu.SetValue('')
			self.sec.SetValue('')
			self.coeff.SetValue('')
		else:
			self.staticrb.SetValue(True)

			customer = False
			if not options.pdkeydyn and options.pdkeys == primdirs.PrimDirs.CUSTOMER:
				customer = True

			self.deg.Enable(customer)
			self.minu.Enable(customer)
			self.sec.Enable(customer)
			self.coeff.Enable(False)
			deg = minu = sec = 0
			coeff = 0.0
			if not customer:
				deg = primdirs.PrimDirs.staticData[options.pdkeys][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[options.pdkeys][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[options.pdkeys][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[options.pdkeys][primdirs.PrimDirs.COEFF]
			else:
				deg = options.pdkeydeg
				minu = options.pdkeymin
				sec = options.pdkeysec
				val = (deg+minu/60.0+sec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.SetValue(str(deg))
			self.minu.SetValue(str(minu))
			self.sec.SetValue(str(sec))
			self.coeff.SetValue(str(coeff))

		self.custom = [options.pdkeydeg, options.pdkeymin, options.pdkeysec]
		self.useregrckb.SetValue(options.useregressive)


	def check(self, options):
		changed = False

		#save to options
		if self.dynamicrb.GetValue() != options.pdkeydyn:
			options.pdkeydyn = self.dynamicrb.GetValue()
			changed = True

		if self.dynsel != options.pdkeyd:
			options.pdkeyd = self.dynsel
			changed = True

		if self.statsel != options.pdkeys:
			options.pdkeys = self.statsel
			changed = True

		if not self.dyn and self.statsel == primdirs.PrimDirs.CUSTOMER:
			self.custom[PrimaryKeysDlg.DEG] = int(self.deg.GetValue())
			self.custom[PrimaryKeysDlg.MIN] = int(self.minu.GetValue())
			self.custom[PrimaryKeysDlg.SEC] = int(self.sec.GetValue())

		if self.custom[PrimaryKeysDlg.DEG] != options.pdkeydeg:
			options.pdkeydeg = self.custom[PrimaryKeysDlg.DEG]
			changed = True

		if self.custom[PrimaryKeysDlg.MIN] != options.pdkeymin:
			options.pdkeymin = self.custom[PrimaryKeysDlg.MIN]
			changed = True

		if self.custom[PrimaryKeysDlg.SEC] != options.pdkeysec:
			options.pdkeysec = self.custom[PrimaryKeysDlg.SEC]
			changed = True

		if self.useregrckb.GetValue() != options.useregressive:
			options.useregressive = self.useregrckb.GetValue()
			changed = True

		return changed


