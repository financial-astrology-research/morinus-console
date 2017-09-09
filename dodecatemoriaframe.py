import wx
import dodecatemoriawnd


class DodecatemoriaFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(300, 480))

		self.w = dodecatemoriawnd.DodecatemoriaWnd(self, chrt, options, parent)
		self.SetMinSize((200,200))


