import wx
import almutenzodswnd


class AlmutenZodsFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		aw = almutenzodswnd.AlmutenZodsWnd(self, chrt, options, parent)
		
		self.SetMinSize((200,200))


