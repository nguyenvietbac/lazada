# -*- coding: utf-8 -*-
import pypyodbc
import pyodbc
import json
import pymongo
#####################################################
# print("fool")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Price"]
names = mydb.collection_names()
# mycol = mydb["data_2018-10-21"]

with open('ada.json') as f:
	file_data = json.load(f)

if "data_"+file_data[1]["time"] not in names:
	print("new data found, creating new access file")

	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Administrator\Documents\share_folder\all_crawl1\temp.accdb;')
	cursor = conn.cursor()
	cursor2 = conn.cursor()
	for table in cursor.tables():
		if table.table_type == "TABLE":
			drop = "DROP TABLE [{0}]".format(table.table_name)
			# print drop
			cursor2.execute(drop)
	conn.commit()
	conn.close()

	#####################################################
	dbname = r'C:\Users\Administrator\Documents\share_folder\all_crawl1\temp.accdb'     
	constr = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={0};".format(dbname)

	dbconn = pypyodbc.connect(constr)
	cur = dbconn.cursor()

	cur.execute("""CREATE TABLE data (
					 ID autoincrement,
					 name varchar(100),
					 price varchar(50),
					 source varchar(50),
					 "time" varchar(50),
					 properties varchar(50));""")
	dbconn.commit()
	dbconn.close()

	####################################################

	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Administrator\Documents\share_folder\all_crawl1\temp.accdb;')
	cursor = conn.cursor()

	# with open('vuivui.json') as f:
	# 	file_data = json.load(f)
	# for x in file_data:
	# 	temp_str = x["properties"][0]
	# 	for y in range(1, len(x["properties"])):
	# 		temp_str = (temp_str) + ", " + (x["properties"][y]) 
	# 	# print(temp_str)
	# 	na = [x["name"], x["price"], x["source"], x["time"], temp_str]
	# 	ind_data = ('''
	# 					INSERT INTO data (name, price, source, "time", properties)
	# 					VALUES(?, ?, ?, ?, ?)

	# 			   ''')

	# 	cursor.execute(ind_data, na)

	# with open('test.json') as f:
	# 	file_data = json.load(f)
	# for x in file_data:
	# 	temp_str = x["properties"][0]
	# 	for y in range(1, len(x["properties"])):
	# 		temp_str = (temp_str) + ", " + (x["properties"][y]) 
	# 	# print(temp_str)
	# 	na = [x["name"], x["price"], x["source"], x["time"], temp_str]
	# 	ind_data = ('''
	# 					INSERT INTO data (name, price, source, "time", properties)
	# 					VALUES(?, ?, ?, ?, ?)

	# 			   ''')

	# 	cursor.execute(ind_data, na)

	with open('tiki.json') as f:
		file_data = json.load(f)
	for x in file_data:
		temp_str = x["properties"][0]
		for y in range(1, len(x["properties"])):
			temp_str = (temp_str) + ", " + (x["properties"][y]) 
		# print(temp_str)
		na = [x["name"], x["price"], x["source"], x["time"], temp_str]
		ind_data = ('''
						INSERT INTO data (name, price, source, "time", properties)
						VALUES(?, ?, ?, ?, ?)

				   ''')

		cursor.execute(ind_data, na)

	with open('ada.json') as f:
		file_data = json.load(f)
	for x in file_data:
		temp_str = x["properties"][0]
		for y in range(1, len(x["properties"])):
			temp_str = (temp_str) + ", " + (x["properties"][y]) 
		# print(temp_str)
		na = [x["name"], x["price"], x["source"], x["time"], temp_str]
		ind_data = ('''
						INSERT INTO data (name, price, source, "time", properties)
						VALUES(?, ?, ?, ?, ?)

				   ''')

		cursor.execute(ind_data, na)


	with open('laz.json') as f:
		file_data = json.load(f)
	for x in file_data:
		temp_str = x["properties"][0]
		for y in range(1, len(x["properties"])):
			temp_str = (temp_str) + ", " + (x["properties"][y]) 
		# print(temp_str)
		na = [x["name"], x["price"], x["source"], x["time"], temp_str]
		ind_data = ('''
						INSERT INTO data (name, price, source, "time", properties)
						VALUES(?, ?, ?, ?, ?)

				   ''')

		cursor.execute(ind_data, na)
	conn.commit()
	conn.close()
else:
	print("data_exist")