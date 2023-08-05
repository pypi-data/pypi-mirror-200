# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## You Can Edit This File : This is wrong >>> PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 640,450 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		Sb1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"label" ), wx.VERTICAL )

		self.titr = wx.StaticText( Sb1.GetStaticBox(), wx.ID_ANY, u"This is a DEMO", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.titr.Wrap( -1 )

		self.titr.SetFont( wx.Font( 45, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		Sb1.Add( self.titr, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		Hsz1.Add( Sb1, 1, wx.EXPAND, 5 )


		Vsz1.Add( Hsz1, 0, wx.EXPAND, 5 )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.fld = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.fld, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chosChoices = []
		self.chos = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chosChoices, 0 )
		self.chos.SetSelection( 0 )
		Hsz2.Add( self.chos, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chk = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.chk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.rdio = wx.RadioButton( self, wx.ID_ANY, u"RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.rdio, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.sldr = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		Hsz2.Add( self.sldr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.gug = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gug.SetValue( 0 )
		Hsz2.Add( self.gug, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz2, 0, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.bmbtn = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		Hsz3.Add( self.bmbtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.tgbtn = wx.ToggleButton( self, wx.ID_ANY, u"Toggle me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.tgbtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.timpkr = wx.TimePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.TP_DEFAULT )
		Hsz3.Add( self.timpkr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fntpkr = wx.FontPickerCtrl( self, wx.ID_ANY, wx.NullFont, wx.DefaultPosition, wx.DefaultSize, wx.FNTP_DEFAULT_STYLE )
		self.fntpkr.SetMaxPointSize( 100 )
		Hsz3.Add( self.fntpkr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spnbtn = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.spnbtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dirpkr = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
		Hsz3.Add( self.dirpkr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz3, 0, wx.EXPAND, 5 )

		Hsz4 = wx.BoxSizer( wx.HORIZONTAL )

		self.TCR = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		Hsz4.Add( self.TCR, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.grd = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.grd.CreateGrid( 5, 5 )
		self.grd.EnableEditing( True )
		self.grd.EnableGridLines( True )
		self.grd.EnableDragGridSize( False )
		self.grd.SetMargins( 0, 0 )

		# Columns
		self.grd.EnableDragColMove( False )
		self.grd.EnableDragColSize( True )
		self.grd.SetColLabelSize( 30 )
		self.grd.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.grd.EnableDragRowSize( True )
		self.grd.SetRowLabelSize( 80 )
		self.grd.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.grd.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		Hsz4.Add( self.grd, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz4, 0, wx.EXPAND, 5 )

		Hsz5 = wx.BoxSizer( wx.HORIZONTAL )

		self.notbok = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.P1 = wx.Panel( self.notbok, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.notbok.AddPage( self.P1, u"a page", False )
		self.P2 = wx.Panel( self.notbok, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.notbok.AddPage( self.P2, u"a page", False )
		self.P3 = wx.Panel( self.notbok, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.notbok.AddPage( self.P3, u"a page", True )

		Hsz5.Add( self.notbok, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.chsbok = wx.Choicebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		self.P4 = wx.Panel( self.chsbok, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.chsbok.AddPage( self.P4, u"a page", False )
		self.P5 = wx.Panel( self.chsbok, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.chsbok.AddPage( self.P5, u"a page", True )
		Hsz5.Add( self.chsbok, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz5, 1, wx.EXPAND, 5 )

		Hsz6 = wx.BoxSizer(wx.HORIZONTAL)

		self.btnq = wx.Button(self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0)
		Hsz6.Add(self.btnq, 0, wx.ALL, 5)

		Vsz1.Add(Hsz6, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

		self.SetSizer( Vsz1 )
		self.Layout()

		# Connect Events
		self.btnq.Bind(wx.EVT_BUTTON, self.closit)

	def __del__( self ):
		pass

	# Virtual event handlers, overide them in your derived class
	def closit(self, event):
		q = self.GetParent()
		q.Close()

