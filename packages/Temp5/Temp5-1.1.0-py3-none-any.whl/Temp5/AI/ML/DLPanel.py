# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):

	def __init__(self, parent, pnl=[], id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(572, 420), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
		wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		self.pnl = pnl

		self.Titr1 = wx.StaticText( self, wx.ID_ANY, u"Define Models and Layers", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Titr1.Wrap( -1 )

		Vsz1.Add( self.Titr1, 0, wx.ALL, 5 )

		self.P1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz2 = wx.BoxSizer( wx.VERTICAL )

		self.TLC1 = wx.dataview.TreeListCtrl( self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE )
		self.TLC1.AppendColumn( u"Col1", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.TLC1.AppendColumn( u"Col2", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )

		Vsz2.Add( self.TLC1, 1, wx.EXPAND |wx.ALL, 5 )


		self.P1.SetSizer( Vsz2 )
		self.P1.Layout()
		Vsz2.Fit( self.P1 )
		Vsz1.Add( self.P1, 1, wx.EXPAND |wx.ALL, 5 )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		MChsChoices = [ u"Sequential", u"Functional" ]
		self.MChs = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, MChsChoices, 0 )
		self.MChs.SetSelection( 1 )
		Hsz1.Add( self.MChs, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt1 = wx.StaticText( self, wx.ID_ANY, u"Models", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt1.Wrap( -1 )

		Hsz1.Add( self.txt1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lin1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		Hsz1.Add( self.lin1, 0, wx.EXPAND |wx.ALL, 5 )

		self.fldin = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz1.Add( self.fldin, 0, wx.ALL, 5 )

		self.txt2 = wx.StaticText( self, wx.ID_ANY, u"= Input ( ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt2.Wrap( -1 )

		Hsz1.Add( self.txt2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz1.Add( self.Input, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt3 = wx.StaticText( self, wx.ID_ANY, u")", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt3.Wrap( -1 )

		Hsz1.Add( self.txt3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz1, 0, wx.EXPAND, 5 )

		self.P2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz3 = wx.BoxSizer( wx.VERTICAL )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.btnm1 = wx.Button( self.P2, wx.ID_ANY, u"Conv2D", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnm2 = wx.Button( self.P2, wx.ID_ANY, u"Danse", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnm3 = wx.Button( self.P2, wx.ID_ANY, u"Flotten", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnm4 = wx.Button( self.P2, wx.ID_ANY, u"MaxPool2D", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnm5 = wx.Button( self.P2, wx.ID_ANY, u"Dropout", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lin2 = wx.StaticLine( self.P2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		Hsz2.Add( self.lin2, 0, wx.EXPAND |wx.ALL, 5 )

		self.btnm6 = wx.Button( self.P2, wx.ID_ANY, u"VGG16", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnm7 = wx.Button( self.P2, wx.ID_ANY, u"VGG19", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz2.Add( self.btnm7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz3.Add( Hsz2, 1, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		self.fldlay = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.fldlay, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt4 = wx.StaticText( self.P2, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt4.Wrap( -1 )

		Hsz3.Add( self.txt4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.layr = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.layr, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnshw = wx.Button( self.P2, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz3.Add( self.btnshw, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz3.Add( Hsz3, 1, wx.EXPAND, 5 )


		self.P2.SetSizer( Vsz3 )
		self.P2.Layout()
		Vsz3.Fit( self.P2 )
		Vsz1.Add( self.P2, 1, wx.EXPAND |wx.ALL, 5 )

		Hsz4 = wx.BoxSizer( wx.HORIZONTAL )

		self.btnadd = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz4.Add( self.btnadd, 0, wx.ALL, 5 )

		self.btnedt = wx.Button( self, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz4.Add( self.btnedt, 0, wx.ALL, 5 )

		self.btndel = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz4.Add( self.btndel, 0, wx.ALL, 5 )

		self.btnsum = wx.Button( self, wx.ID_ANY, u"Summery", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz4.Add( self.btnsum, 0, wx.ALL, 5 )


		Vsz1.Add( Hsz4, 0, wx.EXPAND, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		# Connect Events
		self.MChs.Bind( wx.EVT_CHOICE, self.chngmodl )
		self.btnm1.Bind( wx.EVT_BUTTON, self.conv )
		self.btnm2.Bind( wx.EVT_BUTTON, self.dans )
		self.btnm3.Bind( wx.EVT_BUTTON, self.flot )
		self.btnm4.Bind( wx.EVT_BUTTON, self.mpool )
		self.btnm5.Bind( wx.EVT_BUTTON, self.drop )
		self.btnm6.Bind( wx.EVT_BUTTON, self.vgg16 )
		self.btnm7.Bind( wx.EVT_BUTTON, self.vgg19 )
		self.btnshw.Bind( wx.EVT_BUTTON, self.shwlyr )
		self.btnadd.Bind( wx.EVT_BUTTON, self.addlyr )
		self.btnedt.Bind( wx.EVT_BUTTON, self.edtlyr )
		self.btndel.Bind( wx.EVT_BUTTON, self.dellyr )
		self.btnsum.Bind( wx.EVT_BUTTON, self.sumodl )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def chngmodl( self, event ):
		if self.MChs.GetSelection() == 0:
			self.fldin.Hide()
			self.fldlay.Hide()
		else:
			self.fldin.Show()
			self.fldlay.Show()
		self.Layout()
		self.Refresh()

		event.Skip()

	def conv( self, event ):
		event.Skip()

	def dans( self, event ):
		event.Skip()

	def flot( self, event ):
		event.Skip()

	def mpool( self, event ):
		event.Skip()

	def drop( self, event ):
		event.Skip()

	def vgg16( self, event ):
		event.Skip()

	def vgg19( self, event ):
		event.Skip()

	def shwlyr( self, event ):
		event.Skip()

	def addlyr( self, event ):
		event.Skip()

	def edtlyr( self, event ):
		event.Skip()

	def dellyr( self, event ):
		event.Skip()

	def sumodl( self, event ):
		event.Skip()
