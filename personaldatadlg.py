# -*- coding: utf-8 -*-

import wx
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


class PersonalDataDlg(wx.Dialog):

	PLUSCHOICES = (u'+', u'-')

	def __init__(self, parent, langid):

		self.langid = langid

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, -1, mtexts.txts['PersonalData'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
		self.PostCreate(pre)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		# Name&Gender
		sname =wx.StaticBox(self, label='')
		namesizer = wx.StaticBoxSizer(sname, wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Name']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.name = wx.TextCtrl(self, -1, '', size=(220,-1))
		self.name.SetHelpText(mtexts.txts['HelpName'])
		self.name.SetMaxLength(20)
		hsizer.Add(self.name, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Gender']+':')
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.genderrbM = wx.RadioButton(self, -1, mtexts.txts['Male'], style=wx.RB_GROUP)
		vsubsizer.Add(self.genderrbM, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		self.genderrbF = wx.RadioButton(self, -1, mtexts.txts['Female'])
		vsubsizer.Add(self.genderrbF, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 2)
		hsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, -1, mtexts.txts['Type']+':')
		hsubsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		self.typecb = wx.ComboBox(self, -1, mtexts.typeList[0], size=(140, -1), choices=mtexts.typeList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.typecb.SetHelpText(mtexts.txts['HelpType'])
		hsubsizer.Add(self.typecb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		hsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)
		vsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)
		namesizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		hsubsizer = wx.BoxSizer(wx.HORIZONTAL)

		vsubsizer.Add(namesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 0)

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
		label = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vvsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)
		vvsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Day']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.day.SetHelpText(mtexts.txts['HelpDay'])
		self.day.SetMaxLength(2)
		vvsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.hour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,-1))
		self.hour.SetHelpText(mtexts.txts['HelpHour'])
		self.hour.SetMaxLength(2)
		vvsizer.Add(self.hour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		self.minute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.minute.SetHelpText(mtexts.txts['HelpMin'])
		self.minute.SetMaxLength(2)
		vvsizer.Add(self.minute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		vvsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Sec']+':')
		vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
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
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
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
		hsubsizer.Add(vvsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		#Zone
		self.szone =wx.StaticBox(self, label='')
		zonesizer = wx.StaticBoxSizer(self.szone, wx.VERTICAL)
		self.calcb = wx.ComboBox(self, -1, mtexts.calList[0], size=(80, -1), choices=mtexts.calList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		zonesizer.Add(self.calcb, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)
		self.zonecb = wx.ComboBox(self, -1, mtexts.zoneList[0], size=(80, -1), choices=mtexts.zoneList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		zonesizer.Add(self.zonecb, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)
#		self.zonecb.SetHelpText(mtexts.txts['zone-time')
		hhsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.gmtlabel = wx.StaticText(self, -1, mtexts.txts['GMT'])
		hhsizer.Add(self.gmtlabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
		self.pluscb = wx.ComboBox(self, -1, PersonalDataDlg.PLUSCHOICES[0], size=(50, -1), choices=PersonalDataDlg.PLUSCHOICES, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		hhsizer.Add(self.pluscb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		zonesizer.Add(hhsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		fgsizer = wx.FlexGridSizer(1, 2)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.zhourlabel = wx.StaticText(self, -1, mtexts.txts['Hour']+':')
		vvsizer.Add(self.zhourlabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.zhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,-1))
		self.zhour.SetHelpText(mtexts.txts['HelpZoneHour'])
		self.zhour.SetMaxLength(2)
		vvsizer.Add(self.zhour, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vvsizer = wx.BoxSizer(wx.VERTICAL)
		self.zminutelabel = wx.StaticText(self, -1, mtexts.txts['Min']+':')
		vvsizer.Add(self.zminutelabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		self.zminute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.zminute.SetHelpText(mtexts.txts['HelpMin'])
		self.zminute.SetMaxLength(2)
		vvsizer.Add(self.zminute, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
		fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		zonesizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.daylightckb = wx.CheckBox(self, -1, mtexts.txts['Daylight'])
		zonesizer.Add(self.daylightckb, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.daylightckb.SetHelpText(mtexts.txts['HelpDaylight'])

		vvsubsizer = wx.BoxSizer(wx.VERTICAL)
		vvsubsizer.Add(zonesizer, 2, wx.ALIGN_LEFT|wx.ALL, 0)

		#Altitude
		self.sphs =wx.StaticBox(self, label=mtexts.txts['PlanetaryHour'])
		hourssizer = wx.StaticBoxSizer(self.sphs, wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Altitude']+':')
		hourssizer.Add(label, 0, wx.ALIGN_CENTER|wx.TOP, 10)
		self.alt = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10000), size=(60,-1))
		self.alt.SetHelpText(mtexts.txts['HelpAltitude'])
		self.alt.SetMaxLength(5)
		hhsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		hhsubsizer.Add(self.alt, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		label = wx.StaticText(self, -1, 'm')
		hhsubsizer.Add(label, 0, wx.ALIGN_CENTER|wx.LEFT, 2)
		hourssizer.Add(hhsubsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		vvsubsizer.Add(hourssizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 0)

		hsubsizer.Add(vvsubsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 0)
		vsubsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT|wx.ALL, 0)

		mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)###

		#Notes
		self.snotes =wx.StaticBox(self, label=mtexts.txts['Notes'])
		notessizer = wx.StaticBoxSizer(self.snotes, wx.VERTICAL)
		self.notes = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE, size=(250,-1))
		self.notes.SetHelpText(mtexts.txts['HelpNotes'])
		self.notes.SetMaxLength(500)
		notessizer.Add(self.notes, 1, wx.ALIGN_LEFT|wx.ALL, 0)

		mhsizer.Add(notessizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 0)
		mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT, 5)

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
		self.Bind(wx.EVT_BUTTON, self.onPlaceButton, id=ID_PlaceButton)
		self.Bind(wx.EVT_COMBOBOX, self.onZone, id=self.zonecb.GetId())

		self.name.SetFocus()


	def onOK(self, event):
		if (self.Validate() and self.stime.Validate() and self.splace.Validate() and self.szone.Validate() and self.sphs):

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
				alt = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ALT)

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

				#alt
				self.alt.SetValue(alt)

		pdlg.Destroy()#


	def initialize(self):
		self.timeckb.SetValue(False)
		self.name.SetValue('')
		self.genderrbM.SetValue(True)
		self.year.SetValue(str(1950))
		self.month.SetValue(str(1))
		self.day.SetValue(str(1))
		self.hour.SetValue(str(0))
		self.minute.SetValue(str(0))
		self.sec.SetValue(str(0))
		self.birthplace.SetValue('')
		self.londeg.SetValue(str(0))
		self.lonmin.SetValue(str(0))
		self.latdeg.SetValue(str(0))
		self.latmin.SetValue(str(0))
		self.placerbE.SetValue(True)
		self.placerbN.SetValue(True)
		self.typecb.SetStringSelection(mtexts.typeList[chart.Chart.RADIX]) # -> Horoscope!!
		self.calcb.SetStringSelection(mtexts.calList[chart.Time.GREGORIAN])
		self.zonecb.SetStringSelection(mtexts.zoneList[chart.Time.ZONE])
		self.enableGMT(True)
		self.pluscb.SetStringSelection(PersonalDataDlg.PLUSCHOICES[0])
		self.zhour.SetValue(str(1))
		self.zminute.SetValue(str(0))
		self.daylightckb.SetValue(False)
		self.alt.SetValue(str(100))
		self.notes.Clear()


	def fill(self, chrt):
		self.name.SetValue(chrt.name)
		if chrt.male:
			self.genderrbM.SetValue(True)
		else:
			self.genderrbF.SetValue(True)
		self.typecb.SetStringSelection(mtexts.typeList[chrt.htype])
		self.year.SetValue(str(chrt.time.origyear))
		self.month.SetValue(str(chrt.time.origmonth))
		self.day.SetValue(str(chrt.time.origday))
		self.hour.SetValue(str(chrt.time.hour))
		self.minute.SetValue(str(chrt.time.minute))
		self.sec.SetValue(str(chrt.time.second))
		self.timeckb.SetValue(chrt.time.bc)
		self.calcb.SetStringSelection(mtexts.calList[chrt.time.cal])
		self.zonecb.SetStringSelection(mtexts.zoneList[chrt.time.zt])
		self.enableGMT(chrt.time.zt == chart.Time.ZONE)
		idx = 0
		if not chrt.time.plus:
			idx = 1
		self.pluscb.SetStringSelection(PersonalDataDlg.PLUSCHOICES[idx])
		self.zhour.SetValue(str(chrt.time.zh))
		self.zminute.SetValue(str(chrt.time.zm))
		self.daylightckb.SetValue(chrt.time.daylightsaving)
		self.birthplace.SetValue(chrt.place.place)
		self.londeg.SetValue(str(chrt.place.deglon))
		self.lonmin.SetValue(str(chrt.place.minlon))
		if chrt.place.east:
			self.placerbE.SetValue(True)
		else:
			self.placerbW.SetValue(True)
		self.latdeg.SetValue(str(chrt.place.deglat))
		self.latmin.SetValue(str(chrt.place.minlat))
		if chrt.place.north:
			self.placerbN.SetValue(True)
		else:
			self.placerbS.SetValue(True)
		self.alt.SetValue(str(chrt.place.altitude))
		self.notes.SetValue(chrt.notes)


	def check(self, chrt):
		changed = False
		if self.name.GetValue() != chrt.name:
			changed = True
		elif (self.genderrbM.GetValue() != chrt.male):
			changed = True
		elif self.typecb.GetCurrentSelection() != chrt.htype:
			changed = True
		elif self.notes.GetValue() != chrt.notes:
			changed = True
		#time
		elif int(self.year.GetValue()) != chrt.time.origyear:
			changed = True
		elif int(self.month.GetValue()) != chrt.time.origmonth:
			changed = True
		elif int(self.day.GetValue()) != chrt.time.origday:
			changed = True
		elif int(self.hour.GetValue()) != chrt.time.hour:
			changed = True
		elif int(self.minute.GetValue()) != chrt.time.minute:
			changed = True
		elif int(self.sec.GetValue()) != chrt.time.second:
			changed = True
		elif self.timeckb.GetValue() != chrt.time.bc:
			changed = True
		elif self.calcb.GetCurrentSelection() != chrt.time.cal:
			changed = True
		elif self.zonecb.GetCurrentSelection() != chrt.time.zt:
			changed = True

		idx = 0
		if not chrt.time.plus:
			idx = 1
		elif self.pluscb.GetCurrentSelection() != idx:
			changed = True
		elif int(self.zhour.GetValue()) != chrt.time.zh:
			changed = True
		elif int(self.zminute.GetValue()) != chrt.time.zm:
			changed = True
		elif int(self.daylightckb.GetValue()) != chrt.time.daylightsaving:
			changed = True
		#place
		elif self.birthplace.GetValue() != chrt.place.place:
			changed = True
		elif int(self.londeg.GetValue()) != chrt.place.deglon:
			changed = True
		elif int(self.lonmin.GetValue()) != chrt.place.minlon:
			changed = True
		elif (self.placerbE.GetValue() != chrt.place.east):
			changed = True
		elif int(self.latdeg.GetValue()) != chrt.place.deglat:
			changed = True
		elif int(self.latmin.GetValue()) != chrt.place.minlat:
			changed = True
		elif (self.placerbN.GetValue() != chrt.place.north):
			changed = True
		elif (self.alt.GetValue() != chrt.place.altitude):
			changed = True

		return changed





