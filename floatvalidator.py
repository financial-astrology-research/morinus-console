import  wx
import string
import mtexts


class FloatValidator(wx.PyValidator):
	def __init__(self, minim=None, maxim=None):
		wx.PyValidator.__init__(self)
		self.minim = minim
		self.maxim = maxim
		self.Bind(wx.EVT_CHAR, self.OnChar)

	def Clone(self):
 		return FloatValidator(self.minim, self.maxim)

	def TransferToWindow(self):
		return True

	def TransferFromWindow(self):
		return True

	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()

		if (val == ''):
			dlgm = wx.MessageDialog(None, mtexts.txts['FieldsCannotBeEmpty'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()		
			dlgm.Destroy()
			return False

		if ((self.minim != None and float(val) < self.minim) or (self.maxim != None and float(val) >= self.maxim)):
			s = mtexts.txts['RangeError2']
			if (self.maxim != None):
				s = mtexts.txts['RangeError3'] + '%2.1f' % self.maxim
			dlgm = wx.MessageDialog(None, s, mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
			return False	

		return True

	def OnChar(self, event):
		# FIXME: something is wrong with this code, KeyCode
		# behavior has been changed in wxPython 2.8.1?
		#print event, type(event), event.KeyCode
		key = event.KeyCode

		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			event.Skip()
			return

		tc = self.GetWindow()
		val = tc.GetValue()
		dot = False
		for x in val:
			if x == '.':
				dot = True

		if (chr(key) in string.digits or ((not dot) and chr(key) == '.')):
			event.Skip()
			return

		if not wx.Validator_IsSilent():
			wx.Bell()


