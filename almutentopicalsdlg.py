import sys
import wx
import intvalidator
import chart
import almutens
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


class RowsListCtrl(wx.ListCtrl):
	TYPE = 0
	VALUE = 1
	RULERSHIP = 2

	MAX_ROW_NUM = 30

	def __init__(self, parent, ID, rows, opts, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

		self.rowsdata = {}

		self.load(rows, opts)

		self.Populate(False)
		self.Id = ID


	def Populate(self, change):
		if not change:
			self.InsertColumn(RowsListCtrl.TYPE, mtexts.txts['Type'])
			self.InsertColumn(RowsListCtrl.VALUE, mtexts.txts['Value'])
			self.InsertColumn(RowsListCtrl.RULERSHIP, mtexts.txts['Rulership'])

		items = self.rowsdata.items()
		for key, data in items:
			index = self.InsertStringItem(sys.maxint, data[0])
			self.SetStringItem(index, RowsListCtrl.TYPE, data[0])
			self.SetStringItem(index, RowsListCtrl.VALUE, data[1])
			self.SetStringItem(index, RowsListCtrl.RULERSHIP, data[2])
			self.SetItemData(index, key)

		self.SetColumnWidth(RowsListCtrl.TYPE, 160)#wx.LIST_AUTOSIZE)
		self.SetColumnWidth(RowsListCtrl.VALUE, 160)
		self.SetColumnWidth(RowsListCtrl.RULERSHIP, 160)

		self.currentItem = -1
		if len(self.rowsdata):
			self.currentItem = 0
			self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

		if not change:
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
		if num >= RowsListCtrl.MAX_ROW_NUM:
			txt = mtexts.txts['MaxRowNum']+str(RowsListCtrl.MAX_ROW_NUM)+u'!'
			dlgm = wx.MessageDialog(self, txt, '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

#		if self.checkRow(item):
#			dlgm = wx.MessageDialog(self, mtexts.txts['RowAlreadyExists'], '', wx.OK|wx.ICON_INFORMATION)
#			dlgm.ShowModal()
#			dlgm.Destroy()#
#			return

		self.InsertStringItem(num, item[RowsListCtrl.TYPE])
		for i in range(1, len(item)):
			self.SetStringItem(num, i, item[i])

		self.currentItem = num
		self.EnsureVisible(self.currentItem) #This scrolls the list to the added item at the end
		self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


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

			dlg.Destroy()


	def OnRemoveAll(self):
		if self.currentItem != -1:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.DeleteAllItems()
				self.currentItem = -1

			dlg.Destroy()


	def clearRows(self):
		self.DeleteAllItems()
		self.currentItem = -1
		self.rowsdata.clear()


	def load(self, rows, opts):
		if rows != None:
			idx = 1
			num = len(rows)
			for i in range(num):
				txt1 = mtexts.topicalTypeList[rows[i][0]]
				txt2 = ''
				if rows[i][0] == almutens.Topicals.PLANET:
					txt2 = mtexts.topicalPlanetsList[rows[i][1]]
				elif rows[i][0] == almutens.Topicals.PLANETS:
					txt2 = mtexts.topicalInHouseList[rows[i][1]]
				elif rows[i][0] == almutens.Topicals.HOUSECUSP:
					txt2 = mtexts.topicalHousesList[rows[i][1]]
				elif rows[i][0] == almutens.Topicals.ARABICPART:
					txt2 = mtexts.txts['LotOfFortune']
					if rows[i][1] > 0:
						apnum = len(opts.arabicparts)
						if rows[i][1] < apnum:
							txt2 = opts.arabicparts[rows[i][1]-1][arabicparts.ArabicParts.NAME]
				elif rows[i][0] == almutens.Topicals.SYZYGY:
					txt2 = mtexts.topicalSyzygyList[rows[i][1]]
				elif rows[i][0] == almutens.Topicals.LIGHTOFTHETIME:
					pass

				txt3 = ''
				if (rows[i][0] != almutens.Topicals.PLANETS):
					txt3 = mtexts.topicalRulershipList[rows[i][2]]

				self.rowsdata[idx] = (txt1, txt2, txt3)
				idx += 1


	def getRows(self, aparts):
		arValuetxts = [mtexts.topicalPlanetsList, mtexts.topicalInHouseList, mtexts.topicalHousesList, aparts, mtexts.topicalSyzygyList, mtexts.topicalLightOfTheTimeList]

		rows = []
		num = self.GetItemCount()
		for i in range(num):
			typtxt = self.getColumnText(i, RowsListCtrl.TYPE)
			typ = 0
			num2 = len(mtexts.topicalTypeList)
			for j in range(num2):
				if typtxt == mtexts.topicalTypeList[j]:
					typ = j
					break

			valtxt = self.getColumnText(i, RowsListCtrl.VALUE)
			val = 0
			num2 = len(arValuetxts[typ])
			for j in range(num2):
				if valtxt == arValuetxts[typ][j]:
					val = j
					break

			rultxt = self.getColumnText(i, RowsListCtrl.RULERSHIP)
			rul = 0
			num2 = len(mtexts.topicalRulershipList)
			for j in range(num2):
				if rultxt == mtexts.topicalRulershipList[j]:
					rul = j
					break

			rows.append((typ, val, rul))

		return tuple(rows[:])


	def checkRow(self, item):
		num = self.GetItemCount()
		for i in range(num):
			typtxt = self.getColumnText(i, RowsListCtrl.TYPE)
			valtxt = self.getColumnText(i, RowsListCtrl.VALUE)
			rultxt = self.getColumnText(i, RowsListCtrl.RULERSHIP)
			if typtxt == item[0] and valtxt == item[1] and rultxt == item[2]:
				return True

		return False


	def fill(self, rows, opts):
		if rows != None:
			self.load(rows, opts)
			
			self.Populate(True)


class AlmutenTopicalsDlg(wx.Dialog):

	MAX_TOPICAL_NUM = 20

	def __init__(self, parent, opts):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['TopicalAlmutens'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		self.tpcls = None
		if opts.topicals != None:
			self.tpcls = copy.deepcopy(opts.topicals)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Topical names
		self.stopicalnames = wx.StaticBox(self, label=mtexts.txts['Almutens'])
		topicalnamessizer = wx.StaticBoxSizer(self.stopicalnames, wx.HORIZONTAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.namestxt = []
		if self.tpcls != None:
			num = len(self.tpcls)
			for i in range(num):
				self.namestxt.append(self.tpcls[i][0])
		self.namescb = wx.ComboBox(self, -1, '', size=(230, -1), choices='', style=wx.CB_DROPDOWN|wx.CB_READONLY)
		hsizer.Add(self.namescb, 0, wx.ALL, 5)
		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		ID_Add = wx.NewId()
		self.btnAdd = wx.Button(self, ID_Add, mtexts.txts['Add'])
		hsubsizer.Add(self.btnAdd, 0, wx.ALL, 5)
		ID_Remove = wx.NewId()
		self.btnRemove = wx.Button(self, ID_Remove, mtexts.txts['Remove'])
		hsubsizer.Add(self.btnRemove, 0, wx.ALL, 5)
		ID_RemoveAll = wx.NewId()
		self.btnRemoveAll = wx.Button(self, ID_RemoveAll, mtexts.txts['RemoveAll'])
		hsubsizer.Add(self.btnRemoveAll, 0, wx.ALL, 5)
		hsizer.Add(hsubsizer, 0, wx.LEFT, 10)
		topicalnamessizer.Add(hsizer, 0, wx.ALL, 5)

		mvsizer.Add(topicalnamessizer, 0, wx.GROW|wx.ALL, 5)

		#editor
		self.seditor = wx.StaticBox(self, label=mtexts.txts['Editor'])
		editorsizer = wx.StaticBoxSizer(self.seditor, wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Name']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.name = wx.TextCtrl(self, -1, '', size=(220,-1))
		self.name.SetHelpText(mtexts.txts['HelpTopicalName'])
		self.name.SetMaxLength(20)
		hsizer.Add(self.name, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		editorsizer.Add(hsizer, 0, wx.ALL, 5)

		COMBOSIZE = 160
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.typecb = wx.ComboBox(self, -1, mtexts.topicalTypeList[0], size=(COMBOSIZE, -1), choices=mtexts.topicalTypeList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.typecb.SetStringSelection(mtexts.topicalTypeList[0])
		hsizer.Add(self.typecb, 0, wx.ALL, 5)
		self.valuecb = wx.ComboBox(self, -1, mtexts.topicalPlanetsList[0], size=(COMBOSIZE, -1), choices=mtexts.topicalPlanetsList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.valuecb.SetStringSelection(mtexts.topicalPlanetsList[0])
		hsizer.Add(self.valuecb, 0, wx.ALL, 5)
		self.rulercb = wx.ComboBox(self, -1, mtexts.topicalRulershipList[0], size=(COMBOSIZE, -1), choices=mtexts.topicalRulershipList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.rulercb.SetStringSelection(mtexts.topicalRulershipList[0])
		hsizer.Add(self.rulercb, 0, wx.ALL, 5)
		editorsizer.Add(hsizer, 0, wx.ALL, 5)

		ID_Rows = wx.NewId()
		rows = None
		if self.tpcls != None:
			self.name.SetValue(self.tpcls[0][0])
			rows = self.tpcls[0][1]
		self.li = RowsListCtrl(self, ID_Rows, rows, opts, size=(3*COMBOSIZE,200), style=wx.LC_VRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL)
		editorsizer.Add(self.li, 0, wx.ALL, 5)

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		ID_AddRow = wx.NewId()
		self.btnAddRow = wx.Button(self, ID_AddRow, mtexts.txts['AddRow'])
		hsizer.Add(self.btnAddRow, 0, wx.ALL, 5)
		ID_RemoveRow = wx.NewId()
		self.btnRemoveRow = wx.Button(self, ID_RemoveRow, mtexts.txts['RemoveRow'])
		hsizer.Add(self.btnRemoveRow, 0, wx.ALL, 5)
		ID_RemoveAllRows = wx.NewId()
		self.btnRemoveAllRows = wx.Button(self, ID_RemoveAllRows, mtexts.txts['RemoveAll'])
		hsizer.Add(self.btnRemoveAllRows, 0, wx.ALL, 5)
		editorsizer.Add(hsizer, 0, wx.ALL, 5)

		mvsizer.Add(editorsizer, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

		self.Bind(wx.EVT_BUTTON, self.OnAdd, id=ID_Add)
		self.Bind(wx.EVT_BUTTON, self.OnRemove, id=ID_Remove)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=ID_RemoveAll)

		self.Bind(wx.EVT_COMBOBOX, self.onType, id=self.typecb.GetId())
		self.Bind(wx.EVT_COMBOBOX, self.onAlmuten, id=self.namescb.GetId())
		self.Bind(wx.EVT_BUTTON, self.OnAddRow, id=ID_AddRow)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveRow, id=ID_RemoveRow)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveAllRows, id=ID_RemoveAllRows)

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

		#Create list of Arabic Part names
		self.aplist = [mtexts.txts['LotOfFortune']]
		if opts.arabicparts != None:
			num = len(opts.arabicparts)
			for i in range(num):
				self.aplist.append(opts.arabicparts[i][arabicparts.ArabicParts.NAME])

		self.options = opts


	def onType(self, event):
		if self.typecb.GetCurrentSelection() == almutens.Topicals.PLANET:
			self.valuecb.SetItems(mtexts.topicalPlanetsList)
			self.valuecb.SetStringSelection(mtexts.topicalPlanetsList[0])
			self.valuecb.Enable(True)
			self.rulercb.Enable(True)
		elif self.typecb.GetCurrentSelection() == almutens.Topicals.PLANETS:
			self.valuecb.SetItems(mtexts.topicalInHouseList)
			self.valuecb.SetStringSelection(mtexts.topicalInHouseList[0])
			self.valuecb.Enable(True)
			self.rulercb.Enable(False)
		elif self.typecb.GetCurrentSelection() == almutens.Topicals.HOUSECUSP:
			self.valuecb.SetItems(mtexts.topicalHousesList)
			self.valuecb.SetStringSelection(mtexts.topicalHousesList[0])
			self.valuecb.Enable(True)
			self.rulercb.Enable(True)
		elif self.typecb.GetCurrentSelection() == almutens.Topicals.ARABICPART:
			self.valuecb.SetItems(self.aplist)
			self.valuecb.SetStringSelection(self.aplist[0])
			self.valuecb.Enable(True)
			self.rulercb.Enable(True)
		elif self.typecb.GetCurrentSelection() == almutens.Topicals.SYZYGY:
			self.valuecb.SetItems(mtexts.topicalSyzygyList)
			self.valuecb.SetStringSelection(mtexts.topicalSyzygyList[0])
			self.valuecb.Enable(True)
			self.rulercb.Enable(True)
		elif self.typecb.GetCurrentSelection() == almutens.Topicals.LIGHTOFTHETIME:
#			self.valuecb.SetItems(mtexts.topicalLightOfTheTimeList)
			li = ('', '')
			self.valuecb.SetItems(li)
			self.valuecb.SetStringSelection('')
			self.valuecb.Enable(False)
			self.rulercb.Enable(True)


	def onAlmuten(self, event):
		idx = self.namescb.GetCurrentSelection()
		name = self.namestxt[idx]
		rows = None
		if self.tpcls != None:
			self.name.SetValue(name)
			rows = self.tpcls[idx][1]
		self.li.clearRows()
		self.li.fill(rows, self.options)


	def OnAdd(self, event):
		num = len(self.namestxt)
		if num >= AlmutenTopicalsDlg.MAX_TOPICAL_NUM:
			txt = mtexts.txts['MaxTopicalNum']+str(RowsListCtrl.MAX_TOPICAL_NUM)+u'!'
			dlgm = wx.MessageDialog(self, mtexts.txts[''], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		if self.name.GetValue() == '':
			dlgm = wx.MessageDialog(self, mtexts.txts['NameIsEmpty'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		name = self.name.GetValue()

		if name in self.namestxt:
			dlgm = wx.MessageDialog(self, mtexts.txts['NameAlreadyExists'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return

		rownum = self.li.GetItemCount()
		if rownum == 0:
			dlgm = wx.MessageDialog(self, mtexts.txts['NoRowsAdded'], '', wx.OK|wx.ICON_INFORMATION)
			dlgm.ShowModal()
			dlgm.Destroy()#
			return
		
		rows = self.li.getRows(self.aplist)
		num = len(rows)
		if num > 0:
			t = (name, rows)
			if self.tpcls != None:
				ar = []
				tnum = len(self.tpcls)
				for i in range(tnum):
					top = (self.tpcls[i][0], self.tpcls[i][1])
					ar.append(top)
				ar.append(t)
				del self.tpcls
				self.tpcls = tuple(ar)
			else:
				ar = []
				ar.append(t)
				self.tpcls = tuple(ar)

			self.namestxt.append(name)
			self.namescb.SetItems(self.namestxt)
			self.namescb.SetStringSelection(self.namestxt[-1])


	def OnRemove(self, event):
		num = len(self.namestxt)
		if num > 0:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				if num > 1:
					idx = self.namescb.GetCurrentSelection()	
					name = self.namestxt[idx]

					ar = []
					tnum = len(self.tpcls)
					for i in range(tnum):
						if self.tpcls[i][0] != name:
							ar.append(self.tpcls[i])

					del self.tpcls
					self.tpcls = tuple(ar)

					del self.namestxt[idx]

					self.namescb.SetItems(self.namestxt)
					self.namescb.SetStringSelection(self.namestxt[0])

					#set name and rows
					self.name.SetValue(self.namestxt[0])
					self.li.clearRows()

					rows = None
					if self.tpcls != None:
						self.name.SetValue(self.namestxt[0])
						rows = self.tpcls[0][1]
					self.li.clearRows()
					self.li.fill(rows, self.options)

				elif num > 0:
					self.namestxt = []
					self.namescb.SetItems('')#self.namestxt)
					self.namescb.SetStringSelection('')
					self.namescb.SetValue('')

					del self.tpcls
					self.tpcls = None

					#clear name and rows
					self.name.SetValue('')
					self.li.clearRows()

			dlg.Destroy()


	def OnRemoveAll(self, event):
		num = len(self.namestxt)
		if num > 0:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.namestxt = []
				self.namescb.SetItems('')#self.namestxt)
				self.namescb.SetStringSelection('')
				self.namescb.SetValue('')

				del self.tpcls
				self.tpcls = None

				#clear name and rows
				self.name.SetValue('')
				self.li.clearRows()

			dlg.Destroy()


	def OnAddRow(self, event):
		typ = self.typecb.GetCurrentSelection()
		val = self.valuecb.GetCurrentSelection()
		rul = self.rulercb.GetCurrentSelection()

		typtxt = mtexts.topicalTypeList[typ]
		valtxt = ''
		rultxt = ''

		if typ == almutens.Topicals.PLANET:
			valtxt = mtexts.topicalPlanetsList[val]
			rultxt = mtexts.topicalRulershipList[rul]
		elif typ == almutens.Topicals.PLANETS:
			valtxt = mtexts.topicalInHouseList[val]
		elif typ == almutens.Topicals.HOUSECUSP:
			valtxt = mtexts.topicalHousesList[val]
			rultxt = mtexts.topicalRulershipList[rul]
		elif typ == almutens.Topicals.ARABICPART:
			valtxt = self.aplist[val]
			rultxt = mtexts.topicalRulershipList[rul]
		elif typ == almutens.Topicals.SYZYGY:
			valtxt = mtexts.topicalSyzygyList[val]
			rultxt = mtexts.topicalRulershipList[rul]
		elif typ == almutens.Topicals.LIGHTOFTHETIME:
			rultxt = mtexts.topicalRulershipList[rul]

		item = [typtxt, valtxt, rultxt]

		self.li.OnAdd(item)


	def OnRemoveRow(self, event):
		self.li.OnRemove()


	def OnRemoveAllRows(self, event):
		self.li.OnRemoveAll()


	def fill(self, opts):
		if len(self.namestxt) > 0:
			self.namescb.SetItems(self.namestxt)
			self.namescb.SetStringSelection(self.namestxt[0])
			self.name.SetValue(self.namestxt[0])


	def check(self, opts):

		changed = False

		if (opts.topicals == None and self.tpcls == None):
			return changed

		if (opts.topicals == None and self.tpcls != None) or (opts.topicals != None and self.tpcls == None):
			changed = True
		elif len(opts.topicals) != len(self.tpcls):
			changed = True
		else:
			changed = opts.topicals != self.tpcls

		if changed:
			if opts.topicals != None:
				del opts.topicals
			opts.topicals = copy.deepcopy(self.tpcls)

		return changed





