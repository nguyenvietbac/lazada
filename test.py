# -*- coding: utf-8 -*-
import os
import json
import pymongo
import datetime
import time
start = time.time()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Price"]
names = mydb.collection_names()
# mycol = mydb["data_2018-10-21"]

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

if "data_"+"pycode1" not in names:
	print("new data found, creating new collection")
	# temp = file_data[1]["time"] 
	# temp.replace("-","_")
	# mycol = mydb["data_"+"pycode1"]
	# mycol.insert(file_data)

	if os.stat("laz.json").st_size != 0 :
		with open('laz.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		# im_data = []
		count = 0
		send_data = []
		while file_data != []:
			temp = file_data[0]
			send_data.append(temp)
			count += 1
			
			del file_data[0]
			ls_del = []
			for x in range(int(len(file_data)*1/3), len(file_data)):
				if temp["name"] == file_data[x]["name"] and temp["price"] == file_data[x]["price"]:
					ls_del.append(x)

			for x in list(reversed(ls_del)):
				del file_data[x]
			print(str(count)+ "  " + str(len(ls_del)) + "  " + str(len(file_data)))
		# mycol.insert(send_data)

	if os.stat("tiki.json").st_size != 0 :
		with open('tiki.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		# mycol.insert(file_data)
		count = 0
		send_data = []
		while file_data != []:
			temp = file_data[0]
			send_data.append(temp)
			count += 1
			
			del file_data[0]
			ls_del = []
			for x in range(0, len(file_data)):
				if temp["name"] == file_data[x]["name"] and temp["price"] == file_data[x]["price"]:
					ls_del.append(x)
			# print(str(count)+ "  " + str(len(ls_del)))
			for x in list(reversed(ls_del)):
				del file_data[x]
			print(str(count)+ "  " + str(len(ls_del)) + "  " + str(len(file_data)))
		# mycol.insert(send_data)

	if os.stat("ada.json").st_size != 0 :
		with open('ada.json', encoding="utf-8") as f:
		    file_data = json.load(f)
		# mycol.insert(file_data)
		count = 0
		send_data = []
		while file_data != []:
			temp = file_data[0]
			send_data.append(temp)
			count += 1
			
			del file_data[0]
			ls_del = []
			for x in range(0, len(file_data)):
				if temp["name"] == file_data[x]["name"] and temp["price"] == file_data[x]["price"]:
					ls_del.append(x)
			# print(str(count)+ "  " + str(len(ls_del)))
			for x in list(reversed(ls_del)):
				del file_data[x]
			print(str(count)+ "  " + str(len(ls_del)) + "  " + str(len(file_data)))
		# mycol.insert(send_data)

	myclient.close()
else:
	print("data_exist")


end = time.time()
print(end - start)