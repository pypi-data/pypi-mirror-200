#In the name of GOD
#This program check menu2.db and program structure
# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os


## ====================Open Database======================
import Database.MenuSet2 as MS

from Config.Init import *

Get2Menu = MS.GetData(u'Menu2.db', u'')
Set2Menu = MS.SetData(u'', u'', u'')

##====================Control Table Shame ================
def TestShame():
    Tables = {'Guidir':['Dir','prgdir','hdddir'],'MLAlgo':['MLcod','MLAsrc'],
              'MLPane':['MLPid','MLPfile'],'MLinfo':['MLPid','MLname','MLcod'],
              'PrgDesc':['handlerid','Description'],'access':['acclvlid','userid','acclvl','disenable'],
              'extended':['extid','status','icon','shortcut','help','acclvlid','grpid'],
              'grpitem':['grpid','grpname','grpcnt','grpnl','grpth'],
              'handler':['hamdlerid','prgname','prgdir','paramtr','public','prgno'],
              'menubar':['mbarid','mbarname','mbardir','acclvlid'],
              'mitem':['mbarid','itemid','itemname','itemtyp','extid','handlerid'],
              'panifo':['paninfoid','caption','setting','resize','bstsiz','minsiz','maxsiz','docking','position'],
              'pans':['panid','panname','pandok','pansiz','panlyr','paninfoid','handlerid','acclvlid'],
              'security':['userid','username','password'],
              'toolbar':['toolid','toolname','toolicon','shrttxt','lngtxt','handlerid','acclvlid','tooltype']}
    for t in Tables:
        print(t,Tables[t])

##====================Test Src Directory==================
def TestSrcDir():
	lstHdd = os.listdir(SRC_PATH)
	lstHDDPRG = os.listdir(Src_prg)
	lstDBF = Get2Menu.AllGuiDir()
	#print(lstDBF,lstHdd)
	lstDDb = [d[2].replace('..\\Src\\','') for d in lstDBF]
	#print(lstDDb)
	for row in lstDBF:
		if row[2].replace('..\\Src\\','') in lstHdd:
			print(row,'--------ok')
		elif row[2].replace(Src_prg,'') in lstHDDPRG:
			print(row,'--------ok')
		elif row[2] == '..\\GUI\\Main':
			print(row,'--------ok')
		elif row[2] == '..\\GUI\\Temp':
			print(row,'--------ok')
		else:
			print("this row had a problem",row,'--------',Src_prg)


def TestHandler():
	Allhandler = Get2Menu.AllHndl()
	MainPrgFile = os.listdir(GUI_PATH+'Main\\')
	MitemHandlr = []
	print(Allhandler)
	for row in Allhandler:
		MitemHandlr.append(row)
		if row[1] == 'Demo':
			if row[2][1:3] != str(row[0])[-2:]:
				print("you must change this row:",row)
		elif row[1]+'.py' in MainPrgFile:
			print(row,'--------ok')
		else:
			print(row,'---Other ')
			#MitemHandlr.append(row)

	print(MitemHandlr)
	allhandid = [h[0] for h in MitemHandlr]
	print(allhandid)
	for mitm in Get2Menu.AllSub():
		if mitm[5] in allhandid:
			print(mitm,'--------ok')
		else:
			print("Handler id is not in database: ",mitm)


def main():
	TestSrcDir()
	TestHandler()

if __name__=='__main__':
	main()
