import wx
import profectionswnd


class ProfsTableFrame(wx.Frame):
	def __init__(self, parent, title, pchrts, opts, mainsigs):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))

		self.parent = parent
		self.mainsigs = mainsigs
		self.sw = profectionswnd.ProfectionsWnd(self, 0, pchrts, opts, parent, mainsigs)
		
		self.SetMinSize((200,200))


	def change(self, age, pcharts, opts):
		self.sw.Destroy()
		self.sw = profectionswnd.ProfectionsWnd(self, age, pcharts, opts, self.parent, self.mainsigs, -1, self.GetClientSize())
#		if wx.Platform == '__WXMSW__':
#			self.sw.Refresh()


