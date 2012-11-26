import wx
import stripwnd


class StripFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		self.w = stripwnd.StripWnd(self, chrt, options, parent)
		self.SetMinSize((200,200))


