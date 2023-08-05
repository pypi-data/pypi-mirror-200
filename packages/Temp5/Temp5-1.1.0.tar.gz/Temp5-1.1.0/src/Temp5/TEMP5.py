#In the name of GOD
# This file is for Start Temp5 project in new directory

import os
import sys
import shutil
import sqlite3

import Temp5.update as update


main_direct = ['AI', 'AI\\ML','Config', 'Database', 'DCC1', 'GUI', 'GUI\\Temp', 'GUI\\API', 'GUI\\AuiPanel', 'GUI\\Main',
               #'Locale', 'Locale\\en', 'Locale\\fa', 'Locale\\fr', 'Locale\\gr', 'Locale\\sp', 'Locale\\tr',
               'Logs', 'Res', 'Res\\Fonts', 'Res\\Icons', 'Res\\Icons\\Menu', 'Res\\Icons\\Toolbar',
               'Res\\Icons\\16x16', 'Res\\Icons\\32x32', 'Res\\Images', 'Res\\Pics', 'Res\\Splash',
               'Src', 'Src\\API', 'Src\\AUI', 'Src\\DBF', 'Src\\DBF\\sqls', 'Src\\GUI', 'Src\\MLA', 'Src\\MLP', 'Src\\PRG',
               'Temps', 'Utility', 'Utility\\Fount', 'Utility\\Fount\\GUI', 'Utility\\Fount\\MLA', 'Utility\\Fount\\MLP',
               'Utility\\Fount\\AUI', 'Utility\\Fount\\PRG', 'Utility\\Fount\\API', 'Utility\\UpdateApp',
               'Utility\\Free','Utility\\Account','Utility\\Uploads','Utility\\Downloads'
               ]

local_direct = ['Locale', 'Locale\\en', 'Locale\\fa', 'Locale\\fr', 'Locale\\gr', 'Locale\\sp', 'Locale\\tr']

main_file = {
	'AI': ['OpnSrc.py', 'Generats.py', 'DBgen.py', 'Analiz.py'],
	'AI\\ML':['ConMatrix.py','SLPanel.py'],
    'Config': ['Init.py'],
    'Database': ['wxsq.py', 'PostGet2.py', 'PostGet.py', 'MenuSet2.py','srcsql.py','dbinterface.py'],
	'DCC1': ['Proper2.py', 'MenuDev2.py', 'DBDev2.py', 'ToolBar2.py', 'ProgDev2.py', 'MLDev2.py', 'ListPro2.py', 'AuiPan2.py'],
	'GUI': ['window2.py', 'Start.py', 'proman.py', 'MainTool.py', 'MainMenu2.py', 'BG2.py'],
	'GUI\\Temp': ['untitle.py', 'Demo.py', 'Muntitle.py'],
	'GUI\\API': ['SamPnl.py'],
	'GUI\\AuiPanel': ['tempane.py', 'PAui.py'],
	'GUI\\Main': ['TPv1.py', 'TBv1.py', 'PPv1.py', 'PGv1.py', 'PAv1.py', 'MLv1.py', 'MDv1.py', 'DBv1.py'],
	'Res': ['Allicons.py'],
}

creat_file = {
	'Config': ['MLmethod.ini', 'option.ini', 'system1.ini'],
	'Database': ['Menu2.db'],
	'..': ['Mainpro.py','update.py','requirements.txt','Allimp.py']
}

def create_this(file,source,target):
	if file == 'Menu2.db':
		print('.',end='')
		connection = sqlite3.connect(target+file)
		cursor = connection.cursor()
		with open(source+'Createmenu.sql', 'r') as f:
			cursor.executescript(f.read())
		connection.commit()
		connection.close()
	else:
		print('.', end='')
		shutil.copyfile(source + file, target + file)



def generate_path(mydir):
	if not os.path.isdir(mydir):
		print('.', end='')
		os.mkdir(mydir)

	os.chdir(mydir)

	for dir in main_direct:
		if not os.path.isdir(dir):
			os.mkdir(dir)
			print('.', end='')
			if not os.path.isfile(mydir+dir+'\\'+'__init__.py'):
				with open(mydir +dir+'\\'+'__init__.py','w') as f:
					f.write('')
					print('.', end='')

	for dir in local_direct:
		if not os.path.isdir(dir):
			os.mkdir(dir)
			print('.', end='')

	for dir in main_file:
		for fil in main_file[dir]:
			if not os.path.isfile(mydir+dir+'\\'+fil):
				with open(mydir+dir+'\\'+fil,'w') as f:
					f.write('')
					print('.', end='')

	for Dir in creat_file:
	   for file in creat_file[Dir]:
		   if Dir != '..':
			   if not os.path.isfile(mydir+Dir+'\\'+file):
				   with open(mydir+Dir+'\\'+file,'w') as f:
					   f.write('')
					   print('.', end='')
		   else:
			   with open(mydir+ file, 'w') as f:
				   f.write('')
				   print('.', end='')

	for Dir in creat_file:
		for file in creat_file[Dir]:
			if Dir != '..':
				if os.stat(mydir+Dir+'\\'+file).st_size == 0:
					create_this(file,'..\\Fount\\',mydir+Dir+'\\')
			else:
				if os.stat(mydir+file).st_size == 0:
					create_this(file,'..\\Fount\\',mydir)



def main(argv):
	#print(argv)
	arg_help = """syntax is :{0} <option> <directory> \n 
	    Options: 
	        Create = Make a new empty project 
	        Update = Update my program platform \n
	    example: 
	        {0} Create c:\Temp5\myProject\ 
	        {0} Update c:\Temp5\myProject\  \n """.format(argv[0])

	if len(argv) < 3:
		print(arg_help)
		exit()
	else:
		if 'Create' in argv:
			if argv[2] != '' or argv[2] != None:
				mydir = argv[2]
			else:
				print(" Please set Path to create a project")
				exit()
		elif 'Update' in argv:
			if argv[2] != '' or argv[2] != None:
				mydir = argv[2]
			else:
				print(" Please set Path to create a project")
				exit()

		#print(argv[1])



	if argv[1] == 'Create':
		if mydir[-1] != '\\':
			print(arg_help)
			print('Write a correct directory format')
			exit()
		elif mydir == '':
			print(arg_help)
			print('Exit setup. you not entered correct syntax')
			exit()
		else:
			generate_path(mydir)
			update.main()
	elif argv[1] == 'Update':
		if mydir[-1] != '\\':
			print(arg_help)
			print('Write a correct directory format')
			exit()
		elif mydir == '':
			print(arg_help)
			print('Exit setup. you not entered correct syntax')
			exit()
		else:
			update.main()

	os.chdir(mydir)
	print("Please change path to %s and execute this command: \n >> python -m Mainpro \n or: \n >> python mainpro.py " %mydir)
	exit()


if __name__ == '__main__':
	main(sys.argv)