import wx
import chart
import mundanewnd
import positionswnd
import positionswnd2
import mtexts



class MundaneFrame(wx.Frame):
	CHART = 0
	COMPOUND = 1
	POSITIONS = 2
#	SQUARE = 3

	def __init__(self, parent, title, opts, chrt, radix=None):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		self.parent = parent
		self.title = title
		self.options = opts
		self.chart = chrt
		self.radix = radix
		self.selection = MundaneFrame.CHART

		self.pmenu = wx.Menu()
		self.ID_Selection = wx.NewId()
		self.ID_SaveAsBitmap = wx.NewId()
		self.ID_BlackAndWhite = wx.NewId()

		self.ID_Chart = wx.NewId()
		self.ID_Comparison = wx.NewId()
		self.ID_Positions = wx.NewId()
#		self.ID_Square = wx.NewId()

		self.selmenu = wx.Menu()
		self.chartmenu = self.selmenu.Append(self.ID_Chart, mtexts.txts['Chart'], '', wx.ITEM_RADIO)
		if self.radix != None:
			self.compoundmenu = self.selmenu.Append(self.ID_Comparison, mtexts.txts['Comparison'], '', wx.ITEM_RADIO)
		self.positionsmenu = self.selmenu.Append(self.ID_Positions, mtexts.txts['Positions'], '', wx.ITEM_RADIO)
#		self.squaremenu = self.selmenu.Append(self.ID_Square, mtexts.txts['Square'], '', wx.ITEM_RADIO)

		self.pmenu.AppendMenu(self.ID_Selection, mtexts.txts['Windows'], self.selmenu)

		self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txts['SaveAsBmp'], mtexts.txts['SaveChart'])
		self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txts['BlackAndWhite'], mtexts.txts['ChartBW'], wx.ITEM_CHECK)
		
		self.SetMinSize((200,200))

		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)

		self.Bind(wx.EVT_MENU, self.onChart, id=self.ID_Chart)
		if self.radix != None:
			self.Bind(wx.EVT_MENU, self.onComparison, id=self.ID_Comparison)
		self.Bind(wx.EVT_MENU, self.onPositions, id=self.ID_Positions)
#		self.Bind(wx.EVT_MENU, self.onSquare, id=self.ID_Square)
		self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
		self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)

		if self.options.bw:
			self.mbw.Check()

		self.w = mundanewnd.MundaneWnd(self, parent, self.options, self.chart, self.radix)
		self.chartmenu.Check()


	def onPopupMenu(self, event):
		self.PopupMenu(self.pmenu, event.GetPosition())


	def onChart(self, event):
		if self.selection != MundaneFrame.CHART:
			self.selection = MundaneFrame.CHART
			self.w.Destroy()
			self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, self.radix, -1, self.GetClientSize())


	def onComparison(self, event):
		if self.selection != MundaneFrame.COMPOUND:
			self.selection = MundaneFrame.COMPOUND
			self.w.Destroy()
			self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, self.radix, -1, self.GetClientSize())


	def onPositions(self, event):
		if self.selection != MundaneFrame.POSITIONS:
			self.selection = MundaneFrame.POSITIONS
			self.w.Destroy()
			if wx.Platform == '__WXMSW__':
				self.w = positionswnd2.PositionsWnd2(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
				self.w.Refresh()
			else:
				self.w = positionswnd.PositionsWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())


#	def onSquare(self, event):
#		if self.selection != MundaneFrame.SQUARE:
#			self.selection = MundaneFrame.SQUARE
#			self.w.Destroy()
#			self.w = squarechartwnd.SquareChartWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())


	def onSaveAsBitmap(self, event):
		self.w.onSaveAsBitmap(event)


	def onBlackAndWhite(self, event):
		self.w.onBlackAndWhite(event)





