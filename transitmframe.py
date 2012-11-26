import wx
import transitmwnd


class TransitMonthFrame(wx.Frame):
	def __init__(self, parent, title, trans, year, month, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		w = transitmwnd.TransitMonthWnd(self, trans, year, month, chrt, options, parent)
		self.SetMinSize((200,200))


