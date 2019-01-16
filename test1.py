import datetime

date = datetime.datetime.now()
date = str(date)

print(date)

file = open("test.json", "w")
file.write(date)