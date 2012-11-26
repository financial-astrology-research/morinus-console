import sys
import wx
import intvalidator
import chart
import arabicparts
import options
import mtexts
import copy

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class PartsListCtrl(wx.ListCtrl):
	NAME = 0
	FORMULA = 1
	DIURNAL = 2

	DIURNALTXT = u'*'

	MAX_ARABICPARTS_NUM = 40

	def __init__(self, parent, ID, parts, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

		self.partsdata = {}

		self.load(parts)

		self.Populate()
		self.Id = ID
		self.changed = False
		self.removed = False


	def Populate(self):
		self.InsertColumn(PartsListCtrl.NAME, mtexts.txts['Name'])
		self.InsertColumn(PartsListCtrl.FORMULA, mtexts.txts['Formula'])
		self.InsertColumn(PartsListCtrl.DIURNAL, mtexts.txts['Diurnal'], format=wx.LIST_FORMAT_CENTER)

		items = self.partsdata.items()
		for key, data in items:
			index = self.InsertStringItem(sys.maxint, data[0])
			self.SetStringItem(index, PartsListCtrl.NAME, data[0])
			self.SetStringItem(index, PartsListCtrl.FORMULA, data[1])
			self.SetStringItem(index, PartsListCtrl.DIURNAL, data[2])
			self.SetItemData(index, key)

		self.SetColumnWidth(PartsListCtrl.NAME, 160)#wx.LIST_AUTOSIZE)
		self.SetColumnWidth(PartsListCtrl.FORMULA, 140)
		self.SetColumnWidth(PartsListCtrl.DIURNAL, 65)

		self.currentItem = -1
		if len(self.partsdata):
			self.currentItem = 0
			self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)


	def GetListCtrl(self):
		return self


	def getColumnText(self, index, col):
		item = self.GetItem(index, col)
		return item.GetText()


	def OnItemSelected(self, event):
		self.currentItem = event.m_itemIndex
		event.Skip()


	def OnColClick(self,event):
		event.Skip()


	def OnAdd(self, item):
		num = self.GetItemCount()
		if num >= PartsListCtrl.MAX_ARABICPARTS_NUM:
			txt = mtexts.txts['MaxArabicPartsNum']+str(PartsListCtrl.MAX_ARABICPARTS_NUM)+u'!'
			dlgm = wx.MessageDialog(self, txt, '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		if self.checkName(item[PartsListCtrl.NAME]):
			dlgm = wx.MessageDialog(self, mtexts.txts['ArabicPartAlreadyExists'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		if item[PartsListCtrl.NAME] == '':
			dlgm = wx.MessageDialog(self, mtexts.txts['ArabicPartNameEmpty'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		self.InsertStringItem(num, item[PartsListCtrl.NAME])
		for i in range(1, len(item)):
			self.SetStringItem(num, i, item[i])

		self.currentItem = num
		self.EnsureVisible(self.currentItem) #This scrolls the list to the added item at the end
		self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

		self.changed = True


	def checkName(self, name):
		for i in range(self.GetItemCount()):
			if name == self.getColumnText(i, PartsListCtrl.NAME):
				return True

		return False


	def OnRemove(self):
		if self.currentItem != -1:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.DeleteItem(self.currentItem)

				if self.GetItemCount() == 0:
					self.currentItem = -1
				elif self.currentItem >= self.GetItemCount():
					self.currentItem = self.GetItemCount()-1
					self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
				else:
					self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

				self.changed = True
				self.removed = True

			dlg.Destroy()


	def OnRemoveAll(self):
		if self.currentItem != -1:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.DeleteAllItems()
				self.currentItem = -1

				self.changed = True
				self.removed = True

			dlg.Destroy()


	def load(self, parts):
		if parts != None:
			idx = 1
			num = len(parts)
			for i in range(num):
				#Formula to text
				formula = mtexts.partstxts[parts[i][1][0]]+u' + '+mtexts.partstxts[parts[i][1][1]]+u' - '+mtexts.partstxts[parts[i][1][2]]

				#Diurnal
				diurnal = ''
				if parts[i][2]:
					diurnal = PartsListCtrl.DIURNALTXT
				self.partsdata[idx] = (parts[i][0], formula, diurnal)
				idx += 1


	def save(self, opts):
		if self.changed:

			if opts.arabicparts != None:
				del opts.arabicparts
	
			parts = []
			for i in range(self.GetItemCount()):
				name = self.getColumnText(i, PartsListCtrl.NAME)
				form = self.getColumnText(i, PartsListCtrl.FORMULA)
				f1 = self.getFormula(form, 1)
				f2 = self.getFormula(form, 2)
				f3 = self.getFormula(form, 3)
				diurnal = self.getColumnText(i, PartsListCtrl.DIURNAL)
				diur = True
				if diurnal == '':
					diur = False
				
				parts.append((name, (f1, f2, f3), diur))

			#copy to options
			opts.arabicparts = copy.deepcopy(parts)

#			self.changed = False

		return self.changed, self.removed


	def getFormula(self, txt, num):
		if num == 1:
			idx = txt.find(u'+')
			f = txt[0:idx]
		elif num == 2:
			idx = txt.find(u'+')
			idx2 = txt.find(u'-')
			f = txt[idx+1:idx2]
		else:
			idx = txt.find(u'-')
			f = txt[idx+1:]

		#remove whitespaces
		f = f.strip()

		return mtexts.conv[f]
			


class ArabicPartsDlg(wx.Dialog):

	def __init__(self, parent, options):#, inittxt):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['ArabicParts'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		COMBOSIZE = 70

		#AscRef
		self.sascref =wx.StaticBox(self, label='')
		refsizer = wx.StaticBoxSizer(self.sascref, wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Ascendant']+':')
		refsizer.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.refcb = wx.ComboBox(self, -1, mtexts.partsreftxts[0], size=(COMBOSIZE, -1), choices=mtexts.partsreftxts, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.refcb.SetStringSelection(mtexts.partsreftxts[0])
		refsizer.Add(self.refcb, 0, wx.ALL, 5)

		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		vsubsizer.Add(refsizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)

		#DayNight Orb
		self.sorb =wx.StaticBox(self, label=mtexts.txts['DayNightOrb'])
		orbsizer = wx.StaticBoxSizer(self.sorb, wx.HORIZONTAL)
		self.orbdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 6), size=(40,-1))
		self.orbdeg.SetHelpText(mtexts.txts['HelpDayNightOrbDeg'])
		self.orbdeg.SetMaxLength(1)
		orbsizer.Add(self.orbdeg, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		label = wx.StaticText(self, -1, mtexts.txts['Deg'])
		orbsizer.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.orbmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.orbmin.SetHelpText(mtexts.txts['HelpMin'])
		self.orbmin.SetMaxLength(2)
		orbsizer.Add(self.orbmin, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		label = wx.StaticText(self, -1, mtexts.txts['Min'])
		orbsizer.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		vsubsizer.Add(orbsizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)

		#Editor
		self.seditor =wx.StaticBox(self, label='')
		editorsizer = wx.StaticBoxSizer(self.seditor, wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Name']+':')
		editorsizer.Add(label, 0, wx.LEFT, 5)
		self.name = wx.TextCtrl(self, -1, '', size=(200,-1))
		self.name.SetMaxLength(20)
		editorsizer.Add(self.name, 0, wx.ALL, 5)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)

		self.acb = wx.ComboBox(self, -1, mtexts.partstxts[0], size=(COMBOSIZE, -1), choices=mtexts.partstxts, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.acb.SetStringSelection(mtexts.partstxts[0])
		hsizer.Add(self.acb, 0, wx.ALL, 5)
		label = wx.StaticText(self, -1, '+(')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.bcb = wx.ComboBox(self, -1, mtexts.partstxts[0], size=(COMBOSIZE, -1), choices=mtexts.partstxts, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.bcb.SetStringSelection(mtexts.partstxts[0])
		hsizer.Add(self.bcb, 0, wx.ALL, 5)
		label = wx.StaticText(self, -1, '-')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ccb = wx.ComboBox(self, -1, mtexts.partstxts[0], size=(COMBOSIZE, -1), choices=mtexts.partstxts, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ccb.SetStringSelection(mtexts.partstxts[0])
		hsizer.Add(self.ccb, 0, wx.ALL, 5)
		label = wx.StaticText(self, -1, ')')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		editorsizer.Add(hsizer, 0, wx.ALL, 5)
		self.diurnalckb = wx.CheckBox(self, -1, mtexts.txts['Diurnal'])
		editorsizer.Add(self.diurnalckb, 0, wx.ALL, 5)

		vsubsizer.Add(editorsizer, 0, wx.ALIGN_LEFT|wx.RIGHT, 5)

		#buttons
		sbtns =wx.StaticBox(self, label='')
		btnssizer = wx.StaticBoxSizer(sbtns, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		ID_Add = wx.NewId()
		btnAdd = wx.Button(self, ID_Add, mtexts.txts['Add'])
		vsizer.Add(btnAdd, 0, wx.GROW|wx.ALL, 5)
		ID_Remove = wx.NewId()
		btnRemove = wx.Button(self, ID_Remove, mtexts.txts['Remove'])
		vsizer.Add(btnRemove, 0, wx.GROW|wx.ALL, 5)
		ID_RemoveAll = wx.NewId()
		btnRemoveAll = wx.Button(self, ID_RemoveAll, mtexts.txts['RemoveAll'])
		vsizer.Add(btnRemoveAll, 0, wx.GROW|wx.ALL, 5)
		btnssizer.Add(vsizer, 0, wx.GROW|wx.ALL, 5)#
		vsubsizer.Add(btnssizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)

		mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		#parts
		sparts =wx.StaticBox(self, label='')
		partssizer = wx.StaticBoxSizer(sparts, wx.VERTICAL)
		ID_Parts = wx.NewId()
		self.li = PartsListCtrl(self, ID_Parts, options.arabicparts, size=(370,-1), style=wx.LC_VRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL)
		partssizer.Add(self.li, 1, wx.GROW|wx.ALL, 5)

		mhsizer.Add(partssizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 0)
		mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		self.Bind(wx.EVT_BUTTON, self.OnAdd, id=ID_Add)
		self.Bind(wx.EVT_BUTTON, self.OnRemove, id=ID_Remove)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=ID_RemoveAll)

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


	def OnAdd(self, event):
		name = self.name.GetValue()
		formula = mtexts.partstxts[self.acb.GetCurrentSelection()]+u' + '+mtexts.partstxts[self.bcb.GetCurrentSelection()]+u' - '+mtexts.partstxts[self.ccb.GetCurrentSelection()]
		diurnal = ''
		if self.diurnalckb.GetValue():
			diurnal = PartsListCtrl.DIURNALTXT

		item = []
		item.append(name)
		item.append(formula)
		item.append(diurnal)

		self.li.OnAdd(item)


	def OnRemove(self, event):
		self.li.OnRemove()


	def OnRemoveAll(self, event):
		self.li.OnRemoveAll()


	def fill(self, opts):
		self.refcb.SetStringSelection(mtexts.partsreftxts[opts.arabicpartsref])
		self.orbdeg.SetValue(str(opts.daynightorbdeg))
		self.orbmin.SetValue(str(opts.daynightorbmin))


	def check(self, opts):
		changed = False
		removed = False

		if self.refcb.GetCurrentSelection() != opts.arabicpartsref:
			opts.arabicpartsref = self.refcb.GetCurrentSelection()
			changed = True

		if int(self.orbdeg.GetValue()) != opts.daynightorbdeg:
			opts.daynightorbdeg = int(self.orbdeg.GetValue())
			changed = True

		if int(self.orbmin.GetValue()) != opts.daynightorbmin:
			opts.daynightorbmin = int(self.orbmin.GetValue())
			changed = True

		ch, rem = self.li.save(opts)
		if ch:
			changed = True
			if rem:
				removed = True

		return changed, removed





