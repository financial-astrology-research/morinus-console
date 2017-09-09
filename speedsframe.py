import wx
import speedswnd


class SpeedsFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		sw = speedswnd.SpeedsWnd(self, chrt, options, parent)
		
		self.SetMinSize((200,200))


