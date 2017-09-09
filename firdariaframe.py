import wx
import firdariawnd


class FirdariaFrame(wx.Frame):
	XSIZE = 570
	YSIZE = 450
	def __init__(self, parent, title, chrt, opts):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(FirdariaFrame.XSIZE, FirdariaFrame.YSIZE))

		self.w = firdariawnd.FirdariaWnd(self, chrt, opts, parent)
		self.SetMinSize((200,200))


