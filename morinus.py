#!/usr/bin/env python


#Morinus, Astrology program
#Copyright (C) 2008-  Robert Nagy, robert.pluto@gmail.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import wx
import options
import mtexts
import morin


class Morinus(wx.App):
	def OnInit(self):
		try:
			progPath = os.path.dirname(sys.argv[0])
			os.chdir(progPath)
		except:
			pass

		wx.SetDefaultPyEncoding('utf-8')
		opts = options.Options()
		mtexts.setLang(opts.langid)

		frame = morin.MFrame(None, -1, mtexts.txts['Morinus'], opts)
		frame.Show(True)

		return True

 
app = Morinus(0)
app.MainLoop()



