import transitframe
import common
import mtexts
import util


class ProfectionsFrame(transitframe.TransitFrame):
	def __init__(self, parent, title, chrt, radix, options):
		transitframe.TransitFrame.__init__(self, parent, title, chrt, radix, options)


	def change(self, chrt, title, y, m, d, t):
		self.chart = chrt
		self.w.chart = chrt
		self.w.drawBkg()
		self.w.Refresh()

		#Update Caption
		h, mi, s = util.decToDeg(t)
		title = title.replace(mtexts.txts['Radix'], mtexts.txts['Profections']+' ('+str(y)+'.'+common.common.months[m-1]+'.'+str(d)+' '+str(h)+':'+str(mi).zfill(2)+':'+str(s).zfill(2)+')')
		self.SetTitle(title)






