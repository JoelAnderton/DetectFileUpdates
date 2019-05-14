######################################################################################################################
# Created by: Joel Anderton
# Created date: 4/11/2019
#
# Purpose: To detect all file updates or additions in a given folder and its subfolders compared to the last time
#          the program was run
#
#   1. Run an initial scan of folder and all its subfolders and files
#   2. Save that information
#   3. Run the program again and compare its current state to the state saved
#
######################################################################################################################
import os
import time
import datetime
import pickle
import re


# find all files and files in subfolders: their names and last modified date/time
def find_files(folder_path, initial):
    #folder_path = r'/Users/joelanderton/Desktop/Here'
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if initial == 1:
                print('\rGathering files to monitor: ' + file_path, end='')
            mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))
            file_dic = {file_path: mod_time}
            file_list.append(file_dic)
    print()
    return file_list


# save the state of the folder
def save_history(file_list, folder):
    with open(folder + '.pkl', 'wb') as f:
        pickle.dump(file_list, f)


# compare the filenames that may have been added or deleted/moved
def compare_filenames(file_list_old, folder_path, folder, initial):

    
           
    # find file differences:
    file_list_current = find_files(folder_path, initial)

    # extract dictionary keys into a set for old files
    old_files = []
    for old_file in file_list_old:
        for key, value in old_file.items():
            old_files.append(key)
    old_files_set = set(old_files)
    #print(old_files_set)

    # extract dictionary keys into a set for current files
    cur_files = []
    for cur_file in file_list_current:
        for key, value in cur_file.items():
            cur_files.append(key)
    cur_files_set = set(cur_files)
    #print(cur_files_set)

    # compare the sets
    diff_set1 = old_files_set.difference(cur_files_set)
    diff_list1 = list(diff_set1)
    diff_set2 = cur_files_set.difference(old_files_set)
    diff_list2 = list(diff_set2)

    if diff_list1 != []:
        print('\n' + '########  DELETED/MOVED files  #########')
        with open(folder + '_log.txt', 'a+') as log:
             log.writelines('\n' + '########  DELETED/MOVED files  ######### -- runtime --' + str(datetime.datetime.now()) + '\n') 
        for path in list(diff_list1):
            print(path)
            with open(folder + '_log.txt', 'a+') as log:
                log.writelines(path + '\n')

    if diff_list2 != []:
        print('\n' + '##########  NEW files  ########### -- ' + str(datetime.datetime.now()))
        with open(folder + '_log.txt', 'a+') as log:
             log.writelines('\n' + '##########  NEW files  ########### -- runtime --' + str(datetime.datetime.now()) + '\n') 
        for path in list(diff_list2):
            print(path)
            with open(folder + '_log.txt', 'a+') as log:
                log.writelines(path + '\n')
    else:
        with open(folder + '_log.txt', 'a+') as log:
            log.writelines('\n' + '######## NEW/DELETED/MOVED files  ######### -- runtime --' + str(datetime.datetime.now()) + '\n') 
            log.writelines('No files were added or removed' + '\n')
        print('\n' + '########  NEW/DELETED/MOVED files  ######### -- runtime --' +  str(datetime.datetime.now()) + '\n')
        print('No files were added or removed \n')


def compare_mod_date(file_list_old, folder_path, folder, initial):

    with open(folder + '_log.txt', 'a+') as log:
          log.writelines('\n' + '########  UPDATED Files  ######### -- runtime --' + str(datetime.datetime.now())  + '\n') 
    print('########  UPDATED Files  ######### -- runtime --' + str(datetime.datetime.now()))
    file_list_current = find_files(folder_path, initial)

    # extract dictionary keys into a set for old files
    flag_mod_date_happend = 0

    for old_file in file_list_old:
        for cur_file in file_list_current:
            for old_key, old_value in old_file.items():
                for cur_key, cur_value in cur_file.items():
                    if old_key == cur_key and old_value != cur_value:
                        flag_mod_date_happend = 1
                        print(cur_key + ' -- Last Modified Date: ' + cur_value)
                        with open(folder +'_log.txt', 'a+') as log:
                            log.writelines(cur_key + ' -- Last Modified Date: ' + cur_value + '\n')

    if flag_mod_date_happend == 0:
        with open(folder +'_log.txt', 'a+') as log:
             log.writelines('No files were modified' + '\n')
        print('No files were modified')

def main():
    # check if folder history file exists
    folder_path  = input('Drag/drop folder to monitor changes: ')
    folder = re.split(r'\\', folder_path)
    folder = folder[-1:][0]
    try:
        with open( folder +'.pkl', 'rb') as fh:
            initial = 0
            file_list = pickle.load(fh)
            compare_filenames(file_list, folder_path, folder, initial)
            compare_mod_date(file_list, folder_path, folder, initial)
            file_list = find_files(folder_path, initial)
            save_history(file_list, folder)

    except FileNotFoundError:
        initial = 1
        print('Initialized monitoring')
        file_list = find_files(folder_path, initial)
        save_history(file_list, folder)


if __name__ == '__main__':
    main()

