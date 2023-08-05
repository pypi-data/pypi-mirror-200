# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import datetime
import os
import shutil
import zipfile
import zipimport
import tarfile
import requests
#import cv2
import wx
import wx.xrc
import wx.dataview

from Config.Init import *
import Res.Allicons as icon

import Database.MenuSet2 as MS
import Database.PostGet as PG
import GUI.proman as pro
import importlib
#import importlib.util

import AI.Analiz
import AI.OpnSrc as OS
from AI.Analiz import *
from AI.Generats import *

_ = wx.GetTranslation

###########################################################################
## Class MyPanel7
###########################################################################

class MyPanel1 ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 570,470 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		Vsz1 = wx.BoxSizer( wx.VERTICAL )

		self.getMData = MS.GetData(u'Menu2.db', u'')
		self.setMDate = MS.SetData(u'', u'', u'')

		self.Splt1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE|wx.SP_NO_XP_THEME|wx.SP_THIN_SASH )
		self.Splt1.Bind( wx.EVT_IDLE, self.Splt1OnIdle )

		self.P1 = wx.Panel( self.Splt1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz2 = wx.BoxSizer( wx.VERTICAL )

		self.Titr1 = wx.StaticText( self.P1, wx.ID_ANY, _(u"List of Programs and Tools can download"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Titr1.Wrap( -1 )

		Vsz2.Add( self.Titr1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.TLC1 = wx.dataview.TreeListCtrl( self.P1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE )
		self.TLC1.AppendColumn( _(u"Name"), 200, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.TLC1.AppendColumn( _(u"ID"), 25, wx.ALIGN_LEFT, wx.COL_RESIZABLE )

		Vsz2.Add( self.TLC1, 1, wx.EXPAND |wx.ALL, 5 )

		#Hsz1 = wx.BoxSizer( wx.HORIZONTAL )


		#Vsz2.Add( Hsz1, 0, wx.EXPAND, 5 )

		# Hsz2 = wx.BoxSizer( wx.HORIZONTAL )
		#
		# self.CntSrv = wx.Button( self.P1, wx.ID_ANY, _(u"Connect to server "), wx.DefaultPosition, wx.DefaultSize, 0 )
		# Hsz2.Add( self.CntSrv, 1, wx.ALL, 5 )
		#
		#
		# Vsz2.Add( Hsz2, 0, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn1 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn1.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_add.png', wx.BITMAP_TYPE_ANY))
		self.btn1.SetBitmap(icon.add_package.GetBitmap())
		self.btn1.SetToolTip(_(u"Add"))
		Hsz3.Add( self.btn1, 0, wx.ALL, 5 )

		self.btn2 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn2.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_edit.png', wx.BITMAP_TYPE_ANY))
		self.btn2.SetBitmap(icon.edit_package.GetBitmap())
		self.btn2.SetToolTip(_(u"Edit"))
		Hsz3.Add( self.btn2, 0, wx.ALL, 5 )

		self.btn3 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn3.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_delete.png', wx.BITMAP_TYPE_ANY))
		self.btn3.SetBitmap(icon.delete_package.GetBitmap())
		self.btn3.SetToolTip(_(u"Delete"))
		Hsz3.Add( self.btn3, 0, wx.ALL, 5 )

		self.btn4 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn4.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_form.png', wx.BITMAP_TYPE_ANY))
		self.btn4.SetBitmap(icon.application_form.GetBitmap())
		self.btn4.SetToolTip(_(u"Preview"))
		Hsz3.Add( self.btn4, 0, wx.ALL, 5 )

		self.btn5 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn5.SetBitmap(wx.Bitmap(ICON16_PATH + u'update.png', wx.BITMAP_TYPE_ANY))
		self.btn5.SetBitmap(icon.update.GetBitmap())
		self.btn5.SetToolTip(_(u"UpDate"))
		Hsz3.Add( self.btn5, 0, wx.ALL, 5 )

		self.btn6 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn6.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_put.png', wx.BITMAP_TYPE_ANY))
		self.btn6.SetBitmap(icon.accept_button.GetBitmap())
		self.btn6.SetToolTip(_(u"Apply"))
		Hsz3.Add( self.btn6, 0, wx.ALL, 5 )

		self.btn7 = wx.BitmapButton( self.P1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		#self.btn7.SetBitmap(wx.Bitmap(ICON16_PATH + u'application_lightning.png', wx.BITMAP_TYPE_ANY))
		self.btn7.SetBitmap(icon.lightning.GetBitmap())
		self.btn7.SetToolTip(_(u"Generate"))
		Hsz3.Add( self.btn7, 0, wx.ALL, 5 )


		Vsz2.Add( Hsz3, 0, wx.EXPAND, 5 )


		self.P1.SetSizer( Vsz2 )
		self.P1.Layout()
		Vsz2.Fit( self.P1 )
		self.P2 = wx.Panel( self.Splt1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		Vsz3 = wx.BoxSizer( wx.VERTICAL )

		self.Titr2 = wx.StaticText( self.P2, wx.ID_ANY, _(u"Description"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Titr2.Wrap( -1 )

		Vsz3.Add( self.Titr2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		Hsz11 = wx.BoxSizer( wx.HORIZONTAL )

		self.Descr = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		Hsz11.Add( self.Descr, 1, wx.ALL|wx.EXPAND, 5 )


		Vsz3.Add( Hsz11, 1, wx.EXPAND, 5 )

		# Hsz12 = wx.BoxSizer( wx.HORIZONTAL )
		#
		# self.btndon = wx.Button(self.P2, wx.ID_ANY, _(u"Download"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
		# Hsz12.Add(self.btndon, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		#
		# self.gug1 = wx.Gauge(self.P2, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
		# self.gug1.SetValue(0)
		# Hsz12.Add(self.gug1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		#
		# Vsz3.Add( Hsz12, 0, wx.EXPAND, 5 )

		Hsz13 = wx.BoxSizer( wx.HORIZONTAL )

		self.extchk = wx.Button(self.P2, wx.ID_ANY, _(u"Extract, Check and Show File"), wx.DefaultPosition, wx.DefaultSize,
		                        0)
		Hsz13.Add(self.extchk, 1, wx.ALL, 5)


		Vsz3.Add( Hsz13, 0, wx.EXPAND, 5 )

		Hsz14 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl2 = wx.StaticText( self.P2, wx.ID_ANY, _(u"To Directory"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl2.Wrap( -1 )

		Hsz14.Add( self.lbl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dir2 = wx.DirPickerCtrl( self.P2, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
		Hsz14.Add( self.dir2, 1, wx.ALL, 5 )


		Vsz3.Add( Hsz14, 0, wx.EXPAND, 5 )

		self.lin1 = wx.StaticLine( self.P2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		Vsz3.Add( self.lin1, 0, wx.EXPAND |wx.ALL, 5 )

		# Hsz15 = wx.BoxSizer( wx.HORIZONTAL )
		#
		# self.chk1 = wx.CheckBox( self.P2, wx.ID_ANY, _(u"Check it ..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		# Hsz15.Add( self.chk1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		# Vsz3.Add( Hsz15, 0, wx.EXPAND, 5 )

		Hsz16 = wx.BoxSizer( wx.VERTICAL )

		self.lbl3 = wx.StaticText( self.P2, wx.ID_ANY, _(u"Message"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz16.Add( self.lbl3, 0, wx.ALL, 5 )

		self.msag = wx.TextCtrl( self.P2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		Hsz16.Add( self.msag, 1, wx.ALL|wx.EXPAND, 5 )


		Vsz3.Add( Hsz16, 1, wx.EXPAND, 5 )


		self.P2.SetSizer( Vsz3 )
		self.P2.Layout()
		Vsz3.Fit( self.P2 )
		self.Splt1.SplitVertically( self.P1, self.P2, 255 )
		Vsz1.Add( self.Splt1, 1, wx.EXPAND, 5 )

		self.filllist()


		self.SetSizer( Vsz1 )
		self.Layout()

		self.listfilezip = []
		self.infopacktxt = []

		# Connect Events
		self.TLC1.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.slctitm, id=wx.ID_ANY)
		#self.CntSrv.Bind( wx.EVT_BUTTON, self.consrv )
		self.btn1.Bind( wx.EVT_BUTTON, self.addit )
		self.btn2.Bind( wx.EVT_BUTTON, self.editit )
		self.btn3.Bind( wx.EVT_BUTTON, self.delit )
		self.btn4.Bind( wx.EVT_BUTTON, self.prw )
		self.btn5.Bind( wx.EVT_BUTTON, self.upd )
		self.btn6.Bind( wx.EVT_BUTTON, self.aply )
		self.btn7.Bind( wx.EVT_BUTTON, self.gnrt )
		#self.btn8.Bind( wx.EVT_BUTTON, self.mnuid )
		#self.btndon.Bind(wx.EVT_BUTTON, self.dnlod)
		self.extchk.Bind(wx.EVT_BUTTON, self.extrc)
		self.dir2.Bind( wx.EVT_DIRPICKER_CHANGED, self.thsdir )
		#self.btn9.Bind( wx.EVT_BUTTON, self.dnlod )
		#self.chk1.Bind( wx.EVT_CHECKBOX, self.chkdon )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def filllist(self):

		Aroot = self.TLC1.GetRootItem()
		self.root1 = self.TLC1.AppendItem(Aroot, "Programs you Download it")
		self.root2 = self.TLC1.AppendItem(Aroot, "Programs in your Account")
		self.root3 = self.TLC1.AppendItem(Aroot, "Programs that you Upload ")
		self.root4 = self.TLC1.AppendItem(Aroot, "Unpacked downloaded Programs")
		#self.root5 = self.TLC1.AppendItem(Aroot, "Programs file in your HDD ")

		dirct = ['Downloads','Account','Uploads','Fount']
		dirdt2 = ['API', 'AUI', 'GUI', 'MLA', 'MLP', 'PRG']
		dcods = {'API': 6122, 'AUI': 6155, 'PRG': 6111, 'GUI': 6177, 'MLA': 6133, 'MLP': 6144}
		roots = [self.root1,self.root2,self.root3,self.root4]
		#roots = [self.root1,  self.root3, self.root4]
		i=0
		for d in dirct:
			mylist = os.listdir(UTILITY_PATH+d+'\\')
			if i == 3:
				for d in dirdt2:
					mylist2 = os.listdir(UTILITY_PATH + 'Fount\\' + d + '\\')
					mychild = self.TLC1.AppendItem(self.root4, 'Unpacked')
					self.TLC1.SetItemText(mychild, 0, d)
					self.TLC1.SetItemText(mychild, 1, str(dcods[d])[-3:])
					for file in mylist2:
						if file != '__init__.py' and file != '__pycache__':
							child2 = self.TLC1.AppendItem(mychild, d)
							self.TLC1.SetItemText(child2, 0, file)
							self.TLC1.SetItemText(child2, 1, str(dcods[d]))
				for f in mylist:
					if f != '__init__.py' and f != '__pycache__' and f not in dirdt2:
						mychld = self.TLC1.AppendItem(self.root4,d)
						self.TLC1.SetItemText(mychld,0,f)
						self.TLC1.SetItemText(mychld,1,'^^^')

			else:
				for fil in mylist:
					if fil != '__init__.py' and fil != '__pycache__':
						myfil = fil.replace(UTILITY_PATH+d+'\\','')
						mychld = self.TLC1.AppendItem(roots[i],d)
						self.TLC1.SetItemText(mychld,0,myfil)
						self.TLC1.SetItemText(mychld,1,'>>>')
			i += 1


	def fillfilds(self, Data):
		self.Descr.SetValue(Data[0])
		#self.fld1.SetValue(Data[1])
		self.dir2.SetPath(Data[1])
		self.Refresh()
		self.Layout()

	def slctitm(self, event):
		D = ['','','']
		self.fillfilds(D)
		itm = self.TLC1.GetSelection()
		if itm:
			txt = self.TLC1.GetItemText(itm, 0)
			cod = self.TLC1.GetItemText(itm, 1)
			par = self.TLC1.GetItemParent(itm)
			rot = self.TLC1.GetItemText(par, 0)
		else:
			txt = ''
			code = 6666
		#print(txt,rot)
		if 'Download' in txt :
			Discrpt = "Programs you download from Site in to your HardDisk"
			Pathsrc = UTILITY_PATH+'Downloads'
		elif 'Upload' in txt:
			Discrpt = "Programs that you Upload to your Account for Sell or Send"
			Pathsrc = UTILITY_PATH+'Uploads'
		elif 'Unpacked' in txt:
			Discrpt = "Unpacked program that download from Site and see files in it"
			Pathsrc = UTILITY_PATH+'Account'

		else:
			if 'pack' in txt and not '.sfn' in txt and cod == '>>>': # and 'Download' in rot:
				if 'Download' in rot:
					ipath = UTILITY_PATH+'Downloads'+SLASH
				if 'Upload' in rot:
					ipath = UTILITY_PATH+'Uploads'+SLASH
				with zipfile.ZipFile(ipath+txt,'r') as zf:
					for ifi in zf.namelist():
						if '.sfn' in ifi:
							itxt = zf.read(ifi)
				Discrpt = self.ShowDscr(itxt)
				Pathsrc = UTILITY_PATH+"Fount"
			elif '.sfn' in txt:
				with open(UTILITY_PATH+"Fount"+SLASH+txt, 'r', encoding='utf-8') as f:
					itxt=bytes(f.read(), 'utf-8')
				Discrpt = self.ShowDscr(itxt)
				Pathsrc = UTILITY_PATH+"Fount"
			else:
				Discrpt = ""
				Pathsrc = ""

		D = [Discrpt,Pathsrc]
		self.fillfilds(D)
		if '.py' in txt:
			self.thsfile = UTILITY_PATH+'Fount\\'+rot+SLASH+txt
		else:
		 	self.thsfile = ''
		#print(self.thsfile)

	def ShowDscr( self, sfntxt):
		#print(sfntxt)
		txt = sfntxt.decode('utf-8')
		#print(txt.find('*/'))
		idx = txt.find('*/')
		if idx != -1:
			#print(txt[idx+2:])
			return txt[idx+2:]
		else:
			return ''

	def addit( self, event ):
		def addzip(izipname,chld2):
			thsfil,pthcod = self.slctfil()
			#print(thsfil,pthcod)
			if thsfil == '':
				wx.MessageBox(_(" The file is in Zip file Please select new file!"))
			elif thsfil == -1:
				wx.MessageBox(_("Only file in Src Directory path send to zip file"))
			else:
				self.listfilezip.append(thsfil)
				self.add2zip(izipname, chld2,str(pthcod) )

		itm = self.TLC1.GetSelection()
		if itm.IsOk() :
			txt = self.TLC1.GetItemText(itm, 0)
		else:
			txt = ''
		#print(txt)

		if 'Upload' in txt:
			ischld =  self.TLC1.GetNextItem(itm)
			if 'download' in self.TLC1.GetItemText(ischld, 0):
				addtim = datetime.datetime.now().isoformat(timespec='minutes').replace(':','_').replace('-','_')
				izipname = 'packzip'+addtim+'.tm5'
				chld2 = self.TLC1.AppendItem(self.root3,izipname)
				self.TLC1.SetItemText(chld2,0,izipname)
				self.TLC1.SetItemText(chld2,1,'6666')
				addzip(izipname,chld2)
			else:
				if 'packzip' in self.TLC1.GetItemText(ischld, 0):
					izipname = self.TLC1.GetItemText(ischld, 0)
					chld2 = ischld
					addzip(izipname,chld2)
		else:
			ischld = self.TLC1.GetNextItem(itm)
			if 'packzip' in txt:
				izipname = self.TLC1.GetItemText(ischld, 0)
				chld2 = self.TLC1.GetSelection()
				addzip(izipname,chld2)
				#print(self.TLC1.GetItemText(itm, 0))
		#print(self.listfilezip)
		#self.add2zip(izipname,chld2)
		event.Skip()

	def slctfil(self):
		dlg = wx.FileDialog(self,'Select your Source Code',SRC_PATH,wildcard ='*.*' ,style=wx.FD_DEFAULT_STYLE)
		dlg.ShowModal()
		myfile = dlg.GetPath()
		dlg.Destroy()
		if myfile in self.listfilezip:
			return '',''
		for src in Src_Pth:
			if src.capitalize() in myfile.capitalize():
				#self.writinfo(myfile.capitalize().replace(src.capitalize(),''),Src_Dir[Src_Pth[src]],Src_Pth[src],str(os.stat(myfile).st_size))
				self.writinfo(myfile.split("\\")[-1], Src_Dir[Src_Pth[src]], Src_Pth[src],str(os.stat(myfile).st_size))
				return myfile,Src_Dir[Src_Pth[src]]
		return -1,-1

	def writinfo(self, file, code,titl,size):
		self.infopacktxt.append((titl,str(code),file,size))

	def editit( self, event ):
		itm = self.TLC1.GetSelection()
		txt = self.TLC1.GetItemText(itm, 0)
		cod = self.TLC1.GetItemText(itm, 1)
		#print(txt,cod)
		if cod != '' and cod.isdigit() and cod != '6666':
			myindx = iter(self.infopacktxt)
			#print(self.infopacktxt)
			for i in range(len(self.infopacktxt)):
				if txt in next(myindx):
					#print(i)
					self.infopacktxt.remove(self.infopacktxt[i])
					for i, v in enumerate(self.listfilezip):
						if txt in v:
							self.listfilezip.remove(self.listfilezip[i])
					thsfil, pthcod = self.slctfil()
					self.ins2zip( itm,thsfil,str(pthcod) )
					self.listfilezip.append(thsfil)
		#else:
		#	print('Not this')
		#print(self.infopacktxt)
		#print(self.listfilezip)
		event.Skip()

	def delit( self, event ):
		itm = self.TLC1.GetSelection()
		txt = self.TLC1.GetItemText(itm, 0)
		cod = self.TLC1.GetItemText(itm, 1)
		#print(txt, cod)
		if cod != '' and cod.isdigit() and cod != '6666':
			for indx,item in enumerate(self.infopacktxt):
				if txt in item:
					#print(indx)
					self.infopacktxt.remove(item)
					self.del2zip(itm)
					for i, v in enumerate(self.listfilezip):
						if txt in v:
							self.listfilezip.remove(self.listfilezip[i])

		#print(self.infopacktxt)
		#print(self.listfilezip)
		event.Skip()

	def prw( self, event ):
		txt = self.TLC1.GetItemText(self.TLC1.GetSelection(), 0)
		rot = self.TLC1.GetItemParent(self.TLC1.GetSelection())
		roottxt = self.TLC1.GetItemText(rot, 0)
		if '.py' in txt:
			self.Frm = wx.Frame(self, style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)
			self.Pnl = OS.SrcPanel(self.Frm, self.thsfile)
			self.Frm.SetMenuBar(OS.MyMenuBar1(u'Pro'))
			self.Frm.SetSize((700, 560))
			self.Frm.SetLabel(self.thsfile)
			self.Frm.Show()
		event.Skip()

	def upd( self, event ):
		self.TLC1.DeleteAllItems()
		self.filllist()
		self.Refresh()
		event.Skip()

	def aply( self, event ):
		itm = self.TLC1.GetSelection()
		if itm:
			txt = self.TLC1.GetItemText(itm, 0)
			cod = self.TLC1.GetItemText(itm, 1)
			par = self.TLC1.GetItemParent(itm)
			rot = self.TLC1.GetItemText(par, 0)
		if self.dir2.GetPath() == '' or self.dir2.GetPath() == UTILITY_PATH+'Fount':
			wx.MessageBox(_("Please Change your path or select a correct path"))
			return

		if '.sfn' in txt:
			with open(UTILITY_PATH+'Fount'+SLASH+txt, 'r', encoding='utf-8') as f:
				if_lst = self.list_py_file( f.readlines() )
			#print(if_lst)
			if SRC_PATH not in self.dir2.GetPath():
				print(SRC_PATH, self.dir2.GetPath())
			for i in if_lst:
				if 'PRG' in i[0]:
					shutil.copy(UTILITY_PATH+'Fount'+SLASH+i[0]+SLASH+i[2],self.dir2.GetPath())
				else:
					shutil.copy(UTILITY_PATH + 'Fount' + SLASH + i[0] + SLASH + i[2], SRC_PATH+i[0])

			wx.MessageBox(_(" All file Successfull copy to Src path"))

			shutil.make_archive( UTILITY_PATH+'Account'+SLASH+txt , 'tar', UTILITY_PATH + 'Fount')
			answer=wx.MessageBox(_("We Pack tar file all file to Account path Do you like delete file ?"),style=wx.YES_NO)
			if answer==2:
				os.remove(UTILITY_PATH+'Fount'+SLASH+txt)
				for j in if_lst:
					os.remove(UTILITY_PATH+'Fount'+SLASH+j[0]+SLASH+j[2])
			pass
		event.Skip()

	def list_py_file(self, txtlins):
		mylst = []
		for t in txtlins:
			if '/*' not in t:
				mylst.append(t.replace('\n','').split(','))
		return mylst

	def gnrt( self, event ):

		txt = self.TLC1.GetItemText(self.TLC1.GetSelection(),0)
		rot = self.TLC1.GetItemParent(self.TLC1.GetSelection())
		roottxt = self.TLC1.GetItemText(rot,0)
		if 'packzip' in txt and 'Upload' in roottxt:
			with open(TEMPS_PATH + 'infopack'+txt.lstrip('packzip').rstrip('.tm5')+'.sfn', 'a', encoding='utf-8') as f:
				for t in self.infopacktxt:
					#print(t[2])
					f.write(t[0]+','+t[1]+','+t[2]+','+t[3]+'\n')
				f.write('/*=========Desc.=========*/\n'+self.Descr.GetValue())

			for fil in self.listfilezip:
				shutil.copy(fil, TEMPS_PATH)

			with zipfile.ZipFile(UTILITY_PATH+'Uploads'+SLASH+txt,'w', compression=zipfile.ZIP_DEFLATED) as zp:
				self.zipdir(TEMPS_PATH, zp)

			for zf in os.listdir(TEMPS_PATH):
				if os.path.isfile(TEMPS_PATH+zf):
					os.unlink(TEMPS_PATH+zf)

			self.TLC1.DeleteAllItems()
			self.filllist()
			self.Refresh()


		event.Skip()

	def zipdir(self, path, ziph):
		# ziph is zipfile handle
		for root, dirs, files in os.walk(path):
			for file in files:
				ziph.write(path+file,file)
	# def mnuid( self, event ):
	# 	event.Skip()
	def add2zip(self,zipname,child,pathcod):
		SP1 = {v: k for k, v in Src_Pth.items()}
		SD1 = {v: k for k, v in Src_Dir.items()}
		chld3 = self.TLC1.AppendItem(child,zipname)
		#print(self.listfilezip[-1].split('\\')[-1])
		#self.TLC1.SetItemText(chld3,0,self.listfilezip[-1].capitalize().replace(SP1[SD1[int(pathcod)]].capitalize(),''))
		self.TLC1.SetItemText(chld3, 0,self.listfilezip[-1].split('\\')[-1])
		self.TLC1.SetItemText(chld3,1,pathcod)

	def ins2zip(self, itm, filname, pathcod):
		SP1 = {v: k for k, v in Src_Pth.items()}
		SD1 = {v: k for k, v in Src_Dir.items()}

		self.TLC1.SetItemText(itm, 0, filname.replace(SP1[SD1[int(pathcod)]],'').split('\\')[-1])
		self.TLC1.SetItemText(itm, 1, pathcod)

	def del2zip(self, itm):
		self.TLC1.DeleteItem(itm)

	def thsdir( self, event ):
		event.Skip()

	# def dnlod( self, event ):
	# 	event.Skip()

	def extrc(self, event):
		txt = self.TLC1.GetItemText(self.TLC1.GetSelection(), 0)
		rot = self.TLC1.GetItemParent(self.TLC1.GetSelection())
		roottxt = self.TLC1.GetItemText(rot, 0)
		msg = ''
		nmlst = ''

		if 'Download' in roottxt:
			#print(txt)
			with zipfile.ZipFile(UTILITY_PATH+'Downloads'+SLASH+txt,'r') as fz:
				namelist = fz.namelist()
				#print(namelist)
				for nl in namelist:
					if '.sfn' in nl:
						fz.extract(nl,UTILITY_PATH+'Fount')
						nmlst = nl
			if nmlst != '':
				with open(UTILITY_PATH+'Fount'+SLASH+nmlst,'r') as f:
					lstfil = f.readlines()
				for fl in lstfil:
					if '/*' in fl:
						break
					finfo = fl.split(',')
					msg += 'Copy file Src/%s [%s] size %s'%(finfo[0]+'/'+finfo[2],finfo[1],finfo[3])
					self.msag.SetValue(msg)
					with zipfile.ZipFile(UTILITY_PATH + 'Downloads' + SLASH + txt, 'r') as fz:
						fz.extract(finfo[2],UTILITY_PATH+'Fount'+SLASH+finfo[0])
				#shutil.copy(TEMPS_PATH+fl,)
		event.Skip()

	def Splt1OnIdle( self, event ):
		self.Splt1.SetSashPosition( 255 )
		self.Splt1.Unbind( wx.EVT_IDLE )

