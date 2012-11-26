import  wx
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class FortuneDlg(wx.Dialog):
	def __init__(self, parent):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['LotOfFortune'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		#Time
		sfortune =wx.StaticBox(self, label='')
		fortunesizer = wx.StaticBoxSizer(sfortune, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.msrb = wx.RadioButton(self, -1, mtexts.txts['LFMoonSun'], style=wx.RB_GROUP)
		vsizer.Add(self.msrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.dsmrb = wx.RadioButton(self, -1, mtexts.txts['LFDSunMoon'])
		vsizer.Add(self.dsmrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		label = wx.StaticText(self, -1, mtexts.txts['LFNMoonSun'])
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		vsubsizer.Add(label, 0, wx.ALIGN_LEFT|wx.LEFT, 22)
		vsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		self.dmsrb = wx.RadioButton(self, -1, mtexts.txts['LFDMoonSun'])
		vsizer.Add(self.dmsrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		label = wx.StaticText(self, -1, mtexts.txts['LFNSunMoon'])
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		vsubsizer.Add(label, 0, wx.ALIGN_LEFT|wx.LEFT, 22)
		vsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.TOP, 2)

#		self.zmprb = wx.RadioButton(self, -1, mtexts.txts['LFZODMP'])
#		self.zmprb.SetHelpText(mtexts.txts['HelpMP'])
#		vsizer.Add(self.zmprb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
#		self.mmprb = wx.RadioButton(self, -1, mtexts.txts['LFMUNMP'])
#		self.mmprb.SetHelpText(mtexts.txts['HelpMP'])
#		vsizer.Add(self.mmprb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		fortunesizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(fortunesizer, 0, wx.GROW|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

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

		btnOk.SetFocus()

		self.ar = (self.msrb, self.dsmrb, self.dmsrb)#, self.zmprb, self.mmprb)


	def fill(self, options):
		self.ar[options.lotoffortune].SetValue(True)


	def check(self, options):
		changed = not self.ar[options.lotoffortune].GetValue()

		if changed:
			for i in range(len(self.ar)):
				if self.ar[i].GetValue():
					options.lotoffortune = i
					break

		return changed





