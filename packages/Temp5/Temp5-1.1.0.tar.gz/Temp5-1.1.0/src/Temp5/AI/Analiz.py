#In the name of God
# -*- coding: utf-8 -*-
#!usr/bin/env python

from wx.py import frame,filling,pseudo
import re

class Anlzfil(object):
    def __init__(self, pyFile):
        self.pyFile = pyFile
        self.imprts = []
        self.objcts = {}
        self.pmodls = {}

    def parsefil(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as fpy:
            linsred = fpy.readlines()
            d = 1
            for ln in linsred:
                if 'import' in ln:
                    #print(ln)
                    self.imprts.append(ln)
                if 'class' in ln:
                    #print(ln)
                    i = pseudo.PseudoFile.readline(self.pyFile)
                    #print(dir(i))
                    self.objcts['class'] = ln
                if 'def' in ln:

                    self.pmodls['def'+str(d)] = ln
                    d = d + 1

    def showParse(self):
        print(self.imprts,self.objcts,self.pmodls)

    def hasDesc(self):
        with open(self.pyFile,'r', encoding=u'utf-8') as f:
            txt = f.read()
        whris = re.search(r'############ Description ############',txt)
        whrhs = re.findall(r'^#{12,}.Desc.*#{12,}\n##.*.*\n##.*.*\n##.*.*\n##.*.*\n#{15,}.End.#{15,}',txt,re.MULTILINE)
        #print(whrhs,whris)
        if whris:
            return whrhs[0]


    def getGUIfil(self):
        for im in self.imprts:
            if 'Src' in im:
                return im[im.find('GUI'):].split(' ')[0]

    def checkSyntx(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris = re.search(r"if\s__name__\s==\s\'__main__\':", f.read())
            whmis = re.search(r'(.+main.+)||[main]',f.read())
            #print(whris.group().split(' '))
            if whris:
                mainis = re.search(r'def\smain',f.read())
                mainis2= re.search(r'...\smain\s\(panel.+\)\:',f.read())
                #print(u'main found:',mainis,mainis2)
            #print(whmis)
            return whris

    def checkSyntx2(self):
        '''
        A : if __name__=='__main__': stetement
        B : def main(panel=None): statement
        C : class telframe(wx.Frame): statemenr
        D : class MyPanel1(wx.Panel): statement
        :return: A,B,C,D
        '''
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            txt = f.read()
        whris = re.findall(r"if\s__name__\s?==\s?\'__main__\'\s?:", txt)
        #print('if __name__',whris)
        A = len(whris)
        mainis2 = re.findall(r'def\smain\(panel.+\)\:|def\smain\s?\(\s?panel.+\)\:', txt)
        #print('main(panel=None)', mainis2)
        B = len(mainis2)
        whfis = re.findall(r'class\s.+\(\s?wx\.Frame.+:',txt)
        #print('wx.Frame',whfis)
        C = len(whfis)

        panlis = re.findall(r'class\sMyPanel1\s?\(\s?wx\.Panel.+:',txt)
        #print('class wx.Panel',panlis)
        D = len(panlis)
        #     return False
        return A,B,C,D


    def ishasmain(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris = re.search(r'def\smain', f.read())
            if whris:
                #print(whris.group().split(' '))
                return whris.group().split(' ')[1]

    def ishasifin(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            #whris = re.search(r"if\s__name__", f.read())
            whris = re.search(r"if\s__name__\s?==\s?\'__main__\'\s?:", f.read())
            if whris:
                #print(whris.group().split(' '))
                return whris.group().split(' ')[1]

    def ishasframe(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris = re.search(r'class\s.*\s?(\s?wx\.Frame\s?).+', f.read())
            if whris:
                #print(whris.group().split(' ')[1])
                return whris.group().split(' ')[1]

    def ishaspanel(self):
        with open(self.pyFile, 'r' , encoding=u'utf-8') as f:
            whris = re.search(r"class\s.*\s?(\s?wx\.Panel\s?)", f.read())
            if whris:
                #print(whris.group().split(' ')[1])
                return whris.group().split(' ')[1]

    def ishasimport(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris = re.findall(r'import\s+%s.+\s+'%txt, f.read())
            if whris :
                #print(whris)
                return whris
    def ishasfromim(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris2 = re.findall(r'from\s+%s.+\s+import\s+.+'%txt, f.read())
            if whris2:
                #print(whris2)
                return whris2

    def ismainexist(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris2 = re.findall(r'main',f.read())
            #print(whris2)
            if whris2:
                return whris2
    def iswxframeexist(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris2 = re.findall(r'wx\.Frame',f.read())
            #print(whris2)
            if whris2:
                return whris2

    def isDBimexist(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            whris2 = re.findall(r'import\s+Database\.PostGet\s+as\s+PG',f.read())
            if whris2:
                return whris2

    def isFiledbexist(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            itxt = f.read()
        whris1 = re.findall(r'\s+PG\.Get2\s?\(.*.\)',itxt)
        whris2 = re.findall(r'\s+PG\.Post2\s?\(.*.\)',itxt)

        if whris1 or whris2:
            return whris1,whris2

    def findDBintxt(self, txt):
        whris1 = re.findall(r'\'.*.\\Src\\DBF\\.*.\'', txt)
        if whris1:
            dbfile = whris1[0].replace("'",'').replace(',','')
            #print(dbfile)
            return dbfile
        else:
            whris1 = re.findall(r'\(\'.*.\',',txt)
            #print(whris1)
            if whris1:
                dbfile = whris1[0].replace("'",'').replace(',','').replace('(','')
                #print(dbfile)
                return dbfile

    def indexImpline(self):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            itxt = f.readlines()
        i = 0
        imprtlist = []
        for t in itxt:
            i += 1
            if 'import' in t:
                imprtlist.append((t,i))
        return imprtlist

    def hasMLAimpis(self, txt=''):
        with open(self.pyFile, 'r', encoding=u'utf-8') as f:
            itxt = f.readlines()
        whris1 = whris2 = []

        for linn in itxt:
            if linn[:6] == 'import':
                #print(re.findall('Src\.MLA\..*.', linn),linn)
                if re.findall('Src\.MLA\..*.', linn):
                    whris1.append(linn)

            if linn[:4] == 'from':
                #print(re.findall('Src\.MLA\..*.', linn), linn)
                if re.findall('Src\.MLA\..*.', linn):
                    whris2.append(linn)

        #whris1 = re.search(r'^[import]\s+Src\.MLA\..*.',itxt)
        #whris1 = re.match(r'import\s+Src\.MLA\..*.', itxt)
        #whris2 = re.search(r'^[from]\s+Src\.MLA\..*.',itxt)
        #print(whris2,whris1)
        if whris1 or whris2:
            return whris1,whris2

def GetPanelImport(filewopy):
    f = filewopy+'.py'

def AnalizdbText(dbdatatxt):
    Table_feild_dict = {}
    Index_List = []
    wtxt1 = re.sub(r'[\(\n\)]','',dbdatatxt)
    #print(wtxt1)
    wtxt = re.sub(r'\s+',' ',wtxt1)
    #print(wtxt)
    ltxt = wtxt.split(' ')
    #print(ltxt)
    Table_name = ltxt[ltxt.index('TABLE') + 1]

    t = dbdatatxt
    fld = t[t.find('(')+1:t.find(')')]
    t1 = re.sub(r'\s+',' ',fld)
    #print(t1.replace('\n','').split(','))
    t2 = t1.replace('\n','').split(',')
    #print(t2)
    ifilds = []
    for fll in t2:
        #Table_feild_dict[Table_name]=(fll.split(' ')[0],fll.split(' ')[1])
        ifilds.append(fll)
    Table_feild_dict[Table_name] = ifilds
    return Table_feild_dict

def AnalizdbText2(dbtext):
    Table_list = {}
    Index_list = {}
    for txt in dbtext:
        if txt[0] == 'table':
            f = txt[4][txt[4].index('(')+1:txt[4].index(')',-1)]
            #print(re.sub(r'\s+', ' ', f))
            sbf = re.sub(r'\s+', ' ', f)
            fields = []
            #print(sbf.split(','))
            for sfld in sbf.split(','):
                #print(sfld.strip(' ')[:7])
                if sfld.strip(' ')[:7] == 'PRIMARY' or ')' in sfld.strip(' ').split(' ')[0]:
                    print(sfld)
                else:
                    fields.append(sfld)
            #fields = re.split(',',re.sub('\s+',' ',f))
            #print(fields)
            lstfld = []
            for fl in fields:
                ssfl = ''
                ssfl = fl.strip(' ').split(' ')
                #print(ssfl)
                if len(ssfl) > 0:
                    namfld = ssfl[0]
                    if len(ssfl) > 1:
                        typfld = ssfl[1]
                        if len(ssfl) > 2:
                            stgfld = ssfl[2:]
                        else:
                            stgfld = []
                    else:
                        typfld = "TEXT"
                #print(namfld,typfld,stgfld)
                lstfld.append((namfld,typfld,stgfld))
            Table_list[txt[1]] = lstfld

        if txt[0] == 'index':
            #Index_list[txt[1]]
            pass
    return Table_list,Index_list