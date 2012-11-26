import wx
import string
import mtexts


class IntValidator(wx.PyValidator):
	def __init__(self, minim=None, maxim=None):
		wx.PyValidator.__init__(self)
		self.minim = minim
		self.maxim = maxim
		self.Bind(wx.EVT_CHAR, self.OnChar)

	def Clone(self):
 		return IntValidator(self.minim, self.maxim)

	def TransferToWindow(self):
		return True

	def TransferFromWindow(self):
		return True

	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()

		if (val == ''):
			dlgm = wx.MessageDialog(None, mtexts.txts['NumFieldsCannotBeEmpty'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()		
			dlgm.Destroy()
			return False

		if ((self.minim != None and int(val) < self.minim) or (self.maxim != None and int(val) > self.maxim)):
			dlgm = wx.MessageDialog(None, mtexts.txts['RangeError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
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

		if chr(key) in string.digits:
			event.Skip()
			return

		if not wx.Validator_IsSilent():
			wx.Bell()


