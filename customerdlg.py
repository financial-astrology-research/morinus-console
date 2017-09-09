import wx
import chart
import intvalidator
import mtexts
import util


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class CustomerDlg(wx.Dialog):

	def __init__(self, parent, titletxt):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, titletxt, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		fgsizer = wx.FlexGridSizer(2, 4)

		self.scustomer =wx.StaticBox(self, label='')
		customersizer = wx.StaticBoxSizer(self.scustomer, wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Long']+':')
		fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Deg']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.londeg.SetHelpText(mtexts.txts['HelpPDDeg'])
		self.londeg.SetMaxLength(3)
		vvsizer.Add(self.londeg, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.lonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40, -1))
		self.lonmin.SetHelpText(mtexts.txts['HelpMin'])
		self.lonmin.SetMaxLength(2)
		vvsizer.Add(self.lonmin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.lonsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40, -1))
		self.lonsec.SetHelpText(mtexts.txts['HelpMin'])
		self.lonsec.SetMaxLength(2)
		vvsizer.Add(self.lonsec, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		label = wx.StaticText(self, -1, mtexts.txts['Lat']+':')
		fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Deg']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.latdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 90), size=(40,-1))
		self.latdeg.SetHelpText(mtexts.txts['HelpLatDeg'])
		self.latdeg.SetMaxLength(2)
		vvsizer.Add(self.latdeg, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.latmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40, -1))
		self.latmin.SetHelpText(mtexts.txts['HelpMin'])
		self.latmin.SetMaxLength(2)
		vvsizer.Add(self.latmin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.latsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40, -1))
		self.latsec.SetHelpText(mtexts.txts['HelpMin'])
		self.latsec.SetMaxLength(2)
		vvsizer.Add(self.latsec, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvvsizer = wx.BoxSizer(wx.VERTICAL)
		vvvsizer.Add(fgsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.southernckb = wx.CheckBox(self, -1, mtexts.txts['SouthernLatitude'])
		vvvsizer.Add(self.southernckb, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		customersizer.Add(vvvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(customersizer, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT, 5)

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

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		self.londeg.SetFocus()


	def onOK(self, event):
		if (self.Validate() and self.scustomer.Validate()):
			self.Close()
			self.SetReturnCode(wx.ID_OK)


	def initialize(self, londata, latdata, southern):
		londeg, lonmin, lonsec = str(londata[0]), str(londata[1]), str(londata[2])
		latdeg, latmin, latsec = str(latdata[0]), str(latdata[1]), str(latdata[2])

		self.londeg.SetValue(str(londeg))
		self.lonmin.SetValue(str(lonmin))
		self.lonsec.SetValue(str(lonsec))
		self.latdeg.SetValue(str(latdeg))
		self.latmin.SetValue(str(latmin))
		self.latsec.SetValue(str(latsec))
		
		self.southernckb.SetValue(southern)


	def check(self, londata, latdata, southern):
		changed = False

		if londata[0] != int(self.londeg.GetValue()):
			changed = True
		elif londata[1] != int(self.lonmin.GetValue()):
			changed = True
		elif londata[2] != int(self.lonsec.GetValue()):
			changed = True
		elif latdata[0] != int(self.latdeg.GetValue()):
			changed = True
		elif latdata[1] != int(self.latmin.GetValue()):
			changed = True
		elif latdata[2] != int(self.latsec.GetValue()):
			changed = True
		elif southern != self.southernckb.GetValue():
			changed = True

		return changed





