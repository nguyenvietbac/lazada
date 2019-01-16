# -*- coding: utf-8 -*-
import os
import json
import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Price"]
names = mydb.collection_names()
# mycol = mydb["data_2018-10-21"]

# if os.stat("test.json").st_size != 0 :
# 	with open('test.json', encoding="utf-8") as f:
# 		file_data = json.load(f)

if os.stat("tiki.json").st_size != 0 :
	with open('tiki.json', encoding="utf-8") as f:
		file_data = json.load(f)
elif os.stat("ada.json").st_size != 0 :
	with open('ada.json', encoding="utf-8") as f:
		file_data = json.load(f)
elif os.stat("laz.json").st_size != 0 :
	with open('laz.json', encoding="utf-8") as f:
		file_data = json.load(f)

temp = file_data[1]["time"] 
temp = temp[0:4]+"_"+temp[5:7]+"_"+temp[8:10]
# temp.replace("0","1")
print(temp)

if "data_"+temp not in names:
	print("new data found, creating new collection")
	# temp = file_data[1]["time"] 
	# temp.replace("-","_")
	mycol = mydb["data_"+ temp]
	# mycol.insert(file_data)
	# if os.stat("test.json").st_size != 0 :
	# 	with open('test.json', encoding="utf-8") as f:
	# 		file_data = json.load(f)

	if os.stat("ada.json").st_size != 0 :
		with open('ada.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		mycol.insert(file_data)

	if os.stat("tiki.json").st_size != 0 :
		with open('tiki.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		mycol.insert(file_data)

	if os.stat("laz.json").st_size != 0 :
		with open('laz.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		mycol.insert(file_data)
	myclient.close()
else:
	print("data_exist")