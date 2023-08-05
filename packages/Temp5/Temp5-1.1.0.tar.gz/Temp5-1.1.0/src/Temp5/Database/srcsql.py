# In the name of God
# ! use/bin/env python

import os
import sqlite3

import wx

from Config.Init import *
from wx import MessageBox, OK, ICON_WARNING

from .dbinterface import  *

class SFDB(object):
	def __init__(self, database=':memory:',**kwargs):
		'''

		:param database:
		:param dbpath:
		:param kwargs: user pswrd host
		'''
		self.kwarg = kwargs
		self.database = database
		self.infacecon = self.Getinterface(**kwargs)
		self.connect()

	def Getinterface(self,**kwargs):
		'''

		:param kwargs: user, pswrd, host
		:return: interface connection to database
		'''
		#print(kwargs,self.kwarg)
		self.config = wx.GetApp().GetConfig()
		infaceid = self.config.Read('DBtype')
		myinface = Database_type[int(infaceid)]
		if myinface == 'sqlite':
			return ForSqlitDb(self.database)
		if myinface == 'mysql':
			return ForMySqldb(self.database,kwargs['user'],kwargs['pswrd'],kwargs['host'])
		if myinface == 'postgresql':
			return ForPostgrSql(self.database,kwargs['user'],kwargs['pswrd'],kwargs['host'])
		if myinface == 'oracle':
			return ForOraclSqldb(self.database,kwargs['user'],kwargs['pswrd'],kwargs['host'])
		if myinface == 'sqlserver':
			return ForMsSqlSrv(self.database,kwargs['user'],kwargs['pswrd'],kwargs['host'])


	def connect(self):
		# print self.database
		try:
			self.connection = self.infacecon #.connect(self.database)
			self.cursor = self.connection.cursor()
		except:
			# print( 'No Database find')
			MessageBox(u'No Database find', u'Error', OK | ICON_WARNING)

		self.connected = True
		self.statement = ''
		return self.connection

	def close(self):
		self.commit()
		self.connection.close()
		self.connected = False

	def commit(self):
		return self.connection.commit()

	def execute(self, statments):
		# with self.connect():
		self.cursor.execute(statments)
		#return self.fetchall()

	def execute1(self, statments, *data):
		if len(data) > 0:
			self.cursor.execute(statments, data[0])
		#self.commit()
		#return self.fetchall()

	def execone(self, statments, *data):
		if data == None:
			self.cursor.execute(statments)
		else:
			self.cursor.execute(statments, data[0])
		#return self.fetchone()

	def executemany(self, statments, *data):
		if data == None:
			return self.cursor.executemany(statments)
		else:
			return self.cursor.executemany(statments, data[0])

	def execuetscript(self, statments):
		return self.cursor.executescript(statments)

	def total_changes(self):
		pass

	def rollback(self):
		return self.cursor.rollback()

	def fetchone(self):
		return self.cursor.fetchone()

	def fetchall(self):
		return self.cursor.fetchall()

	def fetchmany(self, size):
		return self.cursor.fetchmany()

class SQLite(object):
	def __init__(self, tables, fields, values):
		self.tables = tables
		self.fields = fields
		self.values = values

	def create(self, **karg):
		sql = 'create table {t} ({f} {p})'.format(t=str(self.tables), f=str(self.fields), p=str(self.values))
		return sql

	def insert(self, **karg):
		sql = 'insert into ' + str(self.tables)
		sql = sql + '(' + str(self.fields) + ')'

		sql = sql + ' values ' + '(' + '?,' * (len(self.fields.split(',')) - 1) + '?)'
		# print sql
		return sql

	def select(self, *arg, **karg):
		sql = ' select ' + self.fields + ' from ' + self.tables
		# print sql
		return sql

	def select1(self, *arg, **karg):
		sql = ' select distinct' + self.fields + ' from ' + self.tables + ' where ' + self.values
		# print sql
		return sql

	def update(self, **karg):
		sql = ' update ' + self.tables + ' set ' + self.fields
		# print sql
		return sql

	def update2(self, **karg):
		sql = ' update ' + self.tables + ' set ' + self.fields + ' where ' + self.values
		return sql

	def delete(self, **karg):
		sql = ' delete from ' + self.tables + ' where ' + self.values
		return sql

	def delall(self, **karg):
		# sql = ' delete from '+self.tables+' where '+self.values
		sql = " delete from {t} ".format(t=self.tables)
		return sql

class MySQLs(object):
	def __init__(self, tables, fields, values):
		self.tables = tables
		self.fields = fields
		self.values = values

	def create(self, **karg):
		sql = 'CREATE TABLE {t} ({f} {p})'.format(t=str(self.tables), f=str(self.fields), p=str(self.values))
		return sql

	def insert(self, **karg):
		sql = 'INSERT INTO ' + str(self.tables)
		sql = sql + '(' + str(self.fields) + ')'

		sql = sql + ' VALUES ' + '(' + '%s,' * (len(self.fields.split(',')) - 1) + '%s)'
		# print sql
		return sql

	def select(self, *arg, **karg):
		sql = ' SELECT ' + self.fields + ' FROM ' + self.tables
		# print sql
		return sql

	def select1(self, *arg, **karg):
		sql = ' SELECT DISTINCT' + self.fields + ' FROM ' + self.tables + ' WHERE ' + self.values
		# print sql
		return sql

	def update(self, **karg):
		sql = ' UPDATE ' + self.tables + ' SET ' + self.fields
		# print sql
		return sql

	def update2(self, **karg):
		sql = ' UPDATE ' + self.tables + ' SET ' + self.fields + ' WHERE ' + self.values
		return sql

	def delete(self, **karg):
		sql = ' DELETE FROM ' + self.tables + ' WHERE ' + self.values
		return sql

	def delall(self, **karg):
		# sql = ' delete from '+self.tables+' where '+self.values
		sql = " DELETE FROM {t} ".format(t=self.tables)
		return sql


def MyDB_Path(database):
	if chkengin() == 2 or chkengin() == 3:
		config = wx.GetApp().GetConfig()
		iusr = config.Read('DBtype.Usr')
		ipwd = config.Read('DBtype.Pwd')
		ihst = config.Read('DBtype.Hst')
		#print(uphstr.split(' '))
		return SFDB(database,user=iusr,pswrd=ipwd,host=ihst)
	else:
		return SFDB(database)

def MySrc_db_Path(database, user='',pswrd='',host=''):
	return SFDB(database,user=user,pswrd=pswrd,host=host)

def chkengin():
	config = wx.GetApp().GetConfig()
	infaceid = config.Read('DBtype')
	return int(infaceid)


def wxsqsel(database, tabels, fields='*', condition=''):

	Mydb = MyDB_Path(database)
	Mydb.connect()
	if chkengin() == 1:
		sql = SQLite(tabels, fields, condition)
		sql1 = sql.select(fields, tabels)
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, condition)
		sql1 = sql.select(fields, tabels)
	Mydb.execute(sql1)
	mylist = Mydb.fetchone()
	return mylist


def wxsqsel1(database, tabels, fields='*', condition=''):
	Mydb = MyDB_Path(database)
	Mydb.connect()
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=condition)
		sql1 = sql.select1(fields, tabels, values=condition)
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=condition)
		sql1 = sql.select1(fields, tabels, values=condition)

	# print sql1
	Mydb.execute(sql1)
	mylist = Mydb.fetchall()
	return mylist

def wxsqsel2(database, tabels, fields='*'):
	Mydb = MyDB_Path(database)
	Mydb.connect()
	# print sql1
	Mydb.execute1(tabels, fields)
	mylist = Mydb.fetchall()
	return mylist

def wxsqltxt(database, text):
	# global MAP
	Mydb = MyDB_Path(database)
	Mydb.execute(text)
	mylist = Mydb.fetchall()
	return mylist


def wxsqins(database, tabels, fields, data):
	# global MAP
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=data)
		sql1 = sql.insert()
		#print( sql1, data )
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=data)
		sql1 = sql.insert()
	mylist = Mydb.execone(sql1, data)
	Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqins2(database, tabels, fields, data):
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=data)
		sql1 = sql.insert()
	# print( sql1, data )
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=data)
		sql1 = sql.insert()
	mylist = Mydb.executemany(sql1, data)
	# Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist

def wxsqins3(database, tabels, fields, data):
	# global MAP
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=data)
		sql1 = sql.insert()
		#print( sql1, data )
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=data)
		sql1 = sql.insert()
	mylist = Mydb.execute1(sql1, data)
	Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqlup(database, tabels, fields, data):
	# global MAP
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=data)
		sql1 = sql.update()
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=data)
		sql1 = sql.update()

	# print sql
	# print sql1
	mylist = Mydb.execone(sql1, data)
	Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqlup2(database, tabels, fields, data):
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields, values=data)
		sql1 = sql.update2()
	if chkengin() > 1:
		sql = MySQLs(tabels, fields, values=data)
		sql1 = sql.update2()

	mylist = Mydb.executemany(sql1, data)
	# Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqdel(database, tabels, data):
	# global MAP
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields='', values=data)
		sql1 = sql.delete()
	if chkengin() > 1:
		sql = MySQLs(tabels, fields='', values=data)
		sql1 = sql.delete()

	# print sql
	# print sql1
	mylist = Mydb.execute(sql1)
	Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqdall(database, tabels):
	Mydb = MyDB_Path(database)
	if chkengin() == 1:
		sql = SQLite(tabels, fields='', values='')
		sql1 = sql.delall()
	if chkengin() > 1:
		sql = MySQLs(tabels, fields='', values='')
		sql1 = sql.delall()
	mylist = Mydb.execute(sql1)
	# Mydb.commit()
	Mydb.close()
	# print mylist
	return mylist


def wxsqsnd(database, tabel, field1, field2, data):
	'''
	Select field1 from table where field2 = data
	'''
	# global MAP
	Mydb = MyDB_Path(database)
	mylist = Mydb.execute(
		'select ' + tabel + '.' + field1 + ' from ' + tabel + ' where ' + tabel + '.' + field2 + " = '%s' " % data)
	# print mylist
	return mylist
