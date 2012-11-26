import wx
import customerwnd
import mtexts


class CustomerFrame(wx.Frame):
	def __init__(self, parent, title, chrt, options, cpt):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		self.w = customerwnd.CustomerWnd(self, chrt, options, parent, cpt)
		self.SetMinSize((200,200))





