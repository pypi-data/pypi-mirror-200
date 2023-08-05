#In The name of God
#!/usr/bin/env python
# -*- codnig: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table,Column,Integer,String,Text

from Config.Init import *

class Get:
	def __init__(self, DBF, engine,**kwargs):
		'''

		:param DBF: Database-name
		:param engine: ['sqlite','mysql','postgresql','oracle','sqlserver']
		:param kwargs: user  password  host
		'''
		if len(kwargs) == 3:
			self.user = kwargs['user']
			self.pswrd = kwargs['password']
			self.host = kwargs['host']

		self.DBF = DBF

		if engine == 'sqlite':
			self.myengin = create_engine('sqlite:///'+self.DBF, echo=False)
		if engine == 'postgresql':
			self.myengin = create_engine('postgresql://'+self.user+':'+self.pswrd+'@'+self.host+'/'+self.DBF)
			# psycopg2
			#self.myengin = create_engine('postgresql+psycopg2://scott:tiger@localhost/'+self.DBF)
			# pg8000
			#self.myengin = create_engine('postgresql+pg8000://scott:tiger@localhost/'+self.DBF)
		if engine == 'mysql':
			self.myengin = create_engine('mysql://'+self.user+':'+self.pswrd+'@'+self.host+'/'+self.DBF)
			# mysqlclient (a maintained fork of MySQL-Python)
			#self.myengin = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
			# PyMySQL
			#self.myengin = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
		if engine == 'oracle':
			self.myengin = create_engine('oracle://'+self.user+':'+self.pswrd+'@'+self.host+':1521/'+self.DBF)
			# self.myengin = create_engine('oracle+cx_oracle://scott:tiger@tnsname')
		if engine == 'sqlserver':
			self.myengin = create_engine('mssql+pymssql://'+self.user+':'+self.pswrd+'@'+self.host+':1521/'+self.DBF)
			#self.myengin = create_engine('mssql+pyodbc://scott:tiger@mydsn')

		meta = MetaData()


	def openSQL(self, sqlfile):
		with open(sqlfile) as f:
			self.alltext = f.readlines()
		return  self.alltext

	def GetFromSql(self):
		with self.myengin.connect() as conn :
			session = sessionmaker()
			result = conn.execute(self.alltext[0])
			conn.close()
			#conn.commit()
		return result

	def GetFromString(self, sqlstring):
		with self.myengin.connect() as conn:
			result = conn.execute(sqlstring)
			return result.fetchall()





class Post:
	def __init__(self, DBF, table, Data, engine, **kwargs):
		'''

		:param DBF:
		:param Table:
		:param Data:
		:param engine:
		:param kwargs: user  pswrd  host
		'''
		if len(kwargs) == 3:
			self.user = kwargs['user']
			self.pswrd = kwargs['password']
			self.host = kwargs['host']
		self.DBF = DBF
		self.Data = Data
		self.table = table
		self.metadata = MetaData()


		if engine == 'sqlite':
			self.myengin = create_engine('sqlite:///'+self.DBF, echo=False)
		if engine == 'postgresql':
			self.myengin = create_engine('postgresql://'+self.user+':'+self.pswrd+'@'+self.host+'/'+self.DBF)
		if engine == 'mysql':
			self.myengin = create_engine('mysql://'+self.user+':'+self.pswrd+'@'+self.host+'/'+self.DBF)
		if engine == 'oracle':
			self.myengin = create_engine('oracle://'+self.user+':'+self.pswrd+'@'+self.host+':1521/'+self.DBF)
		if engine == 'sqlserver':
			self.myengin = create_engine('mssql+pymssql://'+self.user+':'+self.pswrd+'@'+self.host+':1521/'+self.DBF)

	def Addrecord(self,Filed,Data):
		thstbl = Table(self.table,self.metadata,autoload=True,autoload_with=self.myengin)
		with self.myengin.connect() as conn:
			ins = thstbl.insert()
			#print(str(ins))
			ins = thstbl.insert().values(Data)
			result = conn.execute(ins)

	def Updaterecord(self,Field,Data):
		pass

	def Deleterecord(self,Data):
		pass