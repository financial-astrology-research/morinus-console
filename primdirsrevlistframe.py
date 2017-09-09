import wx
import chart
import primdirslistwnd
import intvalidator
import mtexts
import util


class PrimDirsRevListFrame(wx.Frame):
	def __init__(self, parent, mainfr, chrt, options, pds, title):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, size=wx.Size(640, 400))

		self.parent = parent
		self.mainfr = mainfr
		self.chart = chrt
		self.pdrange = pds.pdrange
		self.direction = pds.direction

		#Navigating toolbar
		self.tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT)

		tsize = (24,24)
		tostart_bmp =  wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, tsize)
		back_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR, tsize)
		forward_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tsize)
		toend_bmp= wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, tsize)

		self.tb.SetToolBitmapSize(tsize)
      
		self.ID_Start = 10
		self.tb.AddLabelTool(10, "Start", tostart_bmp, shortHelp=mtexts.txts["Start"], longHelp=mtexts.txts["ToFirstPage"])
		self.Bind(wx.EVT_TOOL, self.OnStart, id=self.ID_Start)

		self.ID_Back = 20
		self.tb.AddLabelTool(20, "Back", back_bmp, shortHelp=mtexts.txts["Back"], longHelp=mtexts.txts["ToBackPage"])
		self.Bind(wx.EVT_TOOL, self.OnBack, id=self.ID_Back)

		self.ID_Forward = 30
		self.tb.AddLabelTool(30, "Forward", forward_bmp, shortHelp=mtexts.txts["Forward"], longHelp=mtexts.txts["ToForwardPage"])
		self.Bind(wx.EVT_TOOL, self.OnForward, id=self.ID_Forward)

		self.ID_End = 40
		self.tb.AddLabelTool(40, "End", toend_bmp, shortHelp=mtexts.txts["End"], longHelp=mtexts.txts["ToLastPage"])
		self.Bind(wx.EVT_TOOL, self.OnEnd, id=self.ID_End)

#		self.tb.AddSeparator()

		self.tb.Realize()

		self.initTB(chrt, options, pds, mainfr)

		self.SetMinSize((200,200))


	def initTB(self, chrt, options, pds, mainfr):
		self.pdsmaxnum = len(pds.pds)

		self.currpage = 1
		self.LINE_NUM = 40 #per column
		self.PAGE = self.LINE_NUM*2
		remainder = self.pdsmaxnum%self.PAGE
		addition = 0
		if remainder > 0:
			addition = 1
		self.maxpage = int(self.pdsmaxnum/self.PAGE)+addition
		fr, to = self.getRange()
		self.w = primdirslistwnd.PrimDirsListWnd(self, chrt, options, pds, mainfr, 1, self.maxpage, fr, to, -1, self.GetClientSize()) #pdsmaxnum -> maxpage

		self.tb.EnableTool(self.ID_Start, False)
		self.tb.EnableTool(self.ID_Back, False)
		if self.maxpage == 1:
			self.tb.EnableTool(self.ID_End, False)
			self.tb.EnableTool(self.ID_Forward, False)
		else:
			self.tb.EnableTool(self.ID_End, True)
			self.tb.EnableTool(self.ID_Forward, True)


	def OnStart(self, event):
		if self.currpage != 1:
			wait = wx.BusyCursor()
			self.currpage = 1
			self.tb.EnableTool(self.ID_Start, False)
			self.tb.EnableTool(self.ID_Back, False)
			self.tb.EnableTool(self.ID_End, True)
			self.tb.EnableTool(self.ID_Forward, True)
			fr, to = self.getRange()
			self.w.display(self.currpage, fr, to)


	def OnBack(self, event):
		if self.currpage != 1:
			wait = wx.BusyCursor()
			self.currpage -= 1
			self.tb.EnableTool(self.ID_Start, self.currpage != 1)
			self.tb.EnableTool(self.ID_Back, self.currpage != 1)
			self.tb.EnableTool(self.ID_End, True)
			self.tb.EnableTool(self.ID_Forward, True)
			fr, to = self.getRange()
			self.w.display(self.currpage, fr, to)


	def OnForward(self, event):
		if self.currpage != self.maxpage:
			wait = wx.BusyCursor()
			self.currpage += 1
			self.tb.EnableTool(self.ID_End, self.currpage != self.maxpage)
			self.tb.EnableTool(self.ID_Forward, self.currpage != self.maxpage)
			self.tb.EnableTool(self.ID_Start, True)
			self.tb.EnableTool(self.ID_Back, True)
			fr, to = self.getRange()
			self.w.display(self.currpage, fr, to)


	def OnEnd(self, event):
		if self.currpage != self.maxpage:
			wait = wx.BusyCursor()
			self.currpage = self.maxpage
			self.tb.EnableTool(self.ID_End, False)
			self.tb.EnableTool(self.ID_Forward, False)
			self.tb.EnableTool(self.ID_Start, True)
			self.tb.EnableTool(self.ID_Back, True)
			fr, to = self.getRange()
			self.w.display(self.currpage, fr, to)


	def getRange(self):
		fr = (self.currpage-1)*self.PAGE
		to = self.currpage*self.PAGE
		if to > self.pdsmaxnum:
			to = self.pdsmaxnum

		return fr, to





