import wx
import chart
import positionswnd
import positionswnd2
import transitwnd
import mundanewnd
import squarechartwnd
import mtexts


class PDsInChartFrame(wx.Frame):
	CHART = 0
	COMPOUND = 1
	POSITIONS = 2
	SQUARE = 3

	def __init__(self, parent, title, chrt, radix, options, sel=0, zod = True):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		self.chart = chrt
		self.radix = radix
		self.options = options
		self.parent = parent
		self.title = title
		self.zod = zod

		self.pmenu = wx.Menu()
		self.ID_Selection = wx.NewId()
		self.ID_PrimaryDirections = wx.NewId()
		self.ID_SaveAsBitmap = wx.NewId()
		self.ID_BlackAndWhite = wx.NewId()

		self.ID_Chart = wx.NewId()
		self.ID_Comparison = wx.NewId()
		self.ID_Positions = wx.NewId()
		self.ID_Square = wx.NewId()

		self.selmenu = wx.Menu()
		self.chartmenu = self.selmenu.Append(self.ID_Chart, mtexts.txts['Chart'], '', wx.ITEM_RADIO)
		self.compoundmenu = self.selmenu.Append(self.ID_Comparison, mtexts.txts['Comparison'], '', wx.ITEM_RADIO)
		self.positionsmenu = self.selmenu.Append(self.ID_Positions, mtexts.txts['Positions'], '', wx.ITEM_RADIO)
		if self.zod:
			self.squaremenu = self.selmenu.Append(self.ID_Square, mtexts.txts['Square'], '', wx.ITEM_RADIO)

		self.pmenu.AppendMenu(self.ID_Selection, mtexts.txts['Windows'], self.selmenu)

		self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txts['SaveAsBmp'], mtexts.txts['SaveChart'])
		self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txts['BlackAndWhite'], mtexts.txts['ChartBW'], wx.ITEM_CHECK)
		
		self.SetMinSize((200,200))

		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)

		self.Bind(wx.EVT_MENU, self.onChart, id=self.ID_Chart)
		self.Bind(wx.EVT_MENU, self.onComparison, id=self.ID_Comparison)
		self.Bind(wx.EVT_MENU, self.onPositions, id=self.ID_Positions)
		if self.zod:
			self.Bind(wx.EVT_MENU, self.onSquare, id=self.ID_Square)
		self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
		self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)

		if self.options.bw:
			self.mbw.Check()

		self.selection = sel
		if sel == PDsInChartFrame.CHART:
			if self.zod:
				self.w = transitwnd.TransitWnd(self, self.chart, self.radix, options, parent)
			else:
				self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, None)
			self.chartmenu.Check()
		else:
			if self.zod:
				self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True)
			else:
				self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, self.radix)
			self.compoundmenu.Check()


	def onPopupMenu(self, event):
		self.PopupMenu(self.pmenu, event.GetPosition())


	def onChart(self, event):
		if self.selection != PDsInChartFrame.CHART:
			self.selection = PDsInChartFrame.CHART
			self.w.Destroy()
			if self.zod:
				self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, False, -1, self.GetClientSize())
			else:
				self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, None, -1, self.GetClientSize())


	def onComparison(self, event):
		if self.selection != PDsInChartFrame.COMPOUND:
			self.selection = PDsInChartFrame.COMPOUND
			self.w.Destroy()
			if self.zod:
				self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True, -1, self.GetClientSize())
			else:
				self.w = mundanewnd.MundaneWnd(self, self.parent, self.options, self.chart, self.radix, -1, self.GetClientSize())


	def onPositions(self, event):
		if self.selection != PDsInChartFrame.POSITIONS:
			self.selection = PDsInChartFrame.POSITIONS
			self.w.Destroy()
			if wx.Platform == '__WXMSW__':
				self.w = positionswnd2.PositionsWnd2(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
				self.w.Refresh()
			else:
				self.w = positionswnd.PositionsWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())


	def onSquare(self, event):
		if self.selection != PDsInChartFrame.SQUARE:
			self.selection = PDsInChartFrame.SQUARE
			self.w.Destroy()
			self.w = squarechartwnd.SquareChartWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())


	def change(self, chrt, y, m, d, ho, mi, se, pdtypetxt, pdkeytxt, txtdir, da):
		self.chart = chrt
		self.w.chart = chrt
		self.w.drawBkg()
		self.w.Refresh()

		#Update Caption
		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		self.SetTitle(txt)


	def onSaveAsBitmap(self, event):
		self.w.onSaveAsBitmap(event)


	def onBlackAndWhite(self, event):
		self.w.onBlackAndWhite(event)








