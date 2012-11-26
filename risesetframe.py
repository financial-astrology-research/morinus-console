import wx
import risesetwnd


class RiseSetFrame(wx.Frame):
	XSIZE = 640
	YSIZE = 400
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(RiseSetFrame.XSIZE, RiseSetFrame.YSIZE))

		rw = risesetwnd.RiseSetWnd(self, chrt, options, parent)
		
		self.SetMinSize((200,200))


