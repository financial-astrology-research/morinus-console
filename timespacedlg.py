import  wx
import datetime
import chart
import intvalidator
import rangechecker
import placesdlg
import mtexts
import util


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class TimeSpaceDlg(wx.Dialog):

	PLUSCHOICES = (u'+', u'-')

	def __init__(self, parent, title, langid):
		self.langid = langid

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Time
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000
		self.stime =wx.StaticBox(self, label='')
		timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.timeckb = wx.CheckBox(self, -1, mtexts.txts['BC'])
		vsizer.Add(self.timeckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5)

		fgsizer = wx.FlexGridSizer(2, 3)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.yearlabel = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vvsizer.Add(self.yearlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vvsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.monthlabel = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vvsizer.Add(self.monthlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)
		vvsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.daylabel = wx.StaticText(self, -1, mtexts.txts['Day']+':')
		vvsizer.Add(self.daylabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.day.SetHelpText(mtexts.txts['HelpDay'])
		self.day.SetMaxLength(2)
		vvsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.hourlabel = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vvsizer.Add(self.hourlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,-1))
		self.hour.SetHelpText(mtexts.txts['HelpHour'])
		self.hour.SetMaxLength(2)
		vvsizer.Add(self.hour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.minlabel = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(self.minlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.minute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.minute.SetHelpText(mtexts.txts['HelpMin'])
		self.minute.SetMaxLength(2)
		vvsizer.Add(self.minute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.seclabel = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vvsizer.Add(self.seclabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.sec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.sec.SetHelpText(mtexts.txts['HelpMin'])
		self.sec.SetMaxLength(2)
		vvsizer.Add(self.sec, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)
		timesizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		vvsubsizer = wx.BoxSizer(wx.VERTICAL)
		vvsubsizer.Add(timesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)###

		#Place
		fgsizer = wx.FlexGridSizer(2, 4)
		vsizer = wx.BoxSizer(wx.VERTICAL)

		self.splace =wx.StaticBox(self, label='')
		placesizer = wx.StaticBoxSizer(self.splace, wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Long']+':')
		fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Deg']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 180), size=(40,-1))
		self.londeg.SetHelpText(mtexts.txts['HelpLonDeg'])
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
		self.placerbE = wx.RadioButton(self, -1, mtexts.txts['E'], style=wx.RB_GROUP)
		vvsizer.Add(self.placerbE, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		self.placerbW = wx.RadioButton(self, -1, mtexts.txts['W'])
		vvsizer.Add(self.placerbW, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
#		fgsizer.AddGrowableCol(4, 0)

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
		self.placerbN = wx.RadioButton(self, -1, mtexts.txts['N'], style=wx.RB_GROUP)
		vvsizer.Add(self.placerbN, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		self.placerbS = wx.RadioButton(self, -1, mtexts.txts['S'])
		vvsizer.Add(self.placerbS, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		ID_PlaceButton = wx.NewId()
		placebtn = wx.Button(self, ID_PlaceButton, mtexts.txts['Place']+':', size=(100, -1))
		vsizer.Add(placebtn, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
		self.birthplace = wx.TextCtrl(self, -1, '', size=(170,-1))
		self.birthplace.SetHelpText(mtexts.txts['HelpPlace'])
		self.birthplace.SetMaxLength(20)
		vsizer.Add(self.birthplace, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		placesizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		vvsubsizer.Add(placesizer, 0, wx.ALIGN_LEFT|wx.RIGHT, 5)
		mhsizer.Add(vvsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		#Zone
		self.szone =wx.StaticBox(self, label='')
		zonesizer = wx.StaticBoxSizer(self.szone, wx.VERTICAL)
		self.calcb = wx.ComboBox(self, -1, mtexts.calList[0], size=(100, -1), choices=mtexts.calList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		zonesizer.Add(self.calcb, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)
		self.zonecb = wx.ComboBox(self, -1, mtexts.zoneList[0], size=(100, -1), choices=mtexts.zoneList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		zonesizer.Add(self.zonecb, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)
#		self.zonecb.SetHelpText(mtexts.txts['zone-time')
		hhsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.gmtlabel = wx.StaticText(self, -1, mtexts.txts['GMT'])
		hhsizer.Add(self.gmtlabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
		self.pluscb = wx.ComboBox(self, -1, TimeSpaceDlg.PLUSCHOICES[0], size=(50, -1), choices=TimeSpaceDlg.PLUSCHOICES, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		hhsizer.Add(self.pluscb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		zonesizer.Add(hhsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		fgsizer = wx.FlexGridSizer(1, 2)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.zhourlabel = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vvsizer.Add(self.zhourlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.zhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(50,-1))
		self.zhour.SetHelpText(mtexts.txts['HelpZoneHour'])
		self.zhour.SetMaxLength(2)
		vvsizer.Add(self.zhour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.zminutelabel = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(self.zminutelabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.zminute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.zminute.SetHelpText(mtexts.txts['HelpMin'])
		self.zminute.SetMaxLength(2)
		vvsizer.Add(self.zminute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		zonesizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.daylightckb = wx.CheckBox(self, -1, mtexts.txts['Daylight'])
		zonesizer.Add(self.daylightckb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.daylightckb.SetHelpText(mtexts.txts['HelpDaylight'])

		mhsizer.Add(zonesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 0)
		mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

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

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onPlaceButton, id=ID_PlaceButton)
		self.Bind(wx.EVT_COMBOBOX, self.onZone, id=self.zonecb.GetId())

		btnOk.SetFocus()


	def onOK(self, event):
		if (self.Validate() and self.stime.Validate() and self.splace.Validate() and self.szone.Validate()):
			if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
				self.Close()
				self.SetReturnCode(wx.ID_OK)
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['InvalidDate']+' ('+self.year.GetValue()+'.'+self.month.GetValue()+'.'+self.day.GetValue()+'.)', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()		
				dlgm.Destroy()


	def onZone(self, event):
		self.enableGMT(self.zonecb.GetCurrentSelection() == 0)


	def enableGMT(self, enable):
		self.gmtlabel.Enable(enable)
		self.pluscb.Enable(enable)
		self.zhourlabel.Enable(enable)
		self.zhour.Enable(enable)
		self.zminute.Enable(enable)
		self.zminutelabel.Enable(enable)


	def onPlaceButton(self, event):
		pdlg = placesdlg.PlacesDlg(self, self.langid)
		val = pdlg.ShowModal()
		if val == wx.ID_OK:
			if pdlg.li.currentItem != -1:
				#copy selected place to fields
				place = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.PLACE)
				lon = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LON)
				lat = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LAT)
				zone = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ZONE)

				self.birthplace.SetValue(place.strip())

				#long
				idx = lon.find(u'E')#
				if idx == -1:
					idx = lon.find(u'W')#
					self.placerbW.SetValue(True)
				else:
					self.placerbE.SetValue(True)
				
				fr = 0
				if lon[0] == '0':
					fr = 1
				self.londeg.SetValue(lon[fr:idx])
				idx += 1
				if lon[idx] == '0':
					idx += 1
				self.lonmin.SetValue(lon[idx:])
	
				#lat
				idx = lat.find(u'N')#
				if idx == -1:
					idx = lat.find(u'S')#
					self.placerbS.SetValue(True)
				else:
					self.placerbN.SetValue(True)
				
				fr = 0
				if lat[0] == '0':
					fr = 1
				self.latdeg.SetValue(lat[fr:idx])
				idx += 1
				if lat[idx] == '0':
					idx += 1
				self.latmin.SetValue(lat[idx:])

				#zone
				self.pluscb.SetStringSelection(zone[0])

				zone = zone[1:]
				idx = zone.find(':')
				self.zhour.SetValue(zone[0:idx])

				idx += 1
				if zone[idx] == '0':
					idx += 1
				self.zminute.SetValue(zone[idx:])

#		pdlg.Destroy()#


	def initialize(self, chrt, ti = None):
		if ti == None:
			now = datetime.datetime.now()
			self.timeckb.SetValue(False)
			self.year.SetValue(str(now.year))
			self.month.SetValue(str(now.month))
			self.day.SetValue(str(now.day))
			self.hour.SetValue(str(now.hour))
			self.minute.SetValue(str(now.minute))
			self.sec.SetValue(str(now.second))

			self.calcb.SetStringSelection(mtexts.calList[chrt.time.cal])
			self.zonecb.SetStringSelection(mtexts.zoneList[chrt.time.zt])
			self.enableGMT(chrt.time.zt == chart.Time.ZONE)
			idx = 0
			if not chrt.time.plus:
				idx = 1
			self.pluscb.SetStringSelection(TimeSpaceDlg.PLUSCHOICES[idx])
			self.zhour.SetValue(str(chrt.time.zh))
			self.zminute.SetValue(str(chrt.time.zm))
			self.daylightckb.SetValue(False)
	
			self.year.SetFocus()
		else:
			self.timeckb.SetValue(chrt.time.bc)
			self.year.SetValue(str(ti[0]))
			self.month.SetValue(str(ti[1]))
			self.day.SetValue(str(ti[2]))
			self.hour.SetValue(str(ti[3]))
			self.minute.SetValue(str(ti[4]))
			self.sec.SetValue(str(ti[5]))

			self.calcb.SetStringSelection(mtexts.calList[ti[6]])
			self.zonecb.SetStringSelection(mtexts.zoneList[ti[7]])
			idx = 0
			if not chrt.time.plus:
				idx = 1
			self.pluscb.SetStringSelection(TimeSpaceDlg.PLUSCHOICES[idx])
			self.zhour.SetValue(str(ti[8]))
			self.zminute.SetValue(str(ti[9]))
			self.daylightckb.SetValue(False)

			self.londeg.SetFocus()

			self.timeckb.Enable(False)
			self.yearlabel.Enable(False)
			self.year.Enable(False)
			self.monthlabel.Enable(False)
			self.month.Enable(False)
			self.daylabel.Enable(False)
			self.day.Enable(False)
			self.hourlabel.Enable(False)
			self.hour.Enable(False)
			self.minlabel.Enable(False)
			self.minute.Enable(False)
			self.seclabel.Enable(False)
			self.sec.Enable(False)
			self.calcb.Enable(False)
			self.zonecb.Enable(False)
			self.enableGMT(False)
			self.zhourlabel.Enable(False)
			self.zhour.Enable(False)
			self.zminutelabel.Enable(False)
			self.zminute.Enable(False)
			self.daylightckb.Enable(False)

		self.londeg.SetValue(str(chrt.place.deglon))
		self.lonmin.SetValue(str(chrt.place.minlon))
		self.latdeg.SetValue(str(chrt.place.deglat))
		self.latmin.SetValue(str(chrt.place.minlat))
		if chrt.place.east:
			self.placerbE.SetValue(True)
		else:
			self.placerbW.SetValue(True)
		if chrt.place.north:
			self.placerbN.SetValue(True)
		else:
			self.placerbS.SetValue(True)

		self.birthplace.SetValue(chrt.place.place)




