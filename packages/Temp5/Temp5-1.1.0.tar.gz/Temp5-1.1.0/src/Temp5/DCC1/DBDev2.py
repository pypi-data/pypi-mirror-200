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

from Config.Init import *
import Res.Allicons as icon

import Database.PostGet as PG
#import Database.PostGet2 as PG2

from AI.Analiz import *
import AI.DBgen as DBG
import AI.OpnSrc as OS

_ = wx.GetTranslation

###########################################################################
## Class MyPanel6
###########################################################################

class MyPanel1 ( wx.Panel ):

	def __init__(self, parent, For_This_Frame=[], id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 450), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
		wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

		self.config = wx.GetApp().GetConfig()
		if int(self.config.Read('DBtype')) == 2:
			self.TDBE = 'mysql'
		elif int(self.config.Read('DBtype')) == 3:
			self.TDBE = 'post'
		elif int(self.config.Read('DBtype')) == 4:
			self.TDBE = 'orcl'
		else:
			self.TDBE = 'sqlite'


		Vsz1 = wx.BoxSizer(wx.VERTICAL)
		self.FTF = For_This_Frame

		self.Splt1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D| wx.SP_LIVE_UPDATE| wx.SP_NO_XP_THEME| wx.SP_THIN_SASH)
		self.Splt1.Bind(wx.EVT_IDLE, self.Splt1OnIdle)

		self.P1 = wx.Panel( self.Splt1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		Vsz2 = wx.BoxSizer(wx.VERTICAL)

		self.lbl0 = wx.StaticText( self.P1, wx.ID_ANY, _(u"Select database"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.lbl0.Wrap(-1)

		Vsz2.Add( self.lbl0, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		if self.TDBE == 'sqlite':
			self.dbfile = wx.FilePickerCtrl( self.P1, wx.ID_ANY, wx.EmptyString, _(u"Select Database file"), u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_OPEN|wx.FLP_SMALL )
			Vsz2.Add( self.dbfile, 0, wx.ALL|wx.EXPAND, 5 )

		if self.TDBE == 'mysql':
			self.idbfl2 = PG.Get2(u'', u'', u'')
			dbChoices = [db[0] for db in self.idbfl2.GetFromString(" SHOW DATABASES; ") ]
			self.dbBox1 = wx.Choice(self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dbChoices, 0)
			Vsz2.Add(self.dbBox1, 0, wx.ALL | wx.EXPAND, 5)

		if self.TDBE == 'post':
			self.idbfl2 = PG.Get2(u'', u'', u'')
			dbChoices = [db[0] for db in self.idbfl2.GetFromString(" SELECT datname FROM pg_database; ") ]
			self.dbBox1 = wx.Choice(self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dbChoices, 0)
			Vsz2.Add(self.dbBox1, 0, wx.ALL | wx.EXPAND, 5)

		if self.TDBE == 'orcl':
			self.idbfl2 = PG.Get2(u'', u'', u'')
			dbChoices = [db[0] for db in self.idbfl2.GetFromString("  ") ]
			self.dbBox1 = wx.Choice(self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dbChoices, 0)
			Vsz2.Add(self.dbBox1, 0, wx.ALL | wx.EXPAND, 5)



		self.lbl1 = wx.StaticText( self.P1, wx.ID_ANY, _(u"List of Tabel:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl1.Wrap( -1 )

		Vsz2.Add( self.lbl1, 0, wx.ALL, 5 )

		self.DVC1 = wx.dataview.TreeListCtrl( self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_HAS_BUTTONS|wx.TR_DEFAULT_STYLE )
		self.Col1 = self.DVC1.AppendColumn( _(u"Name"), 160,  wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.Col2 = self.DVC1.AppendColumn( _(u"Type"), 70,  wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		#self.Col3 = self.DVC1.AppendColumn( u"Name", 0,  wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		Vsz2.Add( self.DVC1, 1, wx.ALL|wx.EXPAND, 5 )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn1 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn1.SetBitmap( wx.Bitmap( ICON16_PATH + u'table_row_insert.png', wx.BITMAP_TYPE_ANY ) )
		self.btn1.SetBitmap(icon.table_row_insert.GetBitmap())
		self.btn1.SetToolTip( _(u"Insert") )

		Hsz1.Add( self.btn1, 0, wx.ALL, 5 )

		self.btn2 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn2.SetBitmap(wx.Bitmap(ICON16_PATH + u'table_refresh.png', wx.BITMAP_TYPE_ANY))
		self.btn2.SetBitmap(icon.table_refresh.GetBitmap())
		self.btn2.SetToolTip(_(u"Update"))

		Hsz1.Add( self.btn2, 0, wx.ALL, 5 )

		self.btn3 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn3.SetBitmap(wx.Bitmap(ICON16_PATH + u'table_row_delete.png', wx.BITMAP_TYPE_ANY))
		self.btn3.SetBitmap(icon.table_row_delete.GetBitmap())
		self.btn3.SetToolTip(_(u"Delete"))

		Hsz1.Add( self.btn3, 0, wx.ALL, 5 )

		self.btn4 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn4.SetBitmap(wx.Bitmap(ICON16_PATH + u'table_relationship.png', wx.BITMAP_TYPE_ANY))
		self.btn4.SetBitmap(icon.table_relationship.GetBitmap())
		self.btn4.SetToolTip(_(u"Join"))

		Hsz1.Add( self.btn4, 0, wx.ALL, 5 )

		self.btn5 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn5.SetBitmap(wx.Bitmap(ICON16_PATH + u'table_import.png', wx.BITMAP_TYPE_ANY))
		self.btn5.SetBitmap(icon.table_import.GetBitmap())
		self.btn5.SetToolTip(_(u"Brows"))

		Hsz1.Add( self.btn5, 0, wx.ALL, 5 )

		self.btn6 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn6.SetBitmap(wx.Bitmap(ICON16_PATH + u'accept_button.png', wx.BITMAP_TYPE_ANY))
		self.btn6.SetBitmap(icon.accept_button.GetBitmap())
		self.btn6.SetToolTip(_(u"Apply"))

		Hsz1.Add( self.btn6, 0, wx.ALL, 5 )

		self.btn7 = wx.BitmapButton(self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		#self.btn7.SetBitmap(wx.Bitmap(ICON16_PATH + u'table_lightning.png', wx.BITMAP_TYPE_ANY))
		self.btn7.SetBitmap(icon.table_lightning.GetBitmap())
		self.btn7.SetToolTip(_(u"Generate"))
		Hsz1.Add(self.btn7, 0, wx.ALL, 5)


		Vsz2.Add( Hsz1, 0, wx.EXPAND, 5 )


		self.P1.SetSizer( Vsz2 )
		self.P1.Layout()
		Vsz2.Fit( self.P1 )
		self.P2 = wx.Panel( self.Splt1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz3 = wx.BoxSizer( wx.VERTICAL )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl3 = wx.StaticText( self.P2, wx.ID_ANY, _(u"Method in program"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz2.Add( self.lbl3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs1Choices = [ u"set", u"get", u"both" ]
		self.chs1 = wx.Choice( self.P2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs1Choices, 0 )
		self.chs1.SetSelection( 2 )
		Hsz2.Add( self.chs1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz3.Add( Hsz2, 0, wx.EXPAND, 5 )

		self.fldinit = wx.TextCtrl(self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
		                           wx.HSCROLL|wx.TE_MULTILINE|wx.TE_WORDWRAP )
		Vsz3.Add(self.fldinit, 1, wx.ALL | wx.EXPAND, 5)

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl4 = wx.StaticText( self.P2, wx.ID_ANY, _(u"Program Statments"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl4.Wrap( -1 )

		Hsz3.Add( self.lbl4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnps = wx.Button( self.P2, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz3.Add( self.btnps, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz3.Add( Hsz3, 0, wx.EXPAND, 5 )

		self.fldprg = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_WORDWRAP )
		Vsz3.Add( self.fldprg, 1, wx.ALL|wx.EXPAND, 5 )

		Hsz4 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl5 = wx.StaticText( self.P2, wx.ID_ANY, _(u"SQL  Statments"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl5.Wrap( -1 )

		Hsz4.Add( self.lbl5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnss = wx.Button( self.P2, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		Hsz4.Add( self.btnss, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz3.Add( Hsz4, 0, wx.EXPAND, 5 )

		self.fldsql = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_WORDWRAP )
		Vsz3.Add( self.fldsql, 1, wx.ALL|wx.EXPAND, 5 )

		Hsz5 = wx.BoxSizer( wx.HORIZONTAL )

		self.btncv = wx.Button( self.P2, wx.ID_ANY, _(u"To CVS"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz5.Add( self.btncv, 0, wx.ALL, 5 )

		self.btnxl = wx.Button( self.P2, wx.ID_ANY, _(u"To Excel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz5.Add( self.btnxl, 0, wx.ALL, 5 )

		self.btnex = wx.Button( self.P2, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btnex.SetToolTip( _(u"Extended") )

		Hsz5.Add( self.btnex, 0, wx.ALL, 5 )

		Vsz3.Add( Hsz5, 0, wx.EXPAND, 5 )

		self.P2.SetSizer( Vsz3 )
		self.P2.Layout()
		Vsz3.Fit( self.P2 )
		self.Splt1.SplitVertically( self.P1, self.P2, 255 )
		Vsz1.Add( self.Splt1, 1, wx.EXPAND, 5 )

		self.SetSizer( Vsz1 )
		self.Layout()


		#Parameter init
		self.table = u''
		self.field = u''
		self.data = u''
		self.sqfile = u''

		# Init program
		self.fromHere()

		# Connect Events
		if self.TDBE == 'sqlite':
			self.dbfile.Bind(wx.EVT_FILEPICKER_CHANGED, self.dbopn)
		if self.TDBE == 'mysql' or self.TDBE == 'post':
			self.dbBox1.Bind( wx.EVT_CHOICE, self.usedb )
		self.DVC1.Bind(wx.dataview.EVT_TREELIST_ITEM_CHECKED, self.chkit)
		self.btn1.Bind( wx.EVT_BUTTON, self.insit )
		self.btn2.Bind( wx.EVT_BUTTON, self.updit )
		self.btn3.Bind( wx.EVT_BUTTON, self.delit )
		self.btn4.Bind( wx.EVT_BUTTON, self.jinit )
		self.btn5.Bind( wx.EVT_BUTTON, self.brwit )
		self.btn6.Bind( wx.EVT_BUTTON, self.aplit )
		self.btn7.Bind( wx.EVT_BUTTON, self.gnrit )

		self.chs1.Bind( wx.EVT_CHOICE, self.chgmtd )
		self.btnps.Bind( wx.EVT_BUTTON, self.prgstm )
		self.btnss.Bind( wx.EVT_BUTTON, self.sqlstm )
		self.btncv.Bind( wx.EVT_BUTTON, self.tocvs )
		self.btnxl.Bind( wx.EVT_BUTTON, self.toexl )
		self.btnex.Bind( wx.EVT_BUTTON, self.extnd )

	def __del__( self ):
		pass

	# Virtual event handlers, overide them in your derived class
	def fromHere(self):
		if len(self.FTF) > 0:
			frmname = self.FTF[0].GetTitle()

			lbl0 = self.lbl0.GetLabel()
			nlbl = lbl0 + ' from ' + frmname
			#print(frmname)
			self.lbl0.SetLabel(nlbl)
			if self.FTF[1] != '' and self.TDBE == 'sqlite':
				self.dbfil = self.FTF[1]
				self.dbfile.SetPath(self.dbfil)
				self.idbfl2 = PG.Get2(self.dbfil, u'', u'')
				self.dbdata = self.idbfl2.GetFromString('select * from sqlite_master')
				self.DVC1.DeleteAllItems()
				self.filllist()
				self.chgmtd(None)
			if self.FTF[1] != '' and self.TDBE in ['mysql','post']:
				self.dbfil = self.FTF[1]
				self.dbBox1.SetStringSelection(self.dbfil)
				self.usedb(None)



	def dbopn(self, event):
		if self.TDBE == 'sqlite':
			dbftype = Database_type[int(self.config.Read('DBtype'))]
			self.dbfil = self.dbfile.GetPath()
			self.idbfl2 = PG.Get2(self.dbfil, u'',u'')
			self.dbdata = self.idbfl2.GetFromString('select * from sqlite_master')
			self.DVC1.DeleteAllItems()
			self.filllist()
			self.chgmtd(None)

	def usedb(self, event):
		thsdbuse = self.dbBox1.GetStringSelection()
		self.idbfl2 = PG.Get2(thsdbuse, u'', u'')
		tbles = ''
		if self.TDBE == 'mysql':
			self.idbfl2.GetCommandStr(thsdbuse,' USE %s; '%thsdbuse )
			tbles = self.idbfl2.GetFromString(' SHOW FULL TABLES; ')

		if self.TDBE == 'post':
			#self.idbfl2 = PG.Get2.GetCommandStr(thsdbuse,"SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND  schemaname != 'information_schema';" )
			stinfsql = " SELECT tablename, schemaname FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'; "
			tabel = self.idbfl2.GetFromString(stinfsql)
			#print(self.idbfl2 , tabel)
			tbles = tabel
			#tbles = self.idbfl2.GetFromString(' \dt ')

		#print(tbles)
		self.dbdata = tbles
		self.DVC1.DeleteAllItems()
		self.filllist2()
		self.chgmtd(None)


	def filllist(self):
		Droot = self.DVC1.GetRootItem()
		self.troot = self.DVC1.AppendItem(Droot,"Table")
		self.iroot = self.DVC1.AppendItem(Droot,"Indices")
		self.Tfilds, self.Indxss = AnalizdbText2(self.dbdata)
		#print(Tfilds)
		for tb in self.Tfilds:
			tbl = self.DVC1.AppendItem(self.troot, tb)
			for fld in self.Tfilds[tb]:
				ifld = self.DVC1.AppendItem(tbl, fld[0])
				self.DVC1.SetItemText(ifld, 0, fld[0])
				self.DVC1.SetItemText(ifld, 1, fld[1])

	def filllist2(self):
		self.Tfilds = {}
		Droot = self.DVC1.GetRootItem()
		self.troot = self.DVC1.AppendItem(Droot, "Table")
		for tb in self.dbdata:
			tbl = self.DVC1.AppendItem(self.troot, tb[0])
			self.DVC1.SetItemText(tbl, 0, tb[0])
			self.DVC1.SetItemText(tbl, 1, tb[1])
			if self.TDBE == 'mysql':
				fldlst = []
				for col in self.idbfl2.GetFromString(" DESC %s" %tb[0]):
					ifld = self.DVC1.AppendItem(tbl, col[0])
					self.DVC1.SetItemText(ifld, 0, col[0])
					self.DVC1.SetItemText(ifld, 1, col[1])
					fldlst.append((col[0],col[1]))
				self.Tfilds[tb[0]] = fldlst
			if self.TDBE == 'post':
				fldlst = []
				for col in self.idbfl2.GetFromString(" SELECT column_name, data_type FROM information_schema.columns WHERE TABLE_NAME = '%s' " %tb[0]):
					ifld = self.DVC1.AppendItem(tbl, col[0])
					self.DVC1.SetItemText(ifld, 0, col[0])
					self.DVC1.SetItemText(ifld, 1, col[1])
					fldlst.append((col[0], col[1]))
				self.Tfilds[tb[0]] = fldlst

			#for fld in self.Tfilds[tb]:

	def chkit(self, event):
		self.gtslt = self.DVC1.GetSelections()
		itmtxt = self.DVC1.GetItemText(self.gtslt[0], 0)
		if itmtxt in [f[0] for fl in self.Tfilds.values() for f in fl ]:
			prnt = self.DVC1.GetItemParent(self.gtslt[0])
			if self.DVC1.AreAllChildrenInState(prnt,1):
				self.DVC1.CheckItem(prnt, 1)
			else:
				self.DVC1.CheckItem(prnt, 2)
			#if self.Tfilds[self.DVC1.GetItemText(prnt, 0)]
			#print(self.DVC1.AreAllChildrenInState(prnt,1))
		if itmtxt in self.Tfilds:
			flds = [f[0] for f in self.Tfilds[itmtxt]]
			if self.DVC1.GetCheckedState(self.gtslt[0]) == 1:
				self.DVC1.CheckItemRecursively(self.gtslt[0], 1)
			elif self.DVC1.GetCheckedState(self.gtslt[0]) == 0:
				self.DVC1.CheckItemRecursively(self.gtslt[0], 0)

	def ChkTicks(self):
		frstitm = self.DVC1.GetRootItem()
		nxitm = self.DVC1.GetNextItem(frstitm)
		tbltiklst = {}
		fldtiklst = []
		#print(self.DVC1.GetItemText(nxitm, 0),self.DVC1.GetCheckedState(nxitm))
		# if self.DVC1.GetCheckedState(frstitm):
		# 	self.DVC1.CheckItemRecursively(frstitm,1)
		# else:
		# 	self.DVC1.UncheckItem(frstitm)
		for fld in self.Tfilds:
			nxitm = self.DVC1.GetNextItem(nxitm)
			tblnm = u''
			if self.DVC1.GetCheckedState(nxitm):
				tblnm = self.DVC1.GetItemText(nxitm, 0)
			fldtiklst = []
			for f in self.Tfilds[fld]:
				nxitm = self.DVC1.GetNextItem(nxitm)
				if self.DVC1.GetCheckedState(nxitm):
					fldtiklst.append(self.DVC1.GetItemText(nxitm, 0))
				#tbltiklst.append(self.DVC1.GetItemText(nxitm, 0))
			if tblnm != u'':
				tbltiklst[tblnm] = fldtiklst

		return tbltiklst

	def insit( self, event ):
		#self.gtslt = self.DVC1.GetSelections()
		#itmtxt = self.DVC1.GetItemText(self.gtslt[0], 0)
		sqlsnts = self.ChkTicks()
		txt = u''
		for tbl in sqlsnts.keys():
			txt += '\n'
			txt += u"\tself.MySet.Tabel = '%s' \n"%tbl
			fild = u''
			for fld in sqlsnts.get(tbl):
				fild += fld + ','
			txt += u'\t#AllData = ['
			for d in range(len(sqlsnts.get(tbl))):
				txt += u' Data%d' %d + ','
			txt = txt.rstrip(',')
			txt += u'] #You can add data to put here\n'
			txt += u'\tself.MySet.Addrecord( " '+fild.rstrip(',')+ u' ", AllData )\n'

		#print(txt)
		self.fldprg.SetValue(txt)

	def updit( self, event ):
		sqlsnts = self.ChkTicks()
		smfild = [ f for fld in sqlsnts.values() for f in fld ]
		#print(sqlsnts,'\n',smfild)
		frm = wx.Dialog(self, -1)
		pnl = MyPanel3(frm, smfild)
		frm.SetSize((400, 125))
		frm.SetLabel(_(u'Select Key feild'))
		frm.ShowModal()
		if pnl.acept:
			choic = pnl.chs2.GetStringSelection()
		else:
			choic = ''

		frm.Destroy()
		txt = u''
		for tbl in sqlsnts.keys():
			txt += '\n'
			txt += u"\tself.MySet.Tabel = '%s' \n" % tbl
			fild = u''
			contor = 0
			for fld in sqlsnts.get(tbl):
				if fld != choic:
					fild += fld + '=? ,'
					contor += 1
			txt += u'\t#AllData = ['
			Data = u''
			for d in range(contor):
				Data += u' Data%d' %d + ','
			Data = Data.rstrip(',')
			#print(Data)
			txt += Data + u'] #You can add data to put here\n'
			txt += u'\t#self.KeyData = #can put need data here\n'
			txt += u'\tself.MySet.Updaterecord( " ' + fild.rstrip(',')
			txt += ' Where '+ choic + ' = %s " %self.KeyData , AllData )\n'

		self.fldprg.SetValue(txt)

		event.Skip()

	def delit( self, event ):
		sqlsnts = self.ChkTicks()
		smfild = [f for fld in sqlsnts.values() for f in fld]
		# print(sqlsnts,'\n',smfild)
		frm = wx.Dialog(self, -1)
		pnl = MyPanel3(frm, smfild)
		frm.SetSize((400, 125))
		frm.SetLabel(_(u'Select Key feild'))
		frm.ShowModal()
		if pnl.acept:
			choic = pnl.chs2.GetStringSelection()
		else:
			choic = ''

		frm.Destroy()
		txt = u''
		for tbl in sqlsnts.keys():
			txt += '\n'
			txt += u"\tself.MySet.Tabel = '%s' \n" % tbl

			txt += u'\t#self.KeyData = #can put need data here\n'
			txt += u'\tself.MySet.Deleterecord( " ' #+ fild.rstrip(',')
			txt += choic + ' = %s " %self.KeyData ) \n'
			#txt += ' Where ' + choic + ' = %s " %self.KeyData , AllData )\n'

		self.fldprg.SetValue(txt)
		event.Skip()

	def jinit( self, event ):
		#print(self.ChkTicks())
		sqlsnts = self.ChkTicks()
		Join = ''
		Jkey = []
		Tbls = [T for T in sqlsnts.keys()]
		Bchs = False
		Btbl = u''
		for i in range(len(Tbls)-1):
			frm = wx.Dialog(self, -1)
			pnl = MyPanel5(frm, sqlsnts)
			frm.SetSize((550, 155))
			frm.SetLabel(_(u'Select Key feild'))
			if Bchs:
				pnl.chs1.SetStringSelection(Btbl)
				pnl.chs1.Disable()
				pnl.chs2.SetItems([Btbl+'.'+f for f in sqlsnts[Btbl]])
				pnl.chs3.SetItems([Tbls[0]+'.'+f for f in sqlsnts[Tbls[0]]] )
			frm.ShowModal()
			if pnl.acept:
				if i == 0:
					Btbl = pnl.chs1.GetStringSelection()
					Tbls.remove(Btbl)
					Bchs = True
				else:
					pass
				Jkey.append(pnl.chs2.GetStringSelection()+' = '+pnl.chs3.GetStringSelection())
				Jslc = pnl.chs3.GetStringSelection().split('.')[0]
				Tbls.remove(Jslc)
				#print(Tbls,Jslc)
			else:
				break
			frm.Destroy()
		#print(Btbl, Jkey)
		Join += " Select "
		Fields = [T+'.'+F for T in sqlsnts.keys() for F in sqlsnts[T]]
		#print(Fields)
		for Fld in Fields:
			Join += Fld + ' ,'
		Join = Join.rstrip(',')
		Join += " From "+Btbl+"\n"
		for J in Jkey:
			Join += " Inner Join " + J.split('=')[-1].split('.')[0] + " On " + J + "\n"
		#print(Join)
		self.fldsql.SetValue(Join)

		#self.fldsql.SetValue(sqltxt)

	def brwit( self, event ):

		#dbtype = Database_type[int(self.config.Read('DBtype'))]
		self.gtslt = self.DVC1.GetSelections()
		if self.fldsql.GetValue() != u'':
			sqlcomnd = self.fldsql.GetValue()
			#brsdb = PG2.Get(self.dbfil, dbtype)
			brsdb = PG.Get2(self.dbfil, u'',u'')
			#brsdb = PG.Get(self.dbfil, u'', u'')
			self.idata = brsdb.GetFromString(sqlcomnd)
			if len(self.idata) == 0:
				wx.MessageBox("0 row in %s"%sqlcomnd)
				thsfld = []
			else:
				thsfld = self.idata[0].keys()

		else:
			thsfld = []
			if self.DVC1.GetItemText(self.gtslt[0], 1) == '' and self.DVC1.GetItemText(self.gtslt[0], 0) not in ['Table','Indices']:
				myfild = self.DVC1.GetItemText(self.gtslt[0], 0)
				#print(self.ChkTicks())
				if len(self.ChkTicks()) > 0:
					thstbl = [T for T in self.ChkTicks().keys()]
					thsfld = [t+'.'+F for t in self.ChkTicks() for F in self.ChkTicks()[t]]
					ftxt = ' ,'.join(thsfld)
					Ttxt = ' ,'.join(thstbl)
					#print(ftxt,thsfld,thstbl)
					self.idbfl = PG.Get2(self.dbfil, u'', u'')
					self.idata = self.idbfl.GetFromString(u'select %s from %s' %(ftxt,Ttxt))

				else:
					for fld in self.Tfilds:
						if myfild == fld:
							thsfld = [f[0] for f in self.Tfilds[fld]]
					self.idbfl = PG.Get2(self.dbfil, u'', u'')
					#self.idbfl = PG2.Get(self.dbfil, dbtype)
					self.idata = self.idbfl.GetFromString(u' select * from %s' % myfild)
			else:
				if self.TDBE == 'mysql' or self.TDBE == 'post':
					itbl = self.DVC1.GetItemText(self.gtslt[0], 0)
					self.idata = self.idbfl2.GetFromString(u" select * from %s" %itbl )
					#print(self.Tfilds,self.idata)
					for fld in self.Tfilds:
						if itbl == fld:
							thsfld = [str(f[0]) for f in self.Tfilds[fld]]
				else:
					self.idata = []
					thsfld = []
		#print(thsfld,self.idata)
		if len(thsfld) > 0 and len(self.idata) > 0 :
			frm = wx.Dialog(self, -1)
			pnl = MyPanel2(frm, thsfld, self.idata)
			frm.SetSize((600, 300))
			frm.SetLabel(_(u'Select Table'))
			frm.ShowModal()

			frm.Destroy()

	def aplit( self, event ):
		pdwf = wx.FindWindowByName("Program Develop")
		#print(dir(pdwf))
		pitm = pdwf.DVC1.GetSelection()
		pdtxt = pdwf.DVC1.GetItemText(pitm,0)
		pdcod = pdwf.DVC1.GetItemText(pitm,1)
		pdfil = pdwf.thsfile
		pdpth = pdwf.thspath
		#print(pdtxt,pdcod,pdfil,pdpth)
		if self.fldinit.GetValue() != '':
			if pdcod != None or pdcod != '':
				if '.py' in pdfil :
					mycod = Anlzfil(pdfil)
					if not mycod.ishaspanel():
						wx.MessageBox(_("Please use wx.Panel in source file"))
						return 1
					#print(mycod.indexImpline())
					ex = 0
					for imlin,inx in mycod.indexImpline():
						if 'Database.PostGet' in imlin:
							ex = 1

					self.Frm = wx.Frame(self,
					                    style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)
					self.Pnl = OS.SrcPanel(self.Frm, pdfil)
					self.Frm.SetMenuBar(OS.MyMenuBar1(u'Pro'))
					self.Frm.SetSize((700, 560))
					self.Frm.SetLabel(pdfil)
					self.Frm.Show()
					if ex == 0:
						linnum = mycod.indexImpline()[-1][1]
						#print(linnum)
						self.Pnl.SrcAlg.GotoLine(linnum+1)
						ipos = self.Pnl.SrcAlg.GetCurrentPos()
						#print(ipos,self.Pnl.SrcAlg.GetLastPosition())
						self.Pnl.SrcAlg.SetInsertionPoint(ipos-1)
						#self.Pnl.SrcAlg.SetInsertionPointEnd()
						self.Pnl.SrcAlg.AddText("\nimport Database.PostGet as PG\n")

					if mycod.isDBimexist():
						getit,postit = mycod.isFiledbexist()
						#print(getit,postit)
						print("If you change Database Please change it manually")
					else:
						#print(self.fldinit.GetValue())
						#print(self.Pnl.SrcAlg.GetCurrentPos())
						rsult=self.Pnl.SrcAlg.SearchInTarget('wx.Panel.__init__')
						self.Pnl.SrcAlg.SearchAnchor()
						if rsult == -1:
							self.Pnl.SrcAlg.SearchNext(1,'wx.Panel.__init__')
						npline=self.Pnl.SrcAlg.GetCurrentLine()
						#print(npline)
						self.Pnl.SrcAlg.GotoLine(npline + 2)
						ipos = self.Pnl.SrcAlg.GetCurrentPos()
						#print(ipos, self.Pnl.SrcAlg.GetLastPosition())
						self.Pnl.SrcAlg.SetInsertionPoint(ipos)
						self.Pnl.SrcAlg.AddText("\n")
						self.Pnl.SrcAlg.AddText(self.fldinit.GetValue())
						self.Pnl.SrcAlg.AddText("\n")
						wx.MessageBox(_("Please Add Program Statements to correct line of source file for Use database.\n"
						              "And Then Save file to Apply change.Do Not forget Save File!"))

				else:
					print(pdfil)
			else:
				print(pdcod,type(pdcod))
		else:
			print(u'Please select your database')
		event.Skip()

	def gnrit( self, event ):
		if self.fldsql.GetValue() != '':
			self.dlg = wx.FileDialog(self, _("Save as SQL file"),
			                         defaultDir=Src_dbf+SLASH+'sqls',
			                         defaultFile="",
			                         wildcard="SQL file(*.sql)|*.sql|All file(*.*)|*.*",
			                         style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
			if self.dlg.ShowModal() == wx.ID_OK:
				sqlfpath = self.dlg.GetPaths()[0]
			else:
				return 1
			self.dlg.Destroy()
			with open(sqlfpath+'.sql','w+',encoding='utf-8') as f:
				f.write(self.fldsql.GetValue())
			wx.MessageBox(_("SQL file successful create in Src\DBF\sqls path."))

		event.Skip()

	def chgmtd( self, event ):
		dbf = Src_dbf + ''
		#inittxt = "## Add this lines to import part of program \nimport Database.PostGet as PG\n"
		inittxt = ''
		inittxt2 = "\t\t## Please Add this line in Panel __init__ function\n"
		if self.TDBE == 'sqlite':
			dbf = self.dbfil
		else:
			dbf = self.dbBox1.GetStringSelection()

		if self.table != '':
			table = self.table
		else:
			table = u''
		if self.field != '':
			field = self.field
		else:
			field = u''
		if self.data != '':
			data = self.dbdat
		else:
			data = u''
		if self.sqfile != '':
			file = self.sqfile
		else:
			file = u''
		if self.chs1.GetStringSelection() == 'set':
			self.fldinit.SetValue(inittxt+inittxt2+f"\t\tself.MySet = PG.Post2('{dbf}','{table}','{field}','{data}')\n".format(dbf,table,field,data))
		elif self.chs1.GetStringSelection() == 'get':
			self.fldinit.SetValue(inittxt+inittxt2+f"\t\tself.MyGet = PG.Get2('{dbf}','{data}','{file}')\n".format(dbf,data,file))
		elif self.chs1.GetStringSelection() == 'both':
			self.fldinit.SetValue(inittxt+inittxt2+f"\t\tself.MySet = PG.Post2('{dbf}','{table}','{field}','{data}')\n".format(dbf,table,field,data)
			                      +f"\t\tself.MyGet = PG.Get2('{dbf}','{data}','{file}')\n".format(dbf,data,file))
		else:
			print('What method is')
		if self.TDBE == 'mysql':
			#if self.chs1.GetStringSelection() == 'set':
			#	self.fldinit.SetValue(self.fldinit.GetValue()+f"\t\tself.MySet.GetCommandStr('{dbf}','USE {dbf};')\n".format(dbf,dbf))
			if self.chs1.GetStringSelection() == 'get':
				self.fldinit.SetValue(self.fldinit.GetValue() + f"\t\tself.MyGet.GetCommandStr('{dbf}','USE {dbf};')\n".format(dbf, dbf))
			elif self.chs1.GetStringSelection() == 'both':
				self.fldinit.SetValue(
					self.fldinit.GetValue() + #f"\t\tself.MySet.GetCommandStr('{dbf}','USE {dbf};')\n".format(dbf, dbf)+
				f"\t\tself.MyGet.GetCommandStr('{dbf}','USE {dbf};')\n".format(dbf, dbf))



	def prgstm( self, event ):
		txt1 = self.fldinit.GetValue()
		txt2 = self.fldprg.GetValue()
		#print(txt1+u'\n'+txt2)
		self.Frm = wx.Frame(self, style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)
		if txt1 != u'':
			self.Pnl = DBG.TxtPanel(self.Frm)
			self.Pnl.Txt.SetValue(txt1+u'\n'+txt2)
			self.Frm.SetMenuBar(DBG.MyMenuBar2(u'prg'))
			self.Frm.Show()
		event.Skip()

	def sqlstm( self, event ):
		# txt1 = self.fldsql.GetValue()
		# #print(txt1)
		# self.Frm = wx.Frame(self, style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)
		# if txt1 != u'':
		# 	self.Pnl = DBG.TxtPanel(self.Frm)
		# 	self.Pnl.Txt.SetValue(txt1)
		# 	self.Frm.SetMenuBar(DBG.MyMenuBar2(u'sql'))
		# 	self.Frm.Show()
		self.dlg = wx.FileDialog(self, _("Open sql file"),
		                         defaultDir=Src_dbf+SLASH+'sqls',
		                         defaultFile="",
		                         wildcard="SQL file(*.sql)|*.sql",
		                         style=wx.FD_OPEN |wx.FD_CHANGE_DIR )
		if self.dlg.ShowModal() == wx.ID_OK:
			sqlfil = self.dlg.GetPaths()[0]
		self.dlg.Destroy()
		with open(sqlfil,'r') as f:
			sqltxt = f.read()
		self.fldsql.SetValue(sqltxt)


		event.Skip()

	def tocvs( self, event ):
		import csv
		self.dlg = wx.FileDialog(self,_("Save as CSV file"),
		                         defaultDir=DATABASE_PATH,
		                         defaultFile="",
		                         wildcard="CSV file(*.csv)|*.csv|All file(*.*)|*.*",
		                         style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
		if self.dlg.ShowModal() == wx.ID_OK:
			paths = self.dlg.GetPaths()[0]

		self.dlg.Destroy()
		#print(paths)
		sqlcomnd = self.fldsql.GetValue()
		brsdb = PG.Get2(self.dbfil, u'', u'')
		self.idata = brsdb.GetFromString(sqlcomnd)
		thsfld = [F.strip('`') for t in self.ChkTicks() for F in self.ChkTicks()[t]]
		with open(paths, 'w',newline='') as csvfile:
			filwrit = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filwrit.writerow(thsfld)
			for row in self.idata:
				filwrit.writerow(row)
		event.Skip()

	def toexl( self, event ):
		from xlsxwriter.workbook import Workbook
		self.dlg = wx.FileDialog(self, _("Save as Excel file"),
		                         defaultDir=DATABASE_PATH,
		                         defaultFile="",
		                         wildcard="Excel file(*.xlsx)|*.xlsx|All file(*.*)|*.*",
		                         style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
		if self.dlg.ShowModal() == wx.ID_OK:
			paths = self.dlg.GetPaths()[0]
		self.dlg.Destroy()
		sqlcomnd = self.fldsql.GetValue()
		brsdb = PG.Get2(self.dbfil, u'', u'')
		self.idata = brsdb.GetFromString(sqlcomnd)

		workbook = Workbook(paths)
		worksheet = workbook.add_worksheet()
		r = 0

		for row in self.idata:
			c = 0
			for col in row:
				worksheet.write(r, c, col)
				c += 1
			r += 1
		workbook.close()
		event.Skip()

	def extnd( self, event ):
		wx.MessageBox(_("Please connect to our site and send your request"))
		event.Skip()

	def Splt1OnIdle( self, event ):
		self.Splt1.SetSashPosition( 255 )
		self.Splt1.Unbind( wx.EVT_IDLE )


###########################################################################
## Class MyPanel2
###########################################################################

class MyPanel2 ( wx.Panel ):

	def __init__( self, parent, fields, Data, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz = wx.BoxSizer( wx.VERTICAL )
		#self.DBF = DBF.split('\\')[-1]

		#self.idbfl = PG.Get(self.DBF, u'', u'')
		#self.idata = self.idbfl.GetFromString(u' select * from %s' %Table)
		self.idata = Data

		self.DVC1 = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_HORIZ_RULES|wx.dataview.DV_VERT_RULES )
		#self.fld1 = self.DVC1.AppendTextColumn( u"Name", 0, wx.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.DATAVIEW_COL_RESIZABLE )
		#self.fld2 = self.DVC1.AppendTextColumn( u"Name", 0, wx.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.DATAVIEW_COL_RESIZABLE )
		Vsz.Add( self.DVC1, 1, wx.ALL|wx.EXPAND, 5 )

		#for Col in range(len(self.idata[0])):
		#	self.DVC1.AppendTextColumn(u"field", -1 )
		for Col in fields:
			self.DVC1.AppendTextColumn(Col, -1 )

		for data in self.idata:
			DD = ()
			for d in data:
				DD = DD + (str(d),)
			self.DVC1.AppendItem(DD)


		self.m_button8 = wx.Button( self, wx.ID_ANY, _(u"ok"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Vsz.Add( self.m_button8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( Vsz )
		self.Layout()

		# Connect Events
		self.m_button8.Bind( wx.EVT_BUTTON, self.cols )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def cols( self, event ):
		q = self.GetParent()
		q.Close()


###########################################################################
## Class MyPanel3
###########################################################################

class MyPanel3 ( wx.Panel ):

	def __init__( self, parent,fldlst, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 396,124 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl2 = wx.StaticText( self, wx.ID_ANY, _(u"Key of Field UpDate"), wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.lbl2.Wrap( -1 )

		Hsz2.Add( self.lbl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs2Choices = fldlst
		self.chs2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs2Choices, 0 )
		self.chs2.SetSelection( 0 )
		Hsz2.Add( self.chs2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl3 = wx.StaticText( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz2.Add( self.lbl3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.codfld = wx.TextCtrl(self, wx.ID_ANY, _(u"SomeData"), wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
		Hsz2.Add(self.codfld, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		Vsz1.Add( Hsz2, 1, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )


		Hsz3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn1 = wx.Button( self, wx.ID_ANY, _(u"Cancle or Return"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btn2 = wx.Button( self, wx.ID_ANY, _(u"Ok or Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz3, 1, wx.EXPAND, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		# Connect Events
		self.btn1.Bind( wx.EVT_BUTTON, self.cncl )
		self.btn2.Bind( wx.EVT_BUTTON, self.aply )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def cncl( self, event ):
		self.acept = False
		q = self.GetParent()
		q.Close()

	def aply( self, event ):
		self.acept = True
		q = self.GetParent()
		q.Close()

###########################################################################
## Class MyPanel4
###########################################################################

class MyPanel4 ( wx.Panel ):

	def __init__( self, parent,tabls, flds1, flds2, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,175 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl1 = wx.StaticText( self, wx.ID_ANY, _(u"Base Table For Join"), wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.lbl1.Wrap( -1 )

		Hsz1.Add( self.lbl1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs1Choices = tabls
		self.chs1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs1Choices, 0 )
		self.chs1.SetSelection( 0 )
		Hsz1.Add( self.chs1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz1, 1, wx.EXPAND, 5 )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl2 = wx.StaticText( self, wx.ID_ANY, _(u"Key of Field For Join"), wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.lbl2.Wrap( -1 )

		Hsz2.Add( self.lbl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs2Choices = flds1
		self.chs2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs2Choices, 0 )
		self.chs2.SetSelection( 0 )
		Hsz2.Add( self.chs2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl3 = wx.StaticText( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz2.Add( self.lbl3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs3Choices = flds2
		self.chs3 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs3Choices, 0 )
		self.chs3.SetSelection( 0 )
		Hsz2.Add( self.chs3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz2, 1, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		#self.chk1 = wx.CheckBox( self, wx.ID_ANY, u"Use All field", wx.DefaultPosition, wx.DefaultSize, 0 )
		#Hsz3.Add( self.chk1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Hsz3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn1 = wx.Button( self, wx.ID_ANY, _(u"Cancle & Return"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btn2 = wx.Button( self, wx.ID_ANY, _(u"Ok & Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz3, 1, wx.EXPAND, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		# Connect Events
		#self.chk1.Bind( wx.EVT_CHECKBOX, self.chkall )
		self.btn1.Bind( wx.EVT_BUTTON, self.cncl )
		self.btn2.Bind( wx.EVT_BUTTON, self.aply )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	#def chkall( self, event ):
	#	event.Skip()

	def cncl( self, event ):
		self.acept = False
		q = self.GetParent()
		q.Close()

	def aply( self, event ):
		self.acept = True
		q = self.GetParent()
		q.Close()

###########################################################################
## Class MyPanel5
###########################################################################

class MyPanel5 ( wx.Panel ):

	def __init__( self, parent, Data, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 400,145 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		self.Data = Data

		Btbl = [T for T in Data.keys()]
		Bfld = [Btbl[0] + '.' + F for F in Data[Btbl[0]]]
		Jfld = [Btbl[1] + '.' + F for F in Data[Btbl[1]]]

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl1 = wx.StaticText( self, wx.ID_ANY, _(u"Base Table For Join"), wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.lbl1.Wrap( -1 )

		Hsz1.Add( self.lbl1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs1Choices = Btbl
		self.chs1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs1Choices, 0 )
		self.chs1.SetSelection( 0 )
		Hsz1.Add( self.chs1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz1, 1, wx.EXPAND, 5 )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl2 = wx.StaticText( self, wx.ID_ANY, _(u"Key of Field For Join"), wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.lbl2.Wrap( -1 )

		Hsz2.Add( self.lbl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs2Choices = Bfld
		self.chs2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs2Choices, 0 )
		self.chs2.SetSelection( 0 )
		Hsz2.Add( self.chs2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.lbl3 = wx.StaticText( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz2.Add( self.lbl3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		chs3Choices = Jfld
		self.chs3 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chs3Choices, 0 )
		self.chs3.SetSelection( 0 )
		Hsz2.Add( self.chs3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz2, 1, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )


		Hsz3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn1 = wx.Button( self, wx.ID_ANY, _(u"Cancle & Return"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btn2 = wx.Button( self, wx.ID_ANY, _(u"Ok & Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz3.Add( self.btn2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz3, 1, wx.EXPAND, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		# Connect Events
		self.chs1.Bind(wx.EVT_CHOICE, self.tblch)
		self.btn1.Bind( wx.EVT_BUTTON, self.cncl )
		self.btn2.Bind( wx.EVT_BUTTON, self.aply )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def tblch(self, event):
		n = self.chs1.GetSelection()
		#c = self.chs1.GetCount()
		#print(n,c)
		T1 = self.chs1.GetStringSelection()
		fld1 = self.Data[T1]
		self.chs2.SetItems([T1+'.'+f for f in fld1])
		if n  == 0:
			m = 1
		else:
			m = 0
		T2 = self.chs1.GetString(m)
		fld2 = self.Data[T2]
		self.chs3.SetItems([T2+'.'+f for f in fld2])

		event.Skip()

	def cncl( self, event ):
		self.acept = False
		q = self.GetParent()
		q.Close()

	def aply( self, event ):
		self.acept = True
		q = self.GetParent()
		q.Close()


