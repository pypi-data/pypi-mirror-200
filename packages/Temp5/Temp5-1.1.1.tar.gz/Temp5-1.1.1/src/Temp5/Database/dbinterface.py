#In the name og GOD
# ! use/bin/env python
#This file for connect to database interface

'''
   General Purpose Database Systems
    *MySQL
    *Oracle
    *PostgreSQL
    *Microsoft SQL Server
    *Microsoft Access

    for Sqlite        import sqlite3
    for Mysql         import mysql.connector
    for PostgerSQL    import psycopg2
    for Oracle        import cx_Oracle
    for MS SQL Server import pymssql
    for MS Access     import pyodbc

    for MongoDB       import pymongo
'''

def ForSqlitDb(database):
	'''

	:param database:
	:return: Connection
	'''
	import sqlite3
	mydb = sqlite3.connect(database)
	mydb.row_factory = sqlite3.Row
	return mydb

def ForMySqldb(database,user,pswrd,host="localhost"):
	'''

	:param database:
	:param user:
	:param pswrd:
	:param host: localhost
	:return: Connector
	'''
	import mysql.connector

	config = {
		"host": host,
		"port": 3306,
		"database": database,
		"user": user,
		"password": pswrd,
		"charset": "utf8",
		"use_unicode": True,
		"get_warnings": True,
	}

	mydb = mysql.connector.Connect(**config)
	# mydb = mysql.connector.connect(
	# 	host=host,
	# 	user=user,
	# 	password=pswrd,
	# 	database=database
	# )

	return mydb

def ForPostgrSql(database,user,pswrd,host="localhost",port="5432"):
	'''

	:param database:
	:param user:
	:param pswrd:
	:param host: localhost
	:param port: default=5432
	:return: Connection
	'''
	import psycopg2
	#print(database,user,pswrd,host,port)
	mydb = psycopg2.connect(database=database, user=user, password=pswrd, host=host, port=port)

	return  mydb

def ForOraclSqldb(database,user,userpwd,host="localhost",port='1521'):
	'''

	:param database:
	:param user:
	:param userpwd:
	:param host: localhost
	:param port: 1521
	:return: Connection
	'''
	import cx_Oracle
	'''
	# Create a table in Oracle database
	try:
		con = cx_Oracle.connect('tiger/scott@localhost:1521/xe')
		print(con.version)
		:return con
	except cx_Oracle.DatabaseError as e:
		print("There is a problem with Oracle", e)
	# by writing finally if any error occurs
	# then also we can close the all database operation
	finally:
		if con:
			con.close()
    '''

	# Establish the database connection

	#mydb = cx_Oracle.connect(user=user, password=userpwd,dsn=host+'/'+database)
	with cx_Oracle.connect(user=user, password=userpwd,dsn=host+':'+str(port)+'/'+database) as mydb:

		return mydb
	#return mydb
'''


	with cx_Oracle.connect(user=user, password=password,
	                       dsn="dbhost.example.com/orclpdb1",
	                       encoding="UTF-8") as connection:
		cursor = connection.cursor()
		cursor.execute("insert into SomeTable values (:1, :2)",
		               (1, "Some string"))
		connection.commit()
'''

def ForMsSqlOdbc(database,user,pswrd,host='localhost\sqlexpress'):
	import pyodbc
	# Some other example server values are
	# server = 'localhost\sqlexpress' # for a named instance
	# server = 'myserver,port' # to specify an alternate port
	server = host
	database = database
	username = user
	password = pswrd
	cnxn = pyodbc.connect(
		'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

	return cnxn

def ForMsSqlSrv(database,user,pswrd,host='localhost\sqlexpress'):
	import pymssql
	mydb = pymssql.connect(server=host, user=user,
	                       password=pswrd, database=database)
	return mydb




def ForMongoDb(database,host="mongodb://localhost:27017/"):
	import pymongo
	myclient = pymongo.MongoClient(host)
	mydb = myclient[database]
	return mydb
	# mycol = mydb["customers"]
	# mydict = {"name": "John", "address": "Highway 37"}
	# x = mycol.insert_one(mydict)
	# mylist = [
	# 	{"name": "Amy", "address": "Apple st 652"},
	# 	{"name": "Hannah", "address": "Mountain 21"},
	# 	{"name": "Michael", "address": "Valley 345"},
	# 	{"name": "Sandy", "address": "Ocean blvd 2"},
	# 	{"name": "Betty", "address": "Green Grass 1"},
	# 	{"name": "Richard", "address": "Sky st 331"},
	# 	{"name": "Susan", "address": "One way 98"},
	# 	{"name": "Vicky", "address": "Yellow Garden 2"},
	# 	{"name": "Ben", "address": "Park Lane 38"},
	# 	{"name": "William", "address": "Central st 954"},
	# 	{"name": "Chuck", "address": "Main Road 989"},
	# 	{"name": "Viola", "address": "Sideway 1633"}
	# ]
	#
	# x = mycol.insert_many(mylist)
	# x = mycol.find_one()
	# myquery = {"address": "Park Lane 38"}
	# mydoc = mycol.find(myquery)
	# mydoc = mycol.find().sort("name")