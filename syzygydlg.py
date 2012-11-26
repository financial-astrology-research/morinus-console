import wx
import planets
import chart
import options
import mtexts

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class SyzygyDlg(wx.Dialog):
	def __init__(self, parent):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['Syzygy'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		#Syzygy
		ssyzygy = wx.StaticBox(self, label="")
		syzygysizer = wx.StaticBoxSizer(ssyzygy, wx.VERTICAL)
		self.syzmoonrb = wx.RadioButton(self, -1, mtexts.txts['SyzMoon'], style=wx.RB_GROUP)
		syzygysizer.Add(self.syzmoonrb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		self.syzaboverb = wx.RadioButton(self, -1, mtexts.txts['SyzAbove'])
		syzygysizer.Add(self.syzaboverb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		self.syzabovenatalrb = wx.RadioButton(self, -1, mtexts.txts['SyzAboveNatal'])
		syzygysizer.Add(self.syzabovenatalrb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		mvsizer.Add(syzygysizer, 0, wx.GROW|wx.ALL, 5)

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


	def fill(self, opts):
		if opts.syzmoon == options.Options.MOON:
			self.syzmoonrb.SetValue(True)
		elif opts.syzmoon == options.Options.ABOVEHOR:
			self.syzaboverb.SetValue(True)
		else:
			self.syzabovenatalrb.SetValue(True)


	def check(self, opts):
		changed = False

		if opts.syzmoon != options.Options.MOON and self.syzmoonrb.GetValue():
			opts.syzmoon = options.Options.MOON
			changed = True
		elif opts.syzmoon != options.Options.ABOVEHOR and self.syzaboverb.GetValue():
			opts.syzmoon = options.Options.ABOVEHOR
			changed = True
		elif opts.syzmoon != options.Options.ABOVEHORNATAL and self.syzabovenatalrb.GetValue():
			opts.syzmoon = options.Options.ABOVEHORNATAL
			changed = True

		return changed

