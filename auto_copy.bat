ECHO startcopy

SET da=data_%date:~10,4%_%date:~4,2%_%date:~7,2%

copy /Y C:\Users\Administrator\Documents\share_folder\all_crawl1\temp.accdb D:\06_Database_Management\Crawling_Prices\%da%.accdb
