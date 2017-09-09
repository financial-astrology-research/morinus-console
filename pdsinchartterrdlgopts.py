import wx
import chart
import mtexts
import util


class PDsInChartsTerrDlgOpts(wx.Dialog):

	def __init__(self, parent):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
#		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PDsInChart'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#SecMotion
		ssecmotion = wx.StaticBox(self, label='')
		secmotionsizer = wx.StaticBoxSizer(ssecmotion, wx.VERTICAL)
		self.secondaryckb = wx.CheckBox(self, -1, mtexts.txts['SecondaryMotion'])
		secmotionsizer.Add(self.secondaryckb, 0, wx.ALL, 5)
#		self.secondaryckb.Enable(False)

		mvsizer.Add(secmotionsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

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


	def fill(self, opts):
		self.secondaryckb.SetValue(opts.pdinchartterrsecmotion)


	def check(self, opts):
		changed = False

		if opts.pdinchartterrsecmotion != self.secondaryckb.GetValue():
			opts.pdinchartterrsecmotion = self.secondaryckb.GetValue()
			changed = True

		return changed



