# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import numpy as np

###########################################################################
## Class MyPanel2
###########################################################################

class MyPanel2 ( wx.Panel ):

	def __init__( self, parent,testdata, leblslst, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.conmatrix = np.array(testdata)
		rowc , colc = self.conmatrix.shape


		Vsz1 = wx.BoxSizer( wx.VERTICAL )


		self.grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.grid1.CreateGrid( rowc, colc )
		self.grid1.EnableEditing( True )
		self.grid1.EnableGridLines( True )
		self.grid1.EnableDragGridSize( False )
		self.grid1.SetMargins( 0, 0 )

		# Columns
		self.grid1.EnableDragColMove( False )
		self.grid1.EnableDragColSize( True )
		self.grid1.SetColLabelSize( 30 )
		for i in range(len(leblslst)):
			self.grid1.SetColLabelValue(i,leblslst[i])
		self.grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.grid1.EnableDragRowSize( True )
		self.grid1.SetRowLabelSize( 80 )
		for j in range(len(leblslst)):
			self.grid1.SetRowLabelValue( j, leblslst[j] )
		self.grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		Vsz1.Add( self.grid1, 0, wx.ALL|wx.EXPAND, 5 )

		Hsz1 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl1 = wx.StaticText( self, wx.ID_ANY, u"Per acc", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl1.Wrap( -1 )

		Hsz1.Add( self.lbl1, 1, wx.ALL, 5 )

		self.ClsLbls = []
		for a in leblslst:
			self.ClsLbls.append(   wx.StaticText( self, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.DefaultSize, 0 ) )
			self.ClsLbls[-1].Wrap( -1 )

			Hsz1.Add( self.ClsLbls[-1], 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz1, 1, wx.EXPAND, 5 )

		Hsz2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl2 = wx.StaticText( self, wx.ID_ANY, u"F1 scores", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl2.Wrap( -1 )

		Hsz2.Add( self.lbl2, 1, wx.ALL, 5 )

		self.F1Lbls = []
		for a in leblslst:
			self.F1Lbls.append(  wx.StaticText( self, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.DefaultSize, 0 ) )
			self.F1Lbls[-1].Wrap( -1 )

			Hsz2.Add( self.F1Lbls[-1], 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		Vsz1.Add( Hsz2, 1, wx.EXPAND, 5 )

		Hsz3 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl3 = wx.StaticText( self, wx.ID_ANY, u"Total accuracy:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl3.Wrap( -1 )

		Hsz3.Add( self.lbl3, 0, wx.ALL, 5 )

		self.Totlac = wx.StaticText( self, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Totlac.Wrap( -1 )

		Hsz3.Add( self.Totlac, 0, wx.ALL, 5 )


		Vsz1.Add( Hsz3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		Hsz4 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl4 = wx.StaticText( self, wx.ID_ANY, u"F1 average:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl4.Wrap( -1 )

		Hsz4.Add( self.lbl4, 0, wx.ALL, 5 )

		self.F1Avg = wx.StaticText( self, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.F1Avg.Wrap( -1 )

		Hsz4.Add( self.F1Avg, 0, wx.ALL, 5 )


		Vsz1.Add( Hsz4, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		Hsz5 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		Hsz5.Add( self.btn, 0, wx.ALL, 5 )


		Vsz1.Add( Hsz5, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( Vsz1 )
		self.Layout()

		self.FillGrid()

		# Connect Events
		self.btn.Bind( wx.EVT_BUTTON, self.closit )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def closit( self, event ):
		q = self.GetParent()
		q.Close()
		event.Skip()

	def FillGrid(self):
		i = j = 0
		for r in self.conmatrix.tolist():
			for c in r:
				self.grid1.SetCellValue(i,j,str(c))
				j += 1
			i += 1
			j = 0
		self.Comput_Accuracy_F1s()
		self.Comput_Total_Accuracy()


	def Item_Acc_F1(self, i):
		TP = self.conmatrix[i][i]
		FP = 0
		FN = 0
		TN = 0
		for m in range(len(self.conmatrix)):
			if m != i:
				FP += self.conmatrix[i][m]
		for m in range(len(self.conmatrix)):
			if m != i:
				FN += self.conmatrix[m][i]
		for m in range(len(self.conmatrix)):
			for n in range(len(self.conmatrix)):
				if m != i and n != i:
					TN += self.conmatrix[m][n]
		return (TP+TN)/(self.conmatrix.sum()),2*TP/(2*TP+FP+FN)

	def Comput_Accuracy_F1s(self):
		#for i in range(len(self.ClsLbls)):
		AvgF1 = 0
		for i in range(len(self.F1Lbls)):
			Acc,F1 =  self.Item_Acc_F1(i)
			AvgF1 += F1
			self.F1Lbls[i].SetLabel(str(round(F1,3)))
			self.ClsLbls[i].SetLabel(str(round(Acc,3)))
		AvgF1 = AvgF1 / len(self.F1Lbls)
		self.F1Avg.SetLabel(str(round(AvgF1,3)))
		pass


	def Comput_Total_Accuracy(self):
		TAcc = 0
		for i in range(len(self.conmatrix)):
			TAcc += self.conmatrix[i][i]
		TAcc = TAcc / self.conmatrix.sum()
		self.Totlac.SetLabel(str(round(TAcc,3)))



