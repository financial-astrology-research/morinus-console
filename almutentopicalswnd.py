import wx
import os
import astrology
import planets
import chart
import houses
import fortune
import almutens
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class AlmutenTopicalsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, idx, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, chrt.options, id, size)
		
		self.idx = idx
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		#essentials
		self.LINE_NUM = len(self.chart.almutens.topicals.collections[idx])# +2(Shares and Scores)
		self.DLINE_HEIGHT = 2*self.LINE_HEIGHT
		self.COLUMN_NUM = 7# +leftmost +degreewins
		self.LONGITUDE_CELL_WIDTH = 7*self.FONT_SIZE
		self.DEGREEWINS_CELL_WIDTH = 7*self.FONT_SIZE
		self.CELL_WIDTH = 7*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TABLE_WIDTH = (self.LONGITUDE_CELL_WIDTH+(self.COLUMN_NUM)*(self.CELL_WIDTH)+self.DEGREEWINS_CELL_WIDTH)
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+(self.LINE_NUM*self.LINE_HEIGHT+2*self.DLINE_HEIGHT))

		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.fntLargeText = ImageFont.truetype(common.common.abc, 5*self.FONT_SIZE/4)
		self.fntBigText = ImageFont.truetype(common.common.abc, 3*self.FONT_SIZE/2)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Alm']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		x = BOR
		y = BOR
		draw.rectangle(((x, y), (x+self.TABLE_WIDTH, y+self.TABLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

		x = BOR
		y = BOR+self.TITLE_HEIGHT
		for i in range(self.LINE_NUM+1):
			draw.line((x, y+i*self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+i*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x, y+i*self.LINE_HEIGHT+self.DLINE_HEIGHT, x+self.TABLE_WIDTH, y+i*self.LINE_HEIGHT+self.DLINE_HEIGHT), fill=tableclr)

		x = BOR+self.LONGITUDE_CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT
		draw.line((x, y, x, y+self.TABLE_HEIGHT-self.TITLE_HEIGHT), fill=tableclr)
		for i in range(self.COLUMN_NUM+1):
			draw.line((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH, y, x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH, y+self.TABLE_HEIGHT-self.TITLE_HEIGHT), fill=tableclr)

		x = BOR+self.LONGITUDE_CELL_WIDTH
		y = BOR
		for i in range(astrology.SE_SATURN+1):
			clr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			txt = common.common.Planets[i]
			w,h = draw.textsize(txt, self.fntMorinus)
			draw.text((x+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

		txt = mtexts.txts['DegreeWins']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+7*self.CELL_WIDTH+(self.DEGREEWINS_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT
		for i in range(self.LINE_NUM):
			lon = self.chart.almutens.topicals.collections[self.idx][i]
			self.drawLong(draw, x, y+i*self.LINE_HEIGHT, lon, txtclr)

			for j in range(astrology.SE_SATURN+1):
				txt = self.chart.almutens.topicals.data[self.idx][j][i][0]
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+self.LONGITUDE_CELL_WIDTH+j*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.LINE_NUM*self.LINE_HEIGHT
		txt = mtexts.txts['TotalShares1']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.LONGITUDE_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
		txt = mtexts.txts['TotalShares2']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.LONGITUDE_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		y += self.DLINE_HEIGHT
		txt = mtexts.txts['TotalScores1']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.LONGITUDE_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
		txt = mtexts.txts['TotalScores2']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.LONGITUDE_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR+self.LONGITUDE_CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+self.LINE_NUM*self.LINE_HEIGHT
		for i in range(astrology.SE_SATURN+1):
			fnt = self.fntLargeText
			if self.chart.almutens.topicals.maxshare[self.idx][0] != -1 and self.chart.almutens.topicals.maxshare[self.idx][0] == i and (not self.chart.almutens.topicals.maxshare[self.idx][2]):
				fnt = self.fntBigText
			txt = str(self.chart.almutens.topicals.shares[self.idx][i])
			w,h = draw.textsize(txt, fnt)
			draw.text((x+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(self.DLINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		y += self.DLINE_HEIGHT
		for i in range(astrology.SE_SATURN+1):
			fnt = self.fntLargeText
			if self.chart.almutens.topicals.maxscore[self.idx][0] != -1 and self.chart.almutens.topicals.maxscore[self.idx][0] == i and (not self.chart.almutens.topicals.maxscore[self.idx][2]):
				fnt = self.fntBigText
			txt = str(self.chart.almutens.topicals.scores[self.idx][i])
			w,h = draw.textsize(txt, fnt)
			draw.text((x+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(self.DLINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		#degree winner
		x = BOR+self.LONGITUDE_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT
		num = len(self.chart.almutens.topicals.degwinner[self.idx])
		for i in range(num):
			aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
			subnum = len(self.chart.almutens.topicals.degwinner[self.idx][0])
			mwidth = 0
			for j in range(subnum):
				pid = self.chart.almutens.topicals.degwinner[self.idx][i][j][0]
				if pid != -1:
					ptxt = common.common.Planets[pid]
					wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
					sco = self.chart.almutens.topicals.degwinner[self.idx][i][0][1]
					txt = '('+str(sco)+')'
					w,h = draw.textsize(txt, self.fntText)
					wsp,hsp = draw.textsize(' ', self.fntText)
					aux[j][0] = pid
					aux[j][1] = sco
					aux[j][2] = wpl+wsp+w
					if mwidth != 0:
						mwidth += wsp
					mwidth += wpl+wsp+w
				else:
					break
			
			for j in range(subnum):
				if aux[j][0] != -1:
					clr = (0, 0, 0)
					if not self.bw:
						if self.options.useplanetcolors:
							clr = self.options.clrindividual[aux[j][0]]
						else:
							dign = self.chart.dignity(aux[j][0])
							clr = self.clrs[dign]
					pltxt = common.common.Planets[aux[j][0]]
					wpl,hpl = draw.textsize(pltxt, self.fntMorinus)
					txt = '('+str(aux[j][1])+')'
					wsp,hsp = draw.textsize(' ', self.fntText)
					w,h = draw.textsize(txt, self.fntText)
					prev = 0
					for p in range(j):
						prev += aux[j][2]+wsp

					draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
					draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawLong(self, draw, x, y, lon, clr):
		if self.options.ayanamsha != 0:
			lon -= self.chart.ayanamsha
			lon = util.normalize(lon)

		d,m,s = util.decToDeg(lon)

		sign = d/chart.Chart.SIGN_DEG
		pos = d%chart.Chart.SIGN_DEG
		wsp,hsp = draw.textsize(' ', self.fntText)
		wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
		txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
		w,h = draw.textsize(txt, self.fntText)
		offset = (self.LONGITUDE_CELL_WIDTH-(w+wsp+wsg))/2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)
		draw.text((x+offset+w+wsp, y+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clr, font=self.fntMorinus)



