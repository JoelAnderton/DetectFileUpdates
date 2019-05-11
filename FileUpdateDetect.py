######################################################################################################################
# Created by: Joel Anderton
# Created date: 4/11/2019
#
# Purpose: To detect all file updates or additions in a given folder and its subfolders compared to the last time
#          the program was run
#
#   1. Run an initial scan of folder and all its subfolders and files
#   2. Save that information in a list
#   3. Run the program again and compare its current state to the state saved in the list
#
######################################################################################################################
import os
import datetime
import time
import shutil

# find all files and files in subfolders: their names and last modified date/time

folder_path = r'/Users/joelanderton/Desktop/Here'
file_list = []
file_dic = {}

for root, dirs, files in os.walk(folder_path):
    for file in files:
        print(file)
        print(os.path.join(root, file))
        mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))

        file_dic = {file: mod_time}
        file_list.append(file_dic)
        print(file_list)

# save the state of the folder in a text file
with open('file_info.txt', 'w') as text:

    for file_time in file_list:
        for k, v in file_time.items():
            text.writelines(k + v + '\n')


# compare the text file to the folder's current state
