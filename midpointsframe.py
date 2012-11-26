import wx
import midpointswnd


class MidPointsFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		sw = midpointswnd.MidPointsWnd(self, chrt, options, parent)
		
		self.SetMinSize((200,200))


