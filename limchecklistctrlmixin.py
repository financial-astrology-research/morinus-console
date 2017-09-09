import wx


class LimCheckListCtrlMixin:
	def __init__(self, lim, check_image=None, uncheck_image=None, imgsz=(16,16)):
		self.lim = lim
		self.checkednum = 0

		if check_image is not None:
			imgsz = check_image.GetSize()
		elif uncheck_image is not None:
			imgsz = check_image.GetSize()

		self.__imagelist_ = wx.ImageList(*imgsz)

		# Create default checkbox images if none were specified
		if check_image is None:
			check_image = self.__CreateBitmap(wx.CONTROL_CHECKED, imgsz)

		if uncheck_image is None:
			uncheck_image = self.__CreateBitmap(0, imgsz)

		self.uncheck_image = self.__imagelist_.Add(uncheck_image)
		self.check_image = self.__imagelist_.Add(check_image)
		self.SetImageList(self.__imagelist_, wx.IMAGE_LIST_SMALL)
		self.__last_check_ = None

		self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown_)
        
		# override the default methods of ListCtrl/ListView
		self.InsertStringItem = self.__InsertStringItem_

	def __CreateBitmap(self, flag=0, size=(16, 16)):
		"""Create a bitmap of the platforms native checkbox. The flag
		is used to determine the checkboxes state (see wx.CONTROL_*)

		"""
		bmp = wx.EmptyBitmap(*size)
		dc = wx.MemoryDC(bmp)
		dc.Clear()
		wx.RendererNative.Get().DrawCheckBox(self, dc, (0, 0, size[0], size[1]), flag)
		dc.SelectObject(wx.NullBitmap)
		return bmp

	# NOTE: if you use InsertItem, InsertImageItem or InsertImageStringItem,
	#       you must set the image yourself.
	def __InsertStringItem_(self, index, label):
		index = self.InsertImageStringItem(index, label, 0)
		return index

	def __OnLeftDown_(self, evt):
		(index, flags) = self.HitTest(evt.GetPosition())
		if flags == wx.LIST_HITTEST_ONITEMICON:
			img_idx = self.GetItem(index).GetImage()
			flag_check = img_idx == 0
			self.CheckItem(index, flag_check)
		else:
			evt.Skip()

	def OnCheckItem(self, index, flag):
		pass

	def IsChecked(self, index):
		return self.GetItem(index).GetImage() == 1

	def CheckItem(self, index, check = True):
		img_idx = self.GetItem(index).GetImage()
		if img_idx == 0 and check is True:
			if self.lim > self.checkednum:
				self.SetItemImage(index, 1)
				self.OnCheckItem(index, True)
				self.checkednum += 1
		elif img_idx == 1 and check is False:
			self.SetItemImage(index, 0)
			self.OnCheckItem(index, False)
			if self.checkednum > 0:
				self.checkednum -= 1

	def ToggleItem(self, index):
		self.CheckItem(index, not self.IsChecked(index))


