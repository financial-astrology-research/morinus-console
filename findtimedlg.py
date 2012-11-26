import sys
import wx
import intvalidator
import rangechecker
import findtime
import mtexts
import util

import thread
import wx.lib.newevent

(FTReadyEvent, EVT_FTREADY) = wx.lib.newevent.NewEvent()
(FTDataReadyEvent, EVT_FTDATAREADY) = wx.lib.newevent.NewEvent()
(FTYearEvent, EVT_FTYEAR) = wx.lib.newevent.NewEvent()
ftlock = thread.allocate_lock()

class AbortFindTime:
	def __init__(self):
		self.abort = False

	def aborting(self):
		self.abort = True


class ResListCtrl(wx.ListCtrl):
	NUM = 0
	DATE = 1
	TIME = 2
	COLNUM = TIME+1

	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

		self.reslistdata = {}

		self.Populate()
		self.Id = ID


	def Populate(self):
		self.InsertColumn(ResListCtrl.NUM, '')
		self.InsertColumn(ResListCtrl.DATE, mtexts.txts['Date'])
		self.InsertColumn(ResListCtrl.TIME, mtexts.txts['Time'])

		self.SetColumnWidth(ResListCtrl.NUM, 50)#wx.LIST_AUTOSIZE)
		self.SetColumnWidth(ResListCtrl.DATE, 150)
		self.SetColumnWidth(ResListCtrl.TIME, 150)

		self.currentItem = -1

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
		num = self.GetItemCount()+1
		numtxt = str(num)+'.'
		self.InsertStringItem(num-1, numtxt)
		self.SetStringItem(num-1, 1, item[0])
		self.SetStringItem(num-1, 2, item[1])

		self.currentItem = 0#num-1
		self.EnsureVisible(self.currentItem) #This scrolls the list to the added item at the end
		self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


	def OnStart(self):
		if self.currentItem != -1:
			dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.DeleteAllItems()
				self.currentItem = -1
				dlg.Destroy()
				return True

			dlg.Destroy()
			return False

		return True


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class FindTimeDlg(wx.Dialog):

	LON = 0
	RETR = 1

	MIN = 0
	SEC = 1
	RET = 2

	USEAPPROX = 0
	APPROXDEG = 1
	APPROXMIN = 2
	APPROXSEC = 3
	

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['FindTime'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		self.parent = parent

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		vsizer = wx.BoxSizer(wx.VERTICAL)

		#BC
		sbc = wx.StaticBox(self, label='')
		sbcsizer = wx.StaticBoxSizer(sbc, wx.VERTICAL)
		self.bcckb = wx.CheckBox(self, -1, mtexts.txts['BC'])
		sbcsizer.Add(self.bcckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
#		self.bcckb.Enable(False)

		vsizer.Add(sbcsizer, 0, wx.GROW)

		#Planets
		splanets =wx.StaticBox(self, label='')
		splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
		gsizer = wx.GridSizer(7, 5)

		label = wx.StaticText(self, -1, mtexts.txts['Sun']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sundeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.sundeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.sundeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.sundeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sunmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.sunmin.SetHelpText(mtexts.txts['HelpMin'])
		self.sunmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.sunmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sunmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.sunmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sunsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.sunsec.SetHelpText(mtexts.txts['HelpMin'])
		self.sunsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.sunsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sunsectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.sunsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.sunretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.sunretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.sunretr.Enable(False)

		label = wx.StaticText(self, -1, mtexts.txts['Moon']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moondeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.moondeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.moondeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.moondeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.moonmin.SetHelpText(mtexts.txts['HelpMin'])
		self.moonmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.moonmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moonmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.moonmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moonsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.moonsec.SetHelpText(mtexts.txts['HelpMin'])
		self.moonsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.moonsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moonsectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.moonsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.moonretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.moonretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.moonretr.Enable(False)

		label = wx.StaticText(self, -1, mtexts.txts['Mercury']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mercurydeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.mercurydeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.mercurydeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mercurydeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mercurymin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.mercurymin.SetHelpText(mtexts.txts['HelpMin'])
		self.mercurymin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mercurymin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mercurymintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.mercurymintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mercurysec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.mercurysec.SetHelpText(mtexts.txts['HelpMin'])
		self.mercurysec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mercurysec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mercurysectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.mercurysectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.mercuryretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mercuryretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Venus']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.venusdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.venusdeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.venusdeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.venusdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.venusmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.venusmin.SetHelpText(mtexts.txts['HelpMin'])
		self.venusmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.venusmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.venusmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.venusmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.venussec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.venussec.SetHelpText(mtexts.txts['HelpMin'])
		self.venussec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.venussec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.venussectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.venussectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.venusretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.venusretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Mars']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.marsdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.marsdeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.marsdeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.marsdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.marsmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.marsmin.SetHelpText(mtexts.txts['HelpMin'])
		self.marsmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.marsmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.marsmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.marsmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.marssec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.marssec.SetHelpText(mtexts.txts['HelpMin'])
		self.marssec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.marssec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.marssectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.marssectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.marsretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.marsretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Jupiter']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.jupiterdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.jupiterdeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.jupiterdeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.jupiterdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.jupitermin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.jupitermin.SetHelpText(mtexts.txts['HelpMin'])
		self.jupitermin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.jupitermin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.jupitermintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.jupitermintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.jupitersec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.jupitersec.SetHelpText(mtexts.txts['HelpMin'])
		self.jupitersec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.jupitersec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.jupitersectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.jupitersectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.jupiterretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.jupiterretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		label = wx.StaticText(self, -1, mtexts.txts['Saturn']+':')
		gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.saturndeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.saturndeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.saturndeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.saturndeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		label = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.saturnmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.saturnmin.SetHelpText(mtexts.txts['HelpMin'])
		self.saturnmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.saturnmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.saturnmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.saturnmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.saturnsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.saturnsec.SetHelpText(mtexts.txts['HelpMin'])
		self.saturnsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.saturnsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.saturnsectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.saturnsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.saturnretr = wx.CheckBox(self, -1, mtexts.txts['R'])
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.saturnretr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		splanetssizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vsizer.Add(splanetssizer, 0)

		#Use
		suse = wx.StaticBox(self, label=mtexts.txts['Use'])
		susesizer = wx.StaticBoxSizer(suse, wx.VERTICAL)
		self.useminckb = wx.CheckBox(self, -1, mtexts.txts['Minute'])
		susesizer.Add(self.useminckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		self.usesecckb = wx.CheckBox(self, -1, mtexts.txts['Second'])
		susesizer.Add(self.usesecckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)
		self.useretrckb = wx.CheckBox(self, -1, mtexts.txts['Retrograde'])
		susesizer.Add(self.useretrckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vsizer.Add(susesizer, 1, wx.GROW)

		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL, 0)

		#Angles
		vvvsizer = wx.BoxSizer(wx.VERTICAL)

		sangles = wx.StaticBox(self, label='')
		sanglessizer = wx.StaticBoxSizer(sangles, wx.VERTICAL)
		gsizer = wx.GridSizer(2, 4)
		self.asctxt = wx.StaticText(self, -1, mtexts.txts['Asc']+':')
		gsizer.Add(self.asctxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.ascdeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.ascdeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.ascdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascdegtxt = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(self.ascdegtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.ascmin.SetHelpText(mtexts.txts['HelpMin'])
		self.ascmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.ascmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.ascmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.ascsec.SetHelpText(mtexts.txts['HelpMin'])
		self.ascsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.ascsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.ascsectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.ascsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.mctxt = wx.StaticText(self, -1, mtexts.txts['MC']+':')
		gsizer.Add(self.mctxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,-1))
		self.mcdeg.SetHelpText(mtexts.txts['HelpDeg'])
		self.mcdeg.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mcdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcdegtxt = wx.StaticText(self, -1, mtexts.txts['D2'])
		hsizer.Add(self.mcdegtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.mcmin.SetHelpText(mtexts.txts['HelpMin'])
		self.mcmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mcmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcmintxt = wx.StaticText(self, -1, mtexts.txts['M2'])
		hsizer.Add(self.mcmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.mcsec.SetHelpText(mtexts.txts['HelpMin'])
		self.mcsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.mcsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.mcsectxt = wx.StaticText(self, -1, mtexts.txts['S2'])
		hsizer.Add(self.mcsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		sanglessizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		self.useascmcckb = wx.CheckBox(self, -1, mtexts.txts['Use'])
		sanglessizer.Add(self.useascmcckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vvvsizer.Add(sanglessizer, 0, wx.GROW|wx.LEFT, 5)

		#Force date
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000

		sforce = wx.StaticBox(self, label='')
		sforcesizer = wx.StaticBoxSizer(sforce, wx.VERTICAL)
		gsizer = wx.GridSizer(2, 3)
		self.fyear = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, rnge), size=(50,-1))
		if checker.isExtended():
			self.fyear.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.fyear.SetHelpText(mtexts.txts['HelpYear2'])
		self.fyear.SetMaxLength(4)

		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fyear, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fyeartxt = wx.StaticText(self, -1, mtexts.txts['YE'])
		hsizer.Add(self.fyeartxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fmonth = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		self.fmonth.SetHelpText(mtexts.txts['HelpMonth'])
		self.fmonth.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fmonth, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fmonthtxt = wx.StaticText(self, -1, mtexts.txts['MO2'])
		hsizer.Add(self.fmonthtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fday = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,-1))
		self.fday.SetHelpText(mtexts.txts['HelpDay'])
		self.fday.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fday, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fdaytxt = wx.StaticText(self, -1, mtexts.txts['DA'])
		hsizer.Add(self.fdaytxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		self.fhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,-1))
		self.fhour.SetHelpText(mtexts.txts['HelpHour'])
		self.fhour.SetMaxLength(3)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fhour, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fhourtxt = wx.StaticText(self, -1, mtexts.txts['HO'])
		hsizer.Add(self.fhourtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.fmin.SetHelpText(mtexts.txts['HelpMin'])
		self.fmin.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fmintxt = wx.StaticText(self, -1, mtexts.txts['MI'])
		hsizer.Add(self.fmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,-1))
		self.fsec.SetHelpText(mtexts.txts['HelpMin'])
		self.fsec.SetMaxLength(2)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)#
		hsizer.Add(self.fsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.fsectxt = wx.StaticText(self, -1, mtexts.txts['SE'])
		hsizer.Add(self.fsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		sforcesizer.Add(gsizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		self.forceckb = wx.CheckBox(self, -1, mtexts.txts['ForceTheDate'])
		sforcesizer.Add(self.forceckb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vvvsizer.Add(sforcesizer, 0, wx.GROW|wx.LEFT, 5)

		#Approximation(Planets)
		sapprox = wx.StaticBox(self, label=mtexts.txts['ApproxPlanets'])
		sapproxsizer = wx.StaticBoxSizer(sapprox, wx.VERTICAL)
		self.useapproxckb = wx.CheckBox(self, -1, mtexts.txts['Use'])
		self.approxdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 4), size=(30,-1))
		self.approxdeg.SetHelpText(mtexts.txts['HelpApproxDeg'])
		self.approxdeg.SetMaxLength(1)
		self.approxmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.approxmin.SetHelpText(mtexts.txts['HelpMin'])
		self.approxmin.SetMaxLength(2)
		self.approxsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,-1))
		self.approxsec.SetHelpText(mtexts.txts['HelpMin'])
		self.approxsec.SetMaxLength(2)
		hsizerDeg = wx.BoxSizer(wx.HORIZONTAL)#
		hsizerDeg.Add(self.approxdeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.approxdegtxt = wx.StaticText(self, -1, mtexts.txts['D'])
		hsizerDeg.Add(self.approxdegtxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerMin = wx.BoxSizer(wx.HORIZONTAL)#
		hsizerMin.Add(self.approxmin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.approxmintxt = wx.StaticText(self, -1, mtexts.txts['M'])
		hsizerMin.Add(self.approxmintxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerSec = wx.BoxSizer(wx.HORIZONTAL)#
		hsizerSec.Add(self.approxsec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		self.approxsectxt = wx.StaticText(self, -1, mtexts.txts['S'])
		hsizerSec.Add(self.approxsectxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerLon = wx.BoxSizer(wx.HORIZONTAL)#
		hsizerLon.Add(hsizerDeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerLon.Add(hsizerMin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerLon.Add(hsizerSec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerAppr = wx.BoxSizer(wx.HORIZONTAL)#
		hsizerAppr.Add(self.useapproxckb, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		hsizerAppr.Add(hsizerLon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

		sapproxsizer.Add(hsizerAppr, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 5)

		vvvsizer.Add(sapproxsizer, 0, wx.GROW|wx.LEFT, 5)

		#List
		sreslist =wx.StaticBox(self, label='')
		reslistsizer = wx.StaticBoxSizer(sreslist, wx.VERTICAL)
		ID_ResList = wx.NewId()
		self.li = ResListCtrl(self, ID_ResList, size=(360,100), style=wx.LC_VRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL)
		reslistsizer.Add(self.li, 1, wx.GROW|wx.ALL, 5)

		vvvsizer.Add(reslistsizer, 0, wx.GROW|wx.LEFT, 5)

		#Start and Show
		List_Start_ID = wx.NewId()
		self.btnStart = wx.Button(self, List_Start_ID, mtexts.txts['Start2'])
		List_Show_ID = wx.NewId()
		self.btnShow = wx.Button(self, List_Show_ID, mtexts.txts['Show'])
		self.btnShow.Enable(False)

		hbtnsizer = wx.BoxSizer(wx.HORIZONTAL)
		hbtnsizer.Add(self.btnStart, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL, 5)
		hbtnsizer.Add(self.btnShow, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL, 5)

		vvvsizer.Add(hbtnsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL, 5)

		mhsizer.Add(vvvsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL, 0)

		mvsizer.Add(mhsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

		btnsizer = wx.StdDialogButtonSizer()
	
		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Close'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)
		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		self.Bind(wx.EVT_CHECKBOX, self.onUseMin, id=self.useminckb.GetId())
		self.Bind(wx.EVT_CHECKBOX, self.onUseSec, id=self.usesecckb.GetId())
		self.Bind(wx.EVT_CHECKBOX, self.onUseRetr, id=self.useretrckb.GetId())

		self.Bind(wx.EVT_CHECKBOX, self.onUseAscMC, id=self.useascmcckb.GetId())
		self.Bind(wx.EVT_CHECKBOX, self.onUseForce, id=self.forceckb.GetId())

		self.Bind(wx.EVT_CHECKBOX, self.onUseApprox, id=self.useapproxckb.GetId())

		self.useminckb.SetValue(True)
		self.usesecckb.SetValue(True)
		self.useretrckb.SetValue(True)

		self.useascmcckb.SetValue(False)
		self.enableAscMC(self.useascmcckb.GetValue())
		self.enableForce(self.useascmcckb.GetValue())

		self.useapproxckb.SetValue(False)
		self.approxdeg.Enable(False)
		self.approxdegtxt.Enable(False)
		self.approxmin.Enable(False)
		self.approxmintxt.Enable(False)
		self.approxsec.Enable(False)
		self.approxsectxt.Enable(False)

		self.Bind(wx.EVT_BUTTON, self.OnStart, id=self.btnStart.GetId())
		self.Bind(wx.EVT_BUTTON, self.OnShow, id=self.btnShow.GetId())

		self.Bind(wx.EVT_BUTTON, self.onOK, id=btnOk.GetId())

		self.Bind(EVT_FTREADY, self.OnFTReady)
		self.Bind(EVT_FTDATAREADY, self.OnFTDataReady)
		self.Bind(EVT_FTYEAR, self.OnFTYear)

		btnOk.SetFocus()

		self.progtxt = mtexts.txts['BusyInfo2']
		self.suffix = ''
		self.found = False
		self.ar = None


	def onUseMin(self, event):
		val = self.useminckb.GetValue()
		self.enableMins(val)
		if not val:
			self.usesecckb.SetValue(False)
			self.usesecckb.Enable(False)
			self.enableSecs(False)

			self.useapproxckb.SetValue(False)
			self.approxdeg.Enable(False)
			self.approxdegtxt.Enable(False)
			self.approxmin.Enable(False)
			self.approxmintxt.Enable(False)
			self.approxsec.Enable(False)
			self.approxsectxt.Enable(False)
		else:
			self.usesecckb.Enable(True)


	def enableMins(self, val):
		ar = (self.sunmin, self.sunmintxt, self.moonmin, self.moonmintxt, self.mercurymin, self.mercurymintxt, self.venusmin, self.venusmintxt, self.marsmin, self.marsmintxt, self.jupitermin, self.jupitermintxt, self.saturnmin, self.saturnmintxt)
		arlen = len(ar)
		for i in range(arlen):
			ar[i].Enable(val)


	def onUseSec(self, event):
		self.enableSecs(self.usesecckb.GetValue())
		val = self.usesecckb.GetValue()
		if not val:
			self.useapproxckb.SetValue(False)
			self.approxdeg.Enable(False)
			self.approxdegtxt.Enable(False)
			self.approxmin.Enable(False)
			self.approxmintxt.Enable(False)
			self.approxsec.Enable(False)
			self.approxsectxt.Enable(False)


	def enableSecs(self, val):
		ar = (self.sunsec, self.sunsectxt, self.moonsec, self.moonsectxt, self.mercurysec, self.mercurysectxt, self.venussec, self.venussectxt, self.marssec, self.marssectxt, self.jupitersec, self.jupitersectxt, self.saturnsec, self.saturnsectxt)
		arlen = len(ar)
		for i in range(arlen):
			ar[i].Enable(val)


	def onUseRetr(self, event):
		self.enableRetrs(self.useretrckb.GetValue())


	def onUseAscMC(self, event):
		self.enableAscMC(self.useascmcckb.GetValue())
		self.enableForce(self.useascmcckb.GetValue())

		if self.forceckb.GetValue():
			self.btnStart.Enable(not self.useascmcckb.GetValue())
			self.btnShow.Enable(self.useascmcckb.GetValue())


	def onUseForce(self, event):
		self.btnStart.Enable(not self.forceckb.GetValue())
		self.btnShow.Enable(self.forceckb.GetValue())


	def onUseApprox(self, event):
		self.enableApprox(self.useapproxckb.GetValue())


	def enableRetrs(self, val):
		ar = (self.mercuryretr, self.venusretr, self.marsretr, self.jupiterretr, self.saturnretr)
		arlen = len(ar)
		for i in range(arlen):
			ar[i].Enable(val)


	def enableAscMC(self, val):
		ar = (self.asctxt, self.ascdeg, self.ascdegtxt, self.ascmin, self.ascmintxt, self.ascsec, self.ascsectxt, self.mctxt, self.mcdeg, self.mcdegtxt, self.mcmin, self.mcmintxt, self.mcsec, self.mcsectxt)
		arlen = len(ar)
		for i in range(arlen):
			ar[i].Enable(val)


	def enableForce(self, val):
		ar = (self.fyear, self.fyeartxt, self.fmonth, self.fmonthtxt, self.fday, self.fdaytxt, self.fhour, self.fhourtxt, self.fmin, self.fmintxt, self.fsec, self.fsectxt)
		arlen = len(ar)
		for i in range(arlen):
			ar[i].Enable(val)

		self.forceckb.Enable(val)


	def enableApprox(self, val):
		self.approxdeg.Enable(val)
		self.approxdegtxt.Enable(val)
		self.approxmin.Enable(val)
		self.approxmintxt.Enable(val)
		self.approxsec.Enable(val)
		self.approxsectxt.Enable(val)
		self.enableMins(True)
		self.enableSecs(True)

		self.useminckb.SetValue(True)
		self.usesecckb.Enable(True)
		self.usesecckb.SetValue(True)


	def OnStart(self, event):
		if (not self.Validate()):
			return

		res = self.li.OnStart()
		if not res:
			return

		if not self.checkAsc():
			return

		self.bc = self.bcckb.GetValue()

		sunlon = float(self.sundeg.GetValue())
		if self.useminckb.GetValue():
			sunlon += float(self.sunmin.GetValue())/60.0
			if self.usesecckb.GetValue():
				sunlon += float(self.sunsec.GetValue())/3600.0
		sunretr = False

		moonlon = float(self.moondeg.GetValue())
		if self.useminckb.GetValue():
			moonlon += float(self.moonmin.GetValue())/60.0
			if self.usesecckb.GetValue():
				moonlon += float(self.moonsec.GetValue())/3600.0
		moonretr = False

		mercurylon = float(self.mercurydeg.GetValue())
		if self.useminckb.GetValue():
			mercurylon += float(self.mercurymin.GetValue())/60.0
			if self.usesecckb.GetValue():
				mercurylon += float(self.mercurysec.GetValue())/3600.0
		mercuryretr = self.mercuryretr.GetValue()

		venuslon = float(self.venusdeg.GetValue())
		if self.useminckb.GetValue():
			venuslon += float(self.venusmin.GetValue())/60.0
			if self.usesecckb.GetValue():
				venuslon += float(self.venussec.GetValue())/3600.0
		venusretr = self.venusretr.GetValue()

		marslon = float(self.marsdeg.GetValue())
		if self.useminckb.GetValue():
			marslon += float(self.marsmin.GetValue())/60.0
			if self.usesecckb.GetValue():
				marslon += float(self.marssec.GetValue())/3600.0
		marsretr = self.marsretr.GetValue()

		jupiterlon = float(self.jupiterdeg.GetValue())
		if self.useminckb.GetValue():
			jupiterlon += float(self.jupitermin.GetValue())/60.0
			if self.usesecckb.GetValue():
				jupiterlon += float(self.jupitersec.GetValue())/3600.0
		jupiterretr = self.jupiterretr.GetValue()

		saturnlon = float(self.saturndeg.GetValue())
		if self.useminckb.GetValue():
			saturnlon += float(self.saturnmin.GetValue())/60.0
		if self.usesecckb.GetValue():
			saturnlon += float(self.saturnsec.GetValue())/3600.0

		saturnretr = self.saturnretr.GetValue()

		useascmc = self.useascmcckb.GetValue()

		asclon = float(self.ascdeg.GetValue())+float(self.ascmin.GetValue())/60.0+float(self.ascsec.GetValue())/3600.0
		mclon = float(self.mcdeg.GetValue())+float(self.mcmin.GetValue())/60.0+float(self.mcsec.GetValue())/3600.0

		useapprox = self.useapproxckb.GetValue()
		approxdeg = float(self.approxdeg.GetValue())
		approxmin = float(self.approxmin.GetValue())
		approxsec = float(self.approxsec.GetValue())

		ftdata = ((sunlon, sunretr), (moonlon, moonretr), (mercurylon, mercuryretr), (venuslon, venusretr), (marslon, marsretr), (jupiterlon, jupiterretr), (saturnlon, saturnretr))

		usemin = self.useminckb.GetValue()
		usesec = self.usesecckb.GetValue()
		useretr = self.useretrckb.GetValue()
		ftdatause = (usemin, usesec, useretr)

		ftdataascmc = (useascmc, asclon, mclon)

		ftdataapprox = (useapprox, approxdeg, approxmin, approxsec)

		##########

		self.suffix = ''
		self.progtxt = mtexts.txts['BusyInfo2']
		self.progbar = wx.ProgressDialog(mtexts.txts['Calculating'], self.progtxt+'\n', parent=self, style = wx.PD_CAN_ABORT|wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME)
		self.progbar.Fit()

		self.btnShow.Enable(False)
		self.found = False
		if self.ar != None:
			del self.ar
			self.ar = None
		self.ftready = False
		self.abort = AbortFindTime()
		thId = thread.start_new_thread(self.calcCharts, (self.bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, self))

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.timer.Start(500)


	def calcCharts(self, bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, win):
		ft = findtime.FindTime(bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, self.abort, win)

		ft.find()

		#maybe there is no need for synchronization since the worker thread is done and it only uses the abort variable but it doesn't matter if it is skipped for a cycle (this is copy/pasted code)
		ftlock.acquire()
		self.ftready = True
		ftlock.release()
		evt = FTReadyEvent()
		wx.PostEvent(win, evt)


	def OnTimer(self, event):
		ftlock.acquire()
		if not self.ftready:
			self.progtxt = mtexts.txts['BusyInfo2']+ '\n' + mtexts.txts['Year'] + ': ' + self.suffix
			(keepGoing, skip) = self.progbar.Pulse(self.progtxt)

			if not keepGoing:
				self.abort.aborting()
		ftlock.release()


	def OnFTReady(self, event):
		self.timer.Stop()
		del self.timer
		self.progbar.Destroy()
		del self.progbar

		if self.abort.abort:
			self.Refresh()
		else:
			if not self.found:
				dlgm = wx.MessageDialog(self, mtexts.txts['NoChartWithSettings'], mtexts.txts['Information'], wx.OK|wx.ICON_INFORMATION)
				dlgm.ShowModal()
				dlgm.Destroy()#

		del self.abort

		if self.found:
			self.btnShow.Enable(True)


	def OnFTDataReady(self, event):
		#update wnd
		self.OnAdd(event.attr1)
		if self.ar == None:
			self.ar = []
		self.ar.append(event.attr1)
		self.found = True


	def OnFTYear(self, event):
		signtxt = ''
		if self.bcckb.GetValue():
			signtxt = '-'
		self.suffix = signtxt+str(event.attr1)


	def OnAdd(self, fnd):
		datstr = str(fnd[0])+'.'+str(fnd[1])+'.'+str(fnd[2])
		h, m, s = util.decToDeg(fnd[3])
		timstr = str(h).zfill(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
		item = [datstr, timstr]

		self.li.OnAdd(item)


	def OnShow(self, event):
#		self.Close()
		if self.useascmcckb.GetValue() and self.forceckb.GetValue():
			if (not self.Validate()):
				return

		if not self.checkAsc():
			return

		arplac = [0.0, 0.0, False] #mclon, asclon, use
		if self.useascmcckb.GetValue():
			arplac[0] = float(self.mcdeg.GetValue())+float(self.mcmin.GetValue())/60.0+float(self.mcsec.GetValue())/3600.0
			arplac[1] = float(self.ascdeg.GetValue())+float(self.ascmin.GetValue())/60.0+float(self.ascsec.GetValue())/3600.0
			arplac[2] = True

		if self.forceckb.GetValue():
			t = float(self.fhour.GetValue())+float(self.fmin.GetValue())/60.0+float(self.fsec.GetValue())/3600.0
			it = (int(self.fyear.GetValue()), int(self.fmonth.GetValue()), int(self.fday.GetValue()), t)
		else:
			it = self.ar[self.li.currentItem]

		self.parent.showFindTime(self.bcckb.GetValue(), it, arplac)


	def checkAsc(self):
		res = True
		if self.useascmcckb.GetValue():
			if (int(self.ascdeg.GetValue()) == 0 and int(self.ascmin.GetValue()) == 0 and int(self.ascsec.GetValue()) == 0) or (int(self.ascdeg.GetValue()) == 180 and int(self.ascmin.GetValue()) == 0 and int(self.ascsec.GetValue()) == 0):
				dlg = wx.MessageDialog(self, mtexts.txts['InvalidAsc'], mtexts.txts['Information'], wx.OK|wx.ICON_INFORMATION)
				val = dlg.ShowModal()
				dlg.Destroy()
				res = False

		return res


	def onOK(self, event):
		self.Close()
		self.SetReturnCode(wx.ID_OK)


	def fill(self):
		self.saturndeg.SetValue(str(0))
		self.saturnmin.SetValue(str(0))
		self.saturnsec.SetValue(str(0))
		self.jupiterdeg.SetValue(str(0))
		self.jupitermin.SetValue(str(0))
		self.jupitersec.SetValue(str(0))
		self.marsdeg.SetValue(str(0))
		self.marsmin.SetValue(str(0))
		self.marssec.SetValue(str(0))
		self.sundeg.SetValue(str(0))
		self.sunmin.SetValue(str(0))
		self.sunsec.SetValue(str(0))
		self.venusdeg.SetValue(str(0))
		self.venusmin.SetValue(str(0))
		self.venussec.SetValue(str(0))
		self.mercurydeg.SetValue(str(0))
		self.mercurymin.SetValue(str(0))
		self.mercurysec.SetValue(str(0))
		self.moondeg.SetValue(str(0))
		self.moonmin.SetValue(str(0))
		self.moonsec.SetValue(str(0))

		self.ascdeg.SetValue(str(0))
		self.ascmin.SetValue(str(0))
		self.ascsec.SetValue(str(0))
		self.mcdeg.SetValue(str(0))
		self.mcmin.SetValue(str(0))
		self.mcsec.SetValue(str(0))

		self.fyear.SetValue(str(1))
		self.fmonth.SetValue(str(1))
		self.fday.SetValue(str(1))
		self.fhour.SetValue(str(0))
		self.fmin.SetValue(str(0))
		self.fsec.SetValue(str(0))

		self.approxdeg.SetValue(str(0))
		self.approxmin.SetValue(str(0))
		self.approxsec.SetValue(str(0))







