import wx
import mtexts


class LanguagesDlg(wx.Dialog):
	def __init__(self, parent, langid):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Languages'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		self.langcb = wx.ComboBox(self, -1, mtexts.langtexts[0], size=(100, -1), choices=mtexts.langtexts, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.langcb.SetStringSelection(mtexts.langtexts[langid])
		mvsizer.Add(self.langcb, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 20)

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

		btnOk.SetFocus()


	def check(self, options):
		changed = False

		selid = self.langcb.GetCurrentSelection()
		if options.langid != selid:
			options.langid = selid
			changed = True

		return changed





