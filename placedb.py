import os
import pickle


class PlaceDB:

	class Record:
		NAME = 0
		LON = 1
		LAT = 2
		TZ = 3
		ALT = 4
		MAX_NUM = ALT

		DELIMITER = '\t'
		DELIMITER_NUM = MAX_NUM

		def __init__(self, name, lon, lat, tz, alt):
			self.name = name
			self.lon = lon
			self.lat = lat
			self.tz = tz
			self.alt = alt
		

	FILENAME = os.path.join('Res', 'placedb.dat')

	def __init__(self):
		self.placedb = []


	def add(self, name, lon, lat, tz, alt):
		self.placedb.append(PlaceDB.Record(name, lon, lat, tz, alt))


	def read(self):
		lines = []
		try:
			f = open(PlaceDB.FILENAME, 'rb')
			try:
				while(True):
					lines.append(pickle.load(f))
				f.close()

			except EOFError:
				for ln in lines:
					#remove newline
					ln = ln.rstrip('\n')
					if not self.isValid(ln):
						continue

					line = ln.split(PlaceDB.Record.DELIMITER)
					self.placedb.append(PlaceDB.Record(line[PlaceDB.Record.NAME], line[PlaceDB.Record.LON], line[PlaceDB.Record.LAT], line[PlaceDB.Record.TZ], line[PlaceDB.Record.ALT]))

		except IOError:
			pass


	def write(self):
		try:
			f = open(PlaceDB.FILENAME, 'wb')
			for rec in self.placedb:
				txt = rec.name+PlaceDB.Record.DELIMITER+rec.lon+PlaceDB.Record.DELIMITER+rec.lat+PlaceDB.Record.DELIMITER+rec.tz+PlaceDB.Record.DELIMITER+rec.alt+'\n'
				pickle.dump(txt, f)

			f.close()

		except IOError:
	 		dlg = wx.MessageDialog(self, mtexts.txts['DBFileError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
		

	def sort(self):
		self.placedb = self.qsort(self.placedb)

#		num = len(self.placedb)

#		for j in range(num):
#			for i in range(num-1):
#				if (self.placedb[i].name > self.placedb[i+1].name):
#					tmp = self.placedb[i]
#					self.placedb[i] = self.placedb[i+1]
#					self.placedb[i+1] = tmp


	def qsort(self, L):
		if L == []: return []
		return self.qsort([x for x in L[1:] if x.name < L[0].name]) + L[0:1] + self.qsort([x for x in L[1:] if x.name >= L[0].name])



	def isValid(self, ln):
		valid = True
		if ln == '':
			valid = False
		else:
			if ln.count(PlaceDB.Record.DELIMITER) != PlaceDB.Record.DELIMITER_NUM:
				valid = False
			#else #here can be more checking...

		return valid



