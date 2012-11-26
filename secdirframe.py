import transitframe
import common
import mtexts


class SecDirFrame(transitframe.TransitFrame):
	def __init__(self, parent, title, chrt, radix, options):
		transitframe.TransitFrame.__init__(self, parent, title, chrt, radix, options)


	def change(self, chrt, title):
		self.chart = chrt
		self.w.chart = chrt
		self.w.drawBkg()
		self.w.Refresh()

		#Update Caption
		title = title.replace(mtexts.txts['Radix'], mtexts.txts['SecondaryDir']+' ('+str(self.chart.time.year)+'.'+common.common.months[self.chart.time.month-1]+'.'+str(self.chart.time.day)+' '+str(self.chart.time.hour)+':'+str(self.chart.time.minute).zfill(2)+':'+str(self.chart.time.second).zfill(2)+')')
		self.SetTitle(title)






