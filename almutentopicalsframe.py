import wx
import chart
import almutentopicalswnd
import mtexts
import util


class AlmutenTopicalsFrame(wx.Frame):

	def __init__(self, parent, chrt, title):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, size=wx.Size(640, 400))

		self.parent = parent
		self.chart = chrt

		#Navigating toolbar
		self.tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT)

		self.namescb = wx.ComboBox(self.tb, -1, self.chart.almutens.topicals.names[0], size=(230, -1), choices=self.chart.almutens.topicals.names, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.namescb.SetSelection(0)
		self.tb.AddControl(self.namescb)

		self.tb.Realize()

		self.SetMinSize((200,200))

		self.Bind(wx.EVT_COMBOBOX, self.onChange, id=self.namescb.GetId())
		self.w = almutentopicalswnd.AlmutenTopicalsWnd(self, chrt, 0, parent, -1, self.GetClientSize()) #parent is mainframe, -1 is id


	def onChange(self, event):
		idx = self.namescb.GetCurrentSelection()
		self.w.Destroy()
		self.w = almutentopicalswnd.AlmutenTopicalsWnd(self, self.chart, idx, self.parent, -1, self.GetClientSize()) #parent is mainframe, -1 is id
		self.w.Refresh()
		


