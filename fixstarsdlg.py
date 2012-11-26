# -*- coding: utf-8 -*-

import sys
import os
import wx
import limchecklistctrlmixin
import chart
import mtexts
import astrology
import util

#import pdb

class FixStars:
	signtxts = (mtexts.txts['Ari'], mtexts.txts['Tau'], mtexts.txts['Gem'], mtexts.txts['Can'], mtexts.txts['Leo'], mtexts.txts['Vir'], mtexts.txts['Lib'], mtexts.txts['Sco'], mtexts.txts['Sag'], mtexts.txts['Cap'], mtexts.txts['Aqu'], mtexts.txts['Pis'])

	class FixStar:
		NAME = 0
		NOMNAME = 1
		LON = 2
		LAT = 3

		def __init__(self, name, nomname, lon, lat):
			self.name = name
			self.nomname = nomname
			self.lon = lon
			self.lat = lat
		
	COMMENT = '#'

	def __init__(self, ephepath):
		self.ephepath = ephepath
		self.jd = astrology.swe_julday(1950, 1, 1, 0.0, astrology.SE_GREG_CAL)	
		self.data = []

		self.fname = os.path.join(self.ephepath, 'fixstars.cat')


	def read(self):
		res = True

		try:
			f = open(self.fname, 'r')
			lines = f.readlines()
			f.close()

			#Count non-comment lines
			cnt = 0
			for ln in lines:
				if ln[0] == FixStars.COMMENT and ln.find('example') != -1:
					break

				if ln[0] != FixStars.COMMENT:
					cnt += 1

			for i in range(1, cnt+1):
				ret, name, dat, serr = astrology.swe_fixstar_ut(str(i), self.jd, 0)
				d, m, s = util.decToDeg(dat[0])
				sign = d/chart.Chart.SIGN_DEG
				lon = d%chart.Chart.SIGN_DEG
				lontxt = str(lon)+FixStars.signtxts[sign]+' '+(str(m)).zfill(2)+"' "+(str(s)).zfill(2)+'"'
				d, m, s = util.decToDeg(dat[1])
				si = ''
				if dat[1] < 0.0:
					si = '-'
				lattxt = si+str(d)+' '+(str(m)).zfill(2)+"' "+(str(s)).zfill(2)+'"'

				nam = name[0].strip()
				nomnam = ''
				DELIMITER = ','
				if nam.find(DELIMITER) != -1:
					snam = nam.split(DELIMITER)
					nam = snam[0].strip()
					nomnam = snam[1].strip()
					
				self.data.append(FixStars.FixStar(nam, nomnam, lontxt, lattxt))

		except IOError:
			res = False
			pass

		return res


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
	LON = 3
	LAT = 4
	COLNUM = LAT+1

	MAX_SEL_NUM = 40

	def __init__(self, parent, ephepath, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		limchecklistctrlmixin.LimCheckListCtrlMixin.__init__(self, FixStarListCtrl.MAX_SEL_NUM)

		self.parent = parent
		self.fixstardata = {}
		self.ephepath = ephepath
		self.Id = ID
		self.changed = False

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)


	def fill(self, names):
		wx.WindowDisabler()

		self.initchecking = True
		wx.BeginBusyCursor()
		self.load()
		self.Populate()

		nset = set()
		items = self.fixstardata.iteritems()
		for k, v in items:
			for nomname in names.iterkeys():
				if v[1] == nomname and nomname not in nset:
					if len(nset) >= FixStarListCtrl.MAX_SEL_NUM:
						break

					self.CheckItem(k-1)
					nset.add(nomname)
					
		wx.EndBusyCursor()
		self.initchecking = False


	def Populate(self):
		self.InsertColumn(FixStarListCtrl.NUM, '')
		self.InsertColumn(FixStarListCtrl.NAME, mtexts.txts['Name'])
		self.InsertColumn(FixStarListCtrl.NOMNAME, mtexts.txts['Nomencl']+'.')
		self.InsertColumn(FixStarListCtrl.LON, mtexts.txts['Long']+'.')
		self.InsertColumn(FixStarListCtrl.LAT, mtexts.txts['Lat']+'.')

		items = self.fixstardata.items()
		cnt = 0
		for key, data in items:
			cnt += 1
			index = self.InsertStringItem(sys.maxint, data[0])
			self.SetStringItem(index, FixStarListCtrl.NUM, str(cnt)+'.')
			self.SetStringItem(index, FixStarListCtrl.NAME, data[0])
			self.SetStringItem(index, FixStarListCtrl.NOMNAME, data[1])
			self.SetStringItem(index, FixStarListCtrl.LON, data[2])
			self.SetStringItem(index, FixStarListCtrl.LAT, data[3])
			self.SetItemData(index, key)

		self.SetColumnWidth(FixStarListCtrl.NUM, 60)
		self.SetColumnWidth(FixStarListCtrl.NAME, 120)
		self.SetColumnWidth(FixStarListCtrl.NOMNAME, 80)
		self.SetColumnWidth(FixStarListCtrl.LON, 105)
		self.SetColumnWidth(FixStarListCtrl.LAT, 80)


	def OnItemActivated(self, evt):
		self.ToggleItem(evt.m_itemIndex)


	def OnCheckItem(self, index, flag):
#		data = self.GetItemData(index)

		if not self.initchecking:
			self.parent.changeNum(flag)


	def OnDeselectAll(self):
		self.initchecking = True
		items = self.fixstardata.iteritems()
		for k, v in items:
			if self.IsChecked(k-1):
				self.CheckItem(k-1, False)

		self.initchecking = False


	def load(self):
		fs = FixStars(self.ephepath)
		if fs.read():
			idx = 1
			for f in fs.data:
				self.fixstardata[idx] = (f.name, f.nomname, f.lon, f.lat)
				idx += 1
		else:
			txt = mtexts.txts['FileError']+'('+fs.fname+')'
			dlgm = wx.MessageDialog(self, txt, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()


class FixStarsDlg(wx.Dialog):
	def __init__(self, parent, names, ephepath):#, inittxt):
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
		label = wx.StaticText(self, -1, mtexts.txts['FixStarRef']+':')
		starssizer.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		ID_FixStars = wx.NewId()
		self.li = FixStarListCtrl(self, ephepath, ID_FixStars, size=(470,340))
		starssizer.Add(self.li, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.li.fill(names)

		fgsizer = wx.FlexGridSizer(1, 2)
		ID_DeselectAll = wx.NewId()
		btnDeselectAll = wx.Button(self, ID_DeselectAll, mtexts.txts['DeselectAll'])
		fgsizer.Add(btnDeselectAll, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['LeftToSelect']+':')
		hsubsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.val = wx.TextCtrl(self, -1, '', size=(40, -1), style=wx.TE_READONLY)
		num = FixStarListCtrl.MAX_SEL_NUM-len(names)
		self.num = num
		self.val.SetValue(str(num))
#		self.val.Enable(False)
		hsubsizer.Add(self.val, 0, wx.RIGHT|wx.ALL, 5)
		fgsizer.Add(hsubsizer, 0, wx.LEFT, 100)

		starssizer.Add(fgsizer, 0)
		mvsizer.Add(starssizer, 0, wx.LEFT|wx.RIGHT, 5)

		#Search
		self.search =wx.StaticBox(self, label=mtexts.txts['Search'])
		searchsizer = wx.StaticBoxSizer(self.search, wx.VERTICAL)

		fgsizer = wx.FlexGridSizer(1, 2)
		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Name']+':')
		hsubsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.searchname = wx.TextCtrl(self, -1, '', size=(150, -1))
		self.searchname.SetMaxLength(20)
		hsubsizer.Add(self.searchname, 0, wx.RIGHT|wx.ALL, 5)
		fgsizer.Add(hsubsizer, 0, wx.LEFT)
		hsubsizer2 = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Nomencl']+':')
		hsubsizer2.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.searchnomname = wx.TextCtrl(self, -1, '', size=(150, -1))
		self.searchnomname.SetMaxLength(20)
		hsubsizer2.Add(self.searchnomname, 0, wx.RIGHT|wx.ALL, 5)
		fgsizer.Add(hsubsizer2, 0, wx.LEFT, 20)

		searchsizer.Add(fgsizer, 0)
		mvsizer.Add(searchsizer, 0, wx.LEFT|wx.RIGHT, 5)

#		self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
		self.searchname.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
		self.searchnomname.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

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

		self.rowrect = self.li.GetItemRect(0)
		self.li.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


	def OnDeselectAll(self, event):
		self.li.OnDeselectAll()
		self.num = FixStarListCtrl.MAX_SEL_NUM
		self.val.SetValue(str(self.num))


	def OnKeyUp(self, evnt):
		nametxt = self.searchname.GetValue()
		nomnametxt = self.searchnomname.GetValue()
		#Remove whitespace (from both ends)
		nametxt = (nametxt.strip()).lower()
		nomnametxt = (nomnametxt.strip()).lower()

		if (self.searchname == self.FindFocus() and not self.isAccepted(nametxt)) or (self.searchnomname == self.FindFocus() and not self.isAccepted(nomnametxt)):
			return

		spos = self.li.GetScrollPos(wx.VERTICAL)
		if ((self.searchname == self.FindFocus() and nametxt != '') or (self.searchnomname == self.FindFocus() and nomnametxt != '')): #Are they active?
			#find item
			length = len(self.li.fixstardata)
			for i in range(1, length):
				if (self.searchname == self.FindFocus() and nametxt != '' and nametxt in (self.li.fixstardata[i][0]).lower()) or (self.searchnomname == self.FindFocus() and nomnametxt != '' and nomnametxt in (self.li.fixstardata[i][1]).lower()):
					break

			self.li.ScrollList(0, -spos*self.rowrect.height)
			self.li.ScrollList(0, (i-1)*self.rowrect.height)
			self.li.SetItemState(i-1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


	def isAccepted(self, txt):
		for i in range(len(txt)):
			if not txt[i].isalnum():
				if txt[i] != ' ' and txt[i] != '-':
					return False

		return True


	def changeNum(self, selected):
		if selected:
			self.num -= 1
		else:
			self.num += 1

		self.val.SetValue(str(self.num))


	def check(self, names):
		changed = False

		self.selnames = []
		items = self.li.fixstardata.iteritems()
		for k, v in items:
			if self.li.IsChecked(k-1):
				self.selnames.append(v[1])

		selnamesnum = len(self.selnames)
		namesnum = len(names)

		if selnamesnum != namesnum:
			changed = True
		else:
			for i in range(selnamesnum):
				if self.selnames[i] not in names:
					changed = True
					break

		if changed:
			names.clear()
			for i in range(selnamesnum):
				names[self.selnames[i]] = chart.Chart.def_fixstarsorb

		return changed






