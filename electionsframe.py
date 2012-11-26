import transitframe
import common
import mtexts


class ElectionsFrame(transitframe.TransitFrame):
	def __init__(self, parent, title, chrt, radix, options):
		transitframe.TransitFrame.__init__(self, parent, title, chrt, radix, options)


	def change(self, chrt, title):
		self.chart = chrt
		self.w.chart = chrt
		self.w.drawBkg()
		self.w.Refresh()

		#Update Caption
		title = title.replace(mtexts.txts['Radix'], mtexts.txts['Elections']+' ('+str(self.chart.time.origyear)+'.'+common.common.months[self.chart.time.origmonth-1]+'.'+str(self.chart.time.origday)+' '+str(self.chart.time.hour)+':'+str(self.chart.time.minute).zfill(2)+':'+str(self.chart.time.second).zfill(2)+')')
		self.SetTitle(title)






