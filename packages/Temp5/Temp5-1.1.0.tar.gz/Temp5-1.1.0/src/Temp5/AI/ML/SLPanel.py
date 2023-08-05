# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import os

import seaborn
import wx
import wx.xrc
import wx.dataview

from Config.Init import *

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):

	def __init__( self, parent,pnl=[], id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 420,450 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )
		self.pnl = pnl

		self.Titr = wx.StaticText( self, wx.ID_ANY, u"Squential Layer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Titr.Wrap( -1 )

		Vsz1.Add( self.Titr, 0, wx.ALL, 5 )

		self.P1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz2 = wx.BoxSizer( wx.VERTICAL )

		self.TLC = wx.dataview.TreeListCtrl( self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE )
		self.TLC.AppendColumn( u"Layer name", 50, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.TLC.AppendColumn( u"Layer Parameter", 350, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		#self.TLC.AppendColumn( u"Col3", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )

		Vsz2.Add( self.TLC, 1, wx.EXPAND |wx.ALL, 5 )


		self.P1.SetSizer( Vsz2 )
		self.P1.Layout()
		Vsz2.Fit( self.P1 )
		Vsz1.Add( self.P1, 1, wx.EXPAND |wx.ALL, 5 )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbla = wx.StaticText( self, wx.ID_ANY, u"Input Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbla.Wrap( -1 )

		Hsz1.Add( self.lbla, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.infld = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz1.Add( self.infld, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz1, 0, wx.EXPAND, 5 )

		self.P2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz3 = wx.BoxSizer( wx.VERTICAL )

		self.NB1 = wx.Notebook( self.P2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Pl11 = wx.Panel( self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz11 = wx.BoxSizer( wx.VERTICAL )

		Hsz11 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt11 = wx.StaticText( self.Pl11, wx.ID_ANY, u"filters =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt11.Wrap( -1 )

		Hsz11.Add( self.txt11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Spc1 = wx.SpinCtrl( self.Pl11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 99, 1 )
		Hsz11.Add( self.Spc1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt12 = wx.StaticText( self.Pl11, wx.ID_ANY, u"kernel_size =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt12.Wrap( -1 )

		Hsz11.Add( self.txt12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld12 = wx.TextCtrl( self.Pl11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fld12.SetToolTip(u"this format:(4,4)")
		Hsz11.Add( self.fld12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz11.Add( Hsz11, 1, wx.EXPAND, 5 )

		Hsz12 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt13 = wx.StaticText( self.Pl11, wx.ID_ANY, u"strides =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt13.Wrap( -1 )

		Hsz12.Add( self.txt13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld13 = wx.TextCtrl( self.Pl11, wx.ID_ANY, u"(1,1)", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz12.Add( self.fld13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt14 = wx.StaticText( self.Pl11, wx.ID_ANY, u"padding =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt14.Wrap( -1 )

		Hsz12.Add( self.txt14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld14 = wx.TextCtrl( self.Pl11, wx.ID_ANY, u"'valid'", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz12.Add( self.fld14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz11.Add( Hsz12, 1, wx.EXPAND, 5 )

		Hsz13 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt15 = wx.StaticText( self.Pl11, wx.ID_ANY, u"activation =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt15.Wrap( -1 )

		Hsz13.Add( self.txt15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld15 = wx.TextCtrl( self.Pl11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz13.Add( self.fld15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz11.Add( Hsz13, 1, wx.EXPAND, 5 )


		self.Pl11.SetSizer( Vsz11 )
		self.Pl11.Layout()
		Vsz11.Fit( self.Pl11 )
		self.NB1.AddPage( self.Pl11, u"Conv2D", True )
		self.adding = wx.Panel( self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Hoz12 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt21 = wx.StaticText( self.adding, wx.ID_ANY, u"units =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt21.Wrap( -1 )

		Hoz12.Add( self.txt21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Spc2 = wx.SpinCtrl( self.adding, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 999, 1 )
		Hoz12.Add( self.Spc2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt22 = wx.StaticText( self.adding, wx.ID_ANY, u"activation =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt22.Wrap( -1 )

		Hoz12.Add( self.txt22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld22 = wx.TextCtrl( self.adding, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hoz12.Add( self.fld22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.adding.SetSizer( Hoz12 )
		self.adding.Layout()
		Hoz12.Fit( self.adding )
		self.NB1.AddPage( self.adding, u"Dense", False )
		self.P13 = wx.Panel( self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Hoz13 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt31 = wx.StaticText( self.P13, wx.ID_ANY, u"Flatten()", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt31.Wrap( -1 )

		Hoz13.Add( self.txt31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.P13.SetSizer( Hoz13 )
		self.P13.Layout()
		Hoz13.Fit( self.P13 )
		self.NB1.AddPage( self.P13, u"Flatten", False )
		self.P14 = wx.Panel( self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz14 = wx.BoxSizer( wx.VERTICAL )

		Hoz41 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt41 = wx.StaticText( self.P14, wx.ID_ANY, u"pool_size =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt41.Wrap( -1 )

		Hoz41.Add( self.txt41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld41 = wx.TextCtrl( self.P14, wx.ID_ANY, u"(2,2)", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hoz41.Add( self.fld41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz14.Add( Hoz41, 1, wx.EXPAND, 5 )

		Hoz42 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt42 = wx.StaticText( self.P14, wx.ID_ANY, u"strides = ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt42.Wrap( -1 )

		Hoz42.Add( self.txt42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld42 = wx.TextCtrl( self.P14, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		Hoz42.Add( self.fld42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txt43 = wx.StaticText( self.P14, wx.ID_ANY, u"padding =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt43.Wrap( -1 )

		Hoz42.Add( self.txt43, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.fld43 = wx.TextCtrl( self.P14, wx.ID_ANY, u"'valid'", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hoz42.Add( self.fld43, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz14.Add( Hoz42, 1, wx.EXPAND, 5 )


		self.P14.SetSizer( Vsz14 )
		self.P14.Layout()
		Vsz14.Fit( self.P14 )
		self.NB1.AddPage( self.P14, u"MaxPool2D", False )
		self.P15 = wx.Panel( self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Hoz15 = wx.BoxSizer( wx.HORIZONTAL )

		self.txt51 = wx.StaticText( self.P15, wx.ID_ANY, u"rate =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt51.Wrap( -1 )

		Hoz15.Add( self.txt51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Spd3 = wx.SpinCtrlDouble( self.P15, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0.010000, 0.01 )
		self.Spd3.SetDigits( 2 )
		Hoz15.Add( self.Spd3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.P15.SetSizer( Hoz15 )
		self.P15.Layout()
		Hoz15.Fit( self.P15 )
		self.NB1.AddPage( self.P15, u"Dropout", False )

		self.P16 = wx.Panel(self.NB1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		Vsz16 = wx.BoxSizer(wx.VERTICAL)

		Hoz61 = wx.BoxSizer(wx.HORIZONTAL)

		self.txt61 = wx.StaticText(self.P16, wx.ID_ANY, u"weights =", wx.DefaultPosition, wx.DefaultSize, 0)
		self.txt61.Wrap(-1)

		Hoz61.Add(self.txt61, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.fld61 = wx.TextCtrl(self.P16, wx.ID_ANY, u"'imagenet'", wx.DefaultPosition, wx.DefaultSize, 0)
		Hoz61.Add(self.fld61, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.txt62 = wx.StaticText(self.P16, wx.ID_ANY, u"include_top =", wx.DefaultPosition, wx.DefaultSize, 0)
		self.txt62.Wrap(-1)

		Hoz61.Add(self.txt62, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		chs2Choices = [u"False", u"True"]
		self.chs2 = wx.Choice(self.P16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs2Choices, 0)
		self.chs2.SetSelection(0)
		Hoz61.Add(self.chs2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		Vsz16.Add(Hoz61, 1, wx.EXPAND, 5)

		Hoz62 = wx.BoxSizer(wx.HORIZONTAL)

		self.txt63 = wx.StaticText(self.P16, wx.ID_ANY, u"pooling =", wx.DefaultPosition, wx.DefaultSize, 0)
		self.txt63.Wrap(-1)

		Hoz62.Add(self.txt63, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.fld63 = wx.TextCtrl(self.P16, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		Hoz62.Add(self.fld63, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.txt64 = wx.StaticText(self.P16, wx.ID_ANY, u"classifier_activation =", wx.DefaultPosition, wx.DefaultSize, 0)
		self.txt64.Wrap(-1)

		Hoz62.Add(self.txt64, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.fld64 = wx.TextCtrl(self.P16, wx.ID_ANY, u"'softmax'", wx.DefaultPosition, wx.DefaultSize, 0)
		Hoz62.Add(self.fld64, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		Vsz16.Add(Hoz62, 1, wx.EXPAND, 5)

		self.P16.SetSizer(Vsz16)
		self.P16.Layout()
		Vsz16.Fit(self.P16)
		self.NB1.AddPage(self.P16, u"VGG16", False)

		Vsz3.Add( self.NB1, 1, wx.EXPAND |wx.ALL, 5 )


		self.P2.SetSizer( Vsz3 )
		self.P2.Layout()
		Vsz3.Fit( self.P2 )
		Vsz1.Add( self.P2, 1, wx.EXPAND |wx.ALL, 5 )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn1 = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.btn1, 0, wx.ALL, 5 )

		self.btn2 = wx.Button( self, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.btn2, 0, wx.ALL, 5 )

		self.btn3 = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.btn3, 0, wx.ALL, 5 )

		self.btn4 = wx.Button( self, wx.ID_ANY, u"Summary", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz2.Add( self.btn4, 0, wx.ALL, 5 )


		Vsz1.Add( Hsz2, 0, wx.EXPAND, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		self.isinput = False

		self.filllist()

		# Connect Events
		self.TLC.Bind( wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.slctitm )
		self.btn1.Bind( wx.EVT_BUTTON, self.addlyr )
		self.btn2.Bind( wx.EVT_BUTTON, self.edtlyr )
		self.btn3.Bind( wx.EVT_BUTTON, self.dellyr )
		self.btn4.Bind( wx.EVT_BUTTON, self.sumry )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def filllist(self):
		if not os.path.isfile(AI_PATH+"ML\\Squ_Lyr.txt"):
			with open(AI_PATH+"ML\\Squ_Lyr.txt","w",encoding='utf-8') as f:
				f.write("")
		else:
			with open(AI_PATH+"ML\\Squ_Lyr.txt","r",encoding='utf-8') as f:
				lins = f.readlines()

			broot = self.TLC.GetRootItem()
			if len(lins) > 0 :
				self.isinput = True
				for l in lins:
					layr, data = self.parseline(l)
					grp_lyr = self.TLC.AppendItem(broot, "active layer")
					self.TLC.SetItemText(grp_lyr, 0, layr)
					self.TLC.SetItemText(grp_lyr, 1, data)

	def parseline(self, line):
		lyer = line[:line.index("(")]
		data = line[line.index("("):]
		return lyer, data


	def slctitm( self, event ):
		gtslc = self.TLC.GetSelection()
		pgtxt = self.TLC.GetItemText(gtslc, 0)
		pgdat = self.TLC.GetItemText(gtslc, 1).rstrip(')\n').lstrip('(')
		#print(pgdat)
		if 'input_shape' in pgdat:
			self.infld.SetValue( pgdat[pgdat.index('input_shape =')+13:] )
		cdata = dict()
		lstpg = ['Conv2D','Dense','Flatten','MaxPool2D','Dropout','VGG16']
		self.NB1.ChangeSelection(lstpg.index(pgtxt))
		curpage = self.NB1.GetCurrentPage()
		if pgdat != '':
			cdata = dict( (a.strip(),b.strip())  for a , b in (elmnt.split('=') for elmnt in pgdat.split(' , ')) )
		#print(cdata)
		for chld in curpage.GetChildren():
			if len(cdata) > 0:
				if chld.GetClassName() == 'wxStaticText' :
					ivlu = cdata[chld.GetLabel().replace('=','').strip()]
				elif chld.GetClassName() == "wxSpinCtrl" :
					chld.SetValue(int(ivlu))
				elif chld.GetClassName() == "wxSpinCtrlDouble":
					chld.SetValue(float(ivlu))
				elif chld.GetClassName() == "wxChoice":
					chld.SetStringSelection('False')
				else:
					chld.SetValue(ivlu)

		event.Skip()

	def countitm(self, slctitm):
		iitm = self.TLC.GetFirstItem()
		i = 0
		while iitm.IsOk():
			if iitm == slctitm:
				return i
			else:
				iitm = self.TLC.GetNextItem(iitm)
				i += 1
		return -1

	def getpgdata(self, curpg, pgtext):
		itxt = ''
		if not self.isinput:
			if self.infld.GetValue() != '':
				#itxt = itxt + "input_shape =" + self.infld.GetValue() + ' , '
				linitxt = "keras.Input( shape = "+self.infld.GetValue()+" )"
				self.isinput = True
			else:
				wx.MessageBox("Do not forget fill input size")
				return ''

		for chld in curpg.GetChildren():
			if chld.GetClassName() == 'wxStaticText':
				itxt = itxt + chld.GetLabel()
			elif chld.GetClassName() == "wxSpinCtrl":
				itxt = itxt + str(chld.GetValue()) + ' , '
			elif chld.GetClassName() == "wxSpinCtrlDouble":
				itxt = itxt + str(chld.GetValue()) + ' , '
			elif chld.GetClassName() == "wxChoice":
				itxt = itxt + chld.GetStringSelection() + ' , '
			else:
				if chld.GetValue() == '':
					itxt = itxt + "None" + ' , '
				else:
					itxt = itxt + chld.GetValue() + ' , '

		# if not self.isinput:
		# 	if pgtext == 'Conv2D' or pgtext == 'VGG16':
		# 		if self.infld.GetValue() != '':
		# 			itxt = itxt + "input_shape =" + self.infld.GetValue() + ' , '
		# 			self.isinput = True
		# 		else:
		# 			wx.MessageBox("Do not forget fill input size")
		# 			return ''
		# 	else:
		# 		wx.MessageBox(" Only Conv2D can add input size")
		# 		return ''


		if pgtext == 'Flatten':
			linitxt = pgtext + "()"
		else:
			linitxt = pgtext + "( " + itxt.rstrip(' , ') + " )"
		return linitxt



	def addlyr( self, event ):
		curpage = self.NB1.GetCurrentPage()
		numpag = self.NB1.GetSelection()
		pagetxt = self.NB1.GetPageText(numpag)

		linitxt = self.getpgdata(curpage, pagetxt)
		if linitxt != '':
			with open(AI_PATH + "ML\\Squ_Lyr.txt", "a", encoding='utf-8') as f:
				f.write(linitxt+'\n')

			self.TLC.DeleteAllItems()
			self.filllist()
		self.Refresh()
		event.Skip()

	def edtlyr( self, event ):
		gtslc = self.TLC.GetSelection()
		nmbr = self.countitm(gtslc)
		#print(nmbr)
		pgtxt = self.TLC.GetItemText(gtslc, 0)
		pgdat = self.TLC.GetItemText(gtslc, 1)
		curpage = self.NB1.GetCurrentPage()
		print(pgtxt,pgdat,nmbr)

		with open(AI_PATH + "ML\\Squ_Lyr.txt", "r", encoding='utf-8') as f:
			lins = f.readlines()
		newlins = []
		i = 0
		for l in lins:
			if l == pgtxt+pgdat and i==nmbr:
				if 'input_shape' in l:
					self.isinput = False
					linitxt = self.getpgdata(curpage, pgtxt)
					newlins.append(linitxt + '\n')
				else:
					self.isinput = False
					linitxt = self.getpgdata(curpage, pgtxt)
					newlins.append(linitxt+'\n')
			else:
				newlins.append(l)
			i+=1
		self.TLC.SetItemText(gtslc, 1, linitxt.replace(pgtxt, ''))
		#print(newlins)
		with open(AI_PATH + "ML\\Squ_Lyr.txt", "w", encoding='utf-8') as f:
			f.write('')
			for l in newlins:
				f.writelines(l)

		event.Skip()

	def dellyr( self, event ):
		gtslc = self.TLC.GetSelection()
		pgtxt = self.TLC.GetItemText(gtslc, 0)
		pgdat = self.TLC.GetItemText(gtslc, 1)
		#print(pgtxt,pgdat)
		self.TLC.DeleteItem(gtslc)
		with open(AI_PATH + "ML\\Squ_Lyr.txt", "r", encoding='utf-8') as f:
			lins = f.readlines()
		newlins = []
		for l in lins:
			if pgtxt+pgdat not in l:
				newlins.append(l)
		#print(lins,newlins)
		with open(AI_PATH + "ML\\Squ_Lyr.txt", "w", encoding='utf-8') as f:
			f.write('')
			for l in newlins:
				f.writelines(l)
		event.Skip()


	def sumry( self, event ):
		print(self.GetGrandParent())
		pnl = self.GetGrandParent()
		#print(pnl.sumry)
		#pnl.sumry = True
		pnl.Dosumry()
		q = self.GetParent()
		q.Close()
		event.Skip()
