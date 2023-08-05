# In the name of God
# Cearte Menu main Frame File
# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import Database.MenuSet2 as MS
from  Allimp import os, sys, wx
from Config.Init import *

_ = wx.GetTranslation


class MenuData(object):
    def __init__(self,userid):
        self.MySql = MS.GetData(u'Menu2.db', u'')
        self.ToSql = MS.SetData(u'', u'',u'')
        self.userid = userid


    def menuBar(self):
        self.mbar = []
        for row in self.MySql.AmenuBar(ext=' and access.userid = %d and menubar.mbarid < 9999  '%self.userid):
            self.mbar.append(row)
        return self.mbar

    def menuBar2(self):
        self.mbar = []
        for row in self.MySql.AmenuBar2(ext=' and menubar.mbarid < 9999  ', userid=self.userid):
            self.mbar.append(row)
        return self.mbar


    def menuItem2(self, i):
        #bitm = self.MySql.AmenuItm(i," order by mitem.itemid ")
        bitm = self.MySql.AmenuItm2(i," order by mitem.itemid ",self.userid)
        mitem = []
        for itm in bitm:
            if itm[-3] == 'S':
                sitem = []
                sitem.append(itm)
                sitem.append(self.menuItem2(itm[0]))
                mitem.append(sitem)
            else:
                mitem.append(itm)
        return mitem

    def menuDir(self):
        self.Bdir = self.MySql.DirBar()
        self.mdir = []
        for row in self.Bdir:
            self.mdir.append(row)
        # print self.mdir
        return self.mdir


class AppMenu(wx.MenuBar):
    Lstmnu = []
    Lstsub = []
    def __init__(self,usrid=1):
        wx.MenuBar.__init__(self, style=0)
        self.m = MenuData(usrid)
        self.userid = usrid

        #print(self.m.userid,self.userid,usrid)
        self.createMenuBar()

    def createMenuBar(self):
        for eachmenu in self.m.menuBar2():
            menutitle = eachmenu[1]
            #print('MenuItem 2:',self.m.menuItem2(eachmenu[0]))
            #self.Append(self.createMenuItem(self.m.menuItem(eachmenu[0])),menutitle)
            self.Append(self.createMenuItem2(self.m.menuItem2(eachmenu[0])), menutitle)
        return self

    def createMenuItem2(self, menudata):
        menu = wx.Menu()
        self.Lstmnu.append(menu)
        #print(menudata)
        for eachitem in menudata:
            #print(eachitem)
            if type(eachitem) != list :
                eachid, eachlabel, eachstatus, shortcut, eachicon, eachtype, eachacc, eachdisbl = eachitem
                if eachacc == '0000':
                    continue

                if not eachlabel:
                    menu.AppendSeparator()
                    continue
                else:
                    itmlbl = eachlabel
                    if shortcut != '':
                        itmlbl += '\t' + shortcut
                if eachtype == 'C':
                    menuitem = menu.AppendCheckItem(eachid, itmlbl, eachstatus)
                elif eachtype == 'R':
                    menuitem = menu.AppendRadioItem(eachid, itmlbl, eachstatus)
                elif eachtype == 'N':
                    menuitem = menu.Append(eachid, itmlbl, eachstatus)
                #elif eachtype == 'S':
                #    self.menu.AppendSubMenu(self.createMenuItem2(eachitem), eachlabel, eachstatus)
                    #return self.menu

                else:
                    wx.MessageBox(_('Error In Menu Database. Please connect to Programmer'))
                if eachicon != None and eachicon != '':
                    menuitem.SetBitmap(wx.Bitmap(ICONS_MENU + eachicon, wx.BITMAP_TYPE_ANY))
                #print(eachacc,eachdisbl)
                if eachdisbl:
                    menuitem.Enable(True)
                else:
                    menuitem.Enable(False)

            elif type(eachitem) == list:
                #print('This list send:', eachitem[1])
                subroot = self.createMenuItem2(eachitem[1])
                menuitem = menu.AppendSubMenu(subroot, eachitem[0][1])
                self.Lstsub.append(subroot)
                #self.createMenuItem2(eachitem)
                pass
            else:
                wx.MessageBox(_('Error In Menu Database. Please connect to Programmer'))
        return menu

    def Onmenu(self, event):
        self.mid = event.GetId()

    def GetItemId(self):
        return self.GetMenus()[0]

    def AddItem2(self, Mbar, Data, Bar=''):
        lbl = self.ChkShrtCut(Data)

        if self.FindMenu(Mbar) != -1:
            imnu = self.GetMenu(self.FindMenu(Mbar))
        else:
            if Bar == 'S':
                imnu = self._findsubmenu2(Mbar)
            else:
                imnu = self._findmenu2(Mbar, Bar)
            #imnu = self.FindMenuItem(mb.GetMenu,Mbar)
        #print(imnu)
        if imnu == None:
            imnu = self._findmenu3(Mbar, Bar)
            iitm = imnu.Append(int(Data[0]), lbl, Data[5])
        else:
            iitm = imnu.Append(int(Data[0]), lbl, Data[5])
        if Data[3] != '':
            iitm.SetBitmap(wx.Bitmap(ICONS_MENU + Data[3], wx.BITMAP_TYPE_ANY))

    def AddSubMenu2(self,Mbar,Data,Bar=''):
        lbl = self.ChkShrtCut(Data)
        #print(self.FindMenu(Mbar))
        if self.FindMenu(Mbar) != -1:
            imnu = self.GetMenu(self.FindMenu(Mbar))
        else:
            if Bar == 'S':
                imnu = self._findsubmenu(Mbar)
            else:
                imnu = self._findmenu2(Mbar, Bar)
        iitm = imnu.AppendSubMenu(self.createSubmenu(Data[0],lbl),lbl)
        if Data[3] != '':
            iitm.SetBitmap(wx.Bitmap(ICONS_MENU + Data[3], wx.BITMAP_TYPE_ANY))

    def createSubmenu(self, mroot, title = '' ):
        mroot = wx.Menu()
        mroot.SetTitle(title)
        self.Lstsub.append(mroot)
        return mroot

    def AddSepar(self,title):
        imnubar = self.FindMenu(title)
        itmmnu = self.GetMenu(imnubar)
        #print(itmmnu)
        itmmnu.AppendSeparator()

    # def AddCheck(self,Mbar,Data,Bar=''):
    #     imnu = self._BackMyMenu(Mbar)
    #     lbl = self.ChkShrtCut(Data)
    #     iitm = imnu.AppendCheckItem(int(Data[0]),lbl,Data[5])

    def AddCheck2(self,Mbar,Data,Bar=''):
        lbl = self.ChkShrtCut(Data)
        if self.FindMenu(Mbar) != -1:
            imnu = self.GetMenu(self.FindMenu(Mbar))
        else:
            if Bar == 'S':
                imnu = self._findsubmenu2(Mbar)
            else:
                imnu = self._findmenu2(Mbar, Bar)
        if imnu == None:
            imnu = self._findmenu3(Mbar, Bar)
            iitm = imnu.AppendCheckItem(int(Data[0]),lbl,Data[5])
        else:
            iitm = imnu.AppendCheckItem(int(Data[0]),lbl,Data[5])

    # def AddRadio(self,Mbar,Data,Bar=''):
    #     imnu = self._BackMyMenu(Mbar)
    #     lbl = self.ChkShrtCut(Data)
    #     iitm = imnu.AppendRadioItem(int(Data[0]), lbl)

    def AddRadio2(self,Mbar,Data,Bar=''):
        lbl = self.ChkShrtCut(Data)
        if self.FindMenu(Mbar) != -1:
            imnu = self.GetMenu(self.FindMenu(Mbar))
        else:
            if Bar == 'S':
                imnu = self._findsubmenu2(Mbar)
            else:
                imnu = self._findmenu2(Mbar, Bar)
        if imnu == None:
            imnu = self._findmenu3(Mbar, Bar)
            iitm = imnu.AppendRadioItem(int(Data[0]), lbl)
        else:
            iitm = imnu.AppendRadioItem(int(Data[0]), lbl)

    def _findmenu2(self, Mbar, Bar):
        mw = self.FindWindowByName('main')
        mb = mw.GetMenuBar()
        if Bar != 'S':
            return mb.GetMenu(mb.FindMenu(Mbar))
        else:
            #print(self.Lstsub)
            for m in self.Lstsub:
                #print(m.GetTitle())
                if m.GetTitle() == '' or m.GetTitle() == Mbar:
                    #print(m)
                    return m

    def _findmenu3(self, Mbar, Bar):
        mw = self.FindWindowByName('main')
        mb = mw.GetMenuBar()
        if Bar == 'S':
            for m in mb.GetMenus():
                mbr, lbl = m
                #print(mbr, lbl)
                if mbr.FindItem(Mbar) != -1:
                    #print( mbr.FindItem(Mbar) )
                    iid = mbr.FindItem(Mbar)
                    #print(mbr.FindItem(iid)[0].GetSubMenu())
                    return mbr.FindItem(iid)[0].GetSubMenu()

    def _BackMyMenu(self,Mbar):
        imnubar = self.FindMenu(Mbar)
        itmmnu = self.GetMenu(imnubar)
        #print(itmmnu)
        return itmmnu

    def _findsubmenu(self,Sub):
        lstbar = self.GetMenus()
        for bar in lstbar:
            lst = bar[0].GetMenuItems()
            for l in lst:
                if l.IsSubMenu() and l.GetItemLabel() == Sub:
                    #print(l.GetSubMenu())
                    return l.GetSubMenu()

    def _findsubmenu2(self, Sub):
        for bar in self.Lstmnu:
            lst = bar.GetMenuItems()
            for l in lst:
                #print(l.IsSubMenu(), l.GetItemLabel())
                if l.IsSubMenu() and l.GetItemLabel() == Sub:
                    return l.GetSubMenu()


    def ChkShrtCut(self,Data):
        if Data[4] != '':
            return Data[2]+'\t'+Data[4]
        else:
            return Data[2]