import wx
import graphephemwnd
import mtexts


class GraphEphemFrame(wx.Frame):
	XSIZE = 640
	YSIZE = 480
	def __init__(self, parent, title, year, posArr, opts):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(GraphEphemFrame.XSIZE, GraphEphemFrame.YSIZE))

		self.options = opts
		self.parent = parent

		self.pmenu = wx.Menu()
		self.ID_SaveAsBitmap = wx.NewId()
		self.ID_BlackAndWhite = wx.NewId()

		self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txts['SaveAsBmp'], mtexts.txts['SaveChart'])
		self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txts['BlackAndWhite'], mtexts.txts['ChartBW'], wx.ITEM_CHECK)
		
		self.w = graphephemwnd.GraphEphemWnd(self, year, posArr, opts, parent)
		self.SetMinSize((200,200))

		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)

		self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
		self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)

		if self.options.bw:
			self.mbw.Check()


	def onPopupMenu(self, event):
		self.PopupMenu(self.pmenu, event.GetPosition())


	def onSaveAsBitmap(self, event):
		self.w.onSaveAsBitmap(event)


	def onBlackAndWhite(self, event):
		self.w.onBlackAndWhite(event)





