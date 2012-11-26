# -*- coding: utf-8 -*-

import sys
import os
import wx
import limchecklistctrlmixin
import chart
import mtexts
import astrology
import util


class FixStars:
	class FixStar:
		NAME = 0
		NOMNAME = 1

		def __init__(self, name, nomname):
			self.name = name
			self.nomname = nomname
		

	def __init__(self, ephepath):
		self.ephepath = ephepath
		self.jd = astrology.swe_julday(1950, 1, 1, 0.0, astrology.SE_GREG_CAL)	
		self.data = []

		self.fname = os.path.join(self.ephepath, 'fixstars.cat')


	def read(self, names):
		for n in names:
			ret, name, dat, serr = astrology.swe_fixstar_ut(','+n, self.jd, 0)
			nam = name[0].strip()
			nomnam = ''
			DELIMITER = ','
			if nam.find(DELIMITER) != -1:
				snam = nam.split(DELIMITER)
				nam = snam[0].strip()
				nomnam = snam[1].strip()
				
			self.data.append(FixStars.FixStar(nam, nomnam))

		return True #!?


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class FixStarListCtrl(wx.ListCtrl, limchecklistctrlmixin.LimCheckListCtrlMixin):
	NUM = 0
	NAME = 1
	NOMNAME = 2

	MAX_SEL_NUM = 40

	def __init__(self, parent, ephepath, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		limchecklistctrlmixin.LimCheckListCtrlMixin.__init__(self, FixStarListCtrl.MAX_SEL_NUM)

		self.parent = parent
		self.ephepath = ephepath
		self.fixstardata = {}
		self.Id = ID

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)


	def fill(self, names, sels):
		wx.WindowDisabler()

		wx.BeginBusyCursor()
		self.load(names)
		self.Populate()

		items = self.fixstardata.iteritems()
		for k, v in items:
			for i in range(len(sels)):
				if sels[i]:
					self.CheckItem(i)
					
		wx.EndBusyCursor()


	def Populate(self):
		self.InsertColumn(FixStarListCtrl.NUM, '')
		self.InsertColumn(FixStarListCtrl.NAME, mtexts.txts['Name'])
		self.InsertColumn(FixStarListCtrl.NOMNAME, mtexts.txts['Nomencl']+'.')

		items = self.fixstardata.items()
		cnt = 0
		for key, data in items:
			cnt += 1
			index = self.InsertStringItem(sys.maxint, data[0])
			self.SetStringItem(index, FixStarListCtrl.NUM, str(cnt)+'.')
			self.SetStringItem(index, FixStarListCtrl.NAME, data[0])
			self.SetStringItem(index, FixStarListCtrl.NOMNAME, data[1])
			self.SetItemData(index, key)

		self.SetColumnWidth(FixStarListCtrl.NUM, 50)
		self.SetColumnWidth(FixStarListCtrl.NAME, 120)
		self.SetColumnWidth(FixStarListCtrl.NOMNAME, 80)


	def OnItemActivated(self, evt):
		self.ToggleItem(evt.m_itemIndex)


#	def OnCheckItem(self, index, flag):
#		data = self.GetItemData(index)


	def OnDeselectAll(self):
		items = self.fixstardata.iteritems()
		for k, v in items:
			if self.IsChecked(k-1):
				self.CheckItem(k-1, False)


	def OnSelectAll(self):
		items = self.fixstardata.iteritems()
		for k, v in items:
			if not self.IsChecked(k-1):
				self.CheckItem(k-1, True)


	def load(self, names):
		fs = FixStars(self.ephepath)
		if fs.read(names):
			idx = 1
			for f in fs.data:
				self.fixstardata[idx] = (f.name, f.nomname)
				idx += 1
		else:
			txt = mtexts.txts['FileError']+'('+fs.fname+')'
			dlgm = wx.MessageDialog(self, txt, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()


class FixStarsPDDlg(wx.Dialog):
	def __init__(self, parent, options, pdfixstarssel, ephepath):#, inittxt):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['FixStars'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		self.sstars =wx.StaticBox(self, label='')
		starssizer = wx.StaticBoxSizer(self.sstars, wx.VERTICAL)

		ID_FixStars = wx.NewId()
		self.li = FixStarListCtrl(self, ephepath, ID_FixStars, size=(275,280))
		starssizer.Add(self.li, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.li.fill(options.fixstars, pdfixstarssel)

		hbtnsizer = wx.BoxSizer(wx.HORIZONTAL)
		ID_SelectAll = wx.NewId()
		btnSelectAll = wx.Button(self, ID_SelectAll, mtexts.txts['SelectAll'])
		hbtnsizer.Add(btnSelectAll, 0)

		ID_DeselectAll = wx.NewId()
		btnDeselectAll = wx.Button(self, ID_DeselectAll, mtexts.txts['DeselectAll'])
		hbtnsizer.Add(btnDeselectAll, 0)

		starssizer.Add(hbtnsizer, 0)
		mvsizer.Add(starssizer, 0, wx.LEFT|wx.RIGHT, 5)

		self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=ID_SelectAll)
		self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=ID_DeselectAll)

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

		btnOk.SetFocus()


	def OnDeselectAll(self, event):
		self.li.OnDeselectAll()


	def OnSelectAll(self, event):
		self.li.OnSelectAll()


	def getSelections(self):
		sels = []
		keys = self.li.fixstardata.iterkeys()
		for k in keys:
			sels.append(self.li.IsChecked(k-1))

		return sels[:]




