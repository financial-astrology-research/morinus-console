import  wx
import Image, ImageDraw, ImageFont
import common
import mtexts


class SymbolsDlg(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Symbols'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

		SIZE = 32
		DIFF = 8
		bkg = (255,255,255)
		fntMorinus = ImageFont.truetype(common.common.symbols, SIZE-DIFF)

		#Uranus
		bmpuranus = [None, None]
		for i in range(len(common.common.Uranus)):
			bmpuranus[i] = wx.EmptyBitmap(SIZE, SIZE)
			bdc = wx.BufferedDC(None, bmpuranus[i])
			bdc.SetBackground(wx.Brush(bkg))
			bdc.Clear()
			wxImag = bmpuranus[i].ConvertToImage()
			img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
			img.fromstring(wxImag.GetData())
			draw = ImageDraw.Draw(img)
			draw.text((DIFF/2, DIFF/2), common.common.Uranus[i], fill=(0,0,0), font=fntMorinus)
			wxImg = wx.EmptyImage(img.size[0], img.size[1])
			wxImg.SetData(img.tostring())
			bmpuranus[i] = wx.BitmapFromImage(wxImg)

		#Pluto
		bmppluto = [None, None, None, None]
		for i in range(len(common.common.Pluto)):
			bmppluto[i] = wx.EmptyBitmap(SIZE, SIZE)
			bdc = wx.BufferedDC(None, bmppluto[i])
			bdc.SetBackground(wx.Brush(bkg))
			bdc.Clear()
			wxImag = bmppluto[i].ConvertToImage()
			img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
			img.fromstring(wxImag.GetData())
			draw = ImageDraw.Draw(img)
			draw.text((DIFF/2, DIFF/2), common.common.Pluto[i], fill=(0,0,0), font=fntMorinus)
			wxImg = wx.EmptyImage(img.size[0], img.size[1])
			wxImg.SetData(img.tostring())
			bmppluto[i] = wx.BitmapFromImage(wxImg)

		#Signs
		#Docs say that on Win9X StaticBitmaps can't be bigger than 64*64
		txt = (common.common.Signs1, common.common.Signs2)
		bmpsigns = [[None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None]]
		for i in range(len(txt)):
			for j in range(len(txt[i])):
				bmpsigns[i][j] = wx.EmptyBitmap(SIZE, SIZE)
				bdc = wx.BufferedDC(None, bmpsigns[i][j])
				bdc.SetBackground(wx.Brush(bkg))
				bdc.Clear()
				wxImag = bmpsigns[i][j].ConvertToImage()
				img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
				img.fromstring(wxImag.GetData())
				draw = ImageDraw.Draw(img)
				draw.text((DIFF/2, DIFF/2), txt[i][j], fill=(0,0,0), font=fntMorinus)
				wxImg = wx.EmptyImage(img.size[0], img.size[1])
				wxImg.SetData(img.tostring())
				bmpsigns[i][j] = wx.BitmapFromImage(wxImg)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		#main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		suranus = wx.StaticBox(self, label='')
		uranussizer = wx.StaticBoxSizer(suranus, wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(2, 2)
		self.uranus1 = wx.RadioButton(self, -1, "", style=wx.RB_GROUP)
		fgsizer.Add(self.uranus1, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmpuranus1 = wx.StaticBitmap(self, -1, bmpuranus[0])
		fgsizer.Add(sbmpuranus1, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.uranus2 = wx.RadioButton(self, -1, "")
		fgsizer.Add(self.uranus2, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmpuranus2 = wx.StaticBitmap(self, -1, bmpuranus[1])
		fgsizer.Add(sbmpuranus2, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		uranussizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(uranussizer, 0, wx.ALIGN_LEFT, 0)

		spluto = wx.StaticBox(self, label='')
		plutosizer = wx.StaticBoxSizer(spluto, wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(4, 2)
		self.pluto1 = wx.RadioButton(self, -1, "", style=wx.RB_GROUP)
		fgsizer.Add(self.pluto1, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmppluto1 = wx.StaticBitmap(self, -1, bmppluto[0])
		fgsizer.Add(sbmppluto1, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.pluto2 = wx.RadioButton(self, -1, "")
		fgsizer.Add(self.pluto2, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmppluto2 = wx.StaticBitmap(self, -1, bmppluto[1])
		fgsizer.Add(sbmppluto2, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.pluto3 = wx.RadioButton(self, -1, "")
		fgsizer.Add(self.pluto3, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmppluto3 = wx.StaticBitmap(self, -1, bmppluto[2])
		fgsizer.Add(sbmppluto3, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		self.pluto4 = wx.RadioButton(self, -1, "")
		fgsizer.Add(self.pluto4, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		sbmppluto4 = wx.StaticBitmap(self, -1, bmppluto[3])
		fgsizer.Add(sbmppluto4, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		plutosizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer.Add(plutosizer, 0, wx.ALIGN_LEFT, 0)

		mhsizer.Add(vsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)

		ssigns = wx.StaticBox(self, label='')
		signssizer = wx.StaticBoxSizer(ssigns, wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(2, 2)
		self.signs1 = wx.RadioButton(self, -1, "", style=wx.RB_GROUP)
		fgsizer.Add(self.signs1, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		subfgsizer = wx.FlexGridSizer(3, 4)
		for i in range(len(txt[0])):
			bmp = wx.StaticBitmap(self, -1, bmpsigns[0][i])
			subfgsizer.Add(bmp, 0, wx.ALIGN_LEFT)

		fgsizer.Add(subfgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		self.signs2 = wx.RadioButton(self, -1, "")
		fgsizer.Add(self.signs2, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		subfgsizer = wx.FlexGridSizer(3, 4)
		for i in range(len(txt[1])):
			bmp = wx.StaticBitmap(self, -1, bmpsigns[1][i])
			subfgsizer.Add(bmp, 0, wx.ALIGN_LEFT)

		fgsizer.Add(subfgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		signssizer.Add(fgsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		mhsizer.Add(signssizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT, 5)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)

		btnsizer.Realize()
		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()


	def fill(self, options):
		if options.uranus:
			self.uranus1.SetValue(True)
		else:
			self.uranus2.SetValue(True)

		if options.pluto == 0:
			self.pluto1.SetValue(True)
		elif options.pluto == 1:
			self.pluto2.SetValue(True)
		elif options.pluto == 2:
			self.pluto3.SetValue(True)
		elif options.pluto == 3:
			self.pluto4.SetValue(True)

		if options.signs:
			self.signs1.SetValue(True)
		else:
			self.signs2.SetValue(True)		


	def check(self, options):
		changed = False

		#save to options
		if options.uranus != self.uranus1.GetValue():
			options.uranus = self.uranus1.GetValue()
			changed = True

		if self.pluto1.GetValue() and options.pluto != 0:
			options.pluto = 0
			changed = True
		if self.pluto2.GetValue() and options.pluto != 1:
			options.pluto = 1
			changed = True
		if self.pluto3.GetValue() and options.pluto != 2:
			options.pluto = 2
			changed = True
		if self.pluto4.GetValue() and options.pluto != 3:
			options.pluto = 3
			changed = True

		if options.signs != self.signs1.GetValue():
			options.signs = self.signs1.GetValue()
			changed = True

		return changed


