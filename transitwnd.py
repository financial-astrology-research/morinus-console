import wx
import os
import chart
import graphchart
import graphchart2
import mtexts


class TransitWnd(wx.Window):
	def __init__(self, parent, chrt, radix, options, mainfr, compound = False, id = -1, size = wx.DefaultSize):
		wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size)

		self.parent = parent
		self.chart = chrt
		self.radix = radix
		self.options = options
		self.mainfr = mainfr
		self.compound = compound

		self.bw = self.options.bw

		self.SetMinSize((200,200))

		self.parent.mbw.Check(self.bw)

		self.SetBackgroundColour(self.options.clrbackground)

		self.drawBkg()

		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.onSize)
#		self.Refresh()


	def drawBkg(self):
		gchart = None
		if self.compound:
			if self.options.theme == 0:
				gchart = graphchart.GraphChart(self.radix, self.GetClientSize(), self.options, self.bw, False, self.chart)
			else:
				gchart = graphchart2.GraphChart2(self.radix, self.GetClientSize(), self.options, self.bw, False, self.chart)
		else:
			if self.options.theme == 0:
				gchart = graphchart.GraphChart(self.chart, self.GetClientSize(), self.options, self.bw, False, None)
			else:
				gchart = graphchart2.GraphChart2(self.chart, self.GetClientSize(), self.options, self.bw, False, None)

		self.buffer = gchart.drawChart()
		self.Refresh()#


	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)


	def onPopupMenu(self, event):
		self.parent.onPopupMenu(event)


	def onSaveAsBitmap(self, event):
		name = self.chart.name+(mtexts.typeList[self.chart.htype][0:3]).capitalize()
		dlg = wx.FileDialog(self, mtexts.txts['SaveAsBmp'], '', name, mtexts.txts['BMPFiles'], wx.FD_SAVE)
		if os.path.isdir(self.mainfr.fpathimgs):
			dlg.SetDirectory(self.mainfr.fpathimgs)
		else:
			dlg.SetDirectory(u'.')

		if (dlg.ShowModal() == wx.ID_OK):
			dpath = dlg.GetDirectory()
			fpath = dlg.GetPath()
			if (not fpath.endswith(u'.bmp')):
				fpath+=u'.bmp'
			#Check if fpath already exists!?
			if (os.path.isfile(fpath)):
 				dlgm = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
				if (dlgm.ShowModal() == wx.ID_NO):
					dlgm.Destroy()
					dlg.Destroy()
					return
				dlgm.Destroy()

			self.mainfr.fpathimgs = dpath
			self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_BMP)

		dlg.Destroy()


	def onBlackAndWhite(self, event):
		if self.bw != event.IsChecked():
			self.bw = event.IsChecked()
			self.drawBkg()
			self.Refresh()


	def onSize(self, event):
		self.drawBkg()



