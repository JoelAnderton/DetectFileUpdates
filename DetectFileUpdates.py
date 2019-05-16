######################################################################################################################
# Created by: Joel Anderton
# Created date: 5/11/2019
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
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if initial == 1:
                display_file_name = re.split(r'\\', file_path)
                display_file_name = display_file_name[-1:][0]
                print('\rGathering files to monitor: ' + display_file_name, end='')
               
            try:
                mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))            
            except:
                mod_time = time.ctime(os.path.getmtime(os.path.join(u'\\\\?\\' + root, file))) # u'\\\\?\\' for file paths greater than 255 characters

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
    file_list_current = find_files(folder_path, initial)

    # extract dictionary keys into a set for old files
    old_files = []
    for old_file in file_list_old:
        for key, value in old_file.items():
            old_files.append(key)
    old_files_set = set(old_files)

    # extract dictionary keys into a set for current files
    cur_files = []
    for cur_file in file_list_current:
        for key, value in cur_file.items():
            cur_files.append(key)
    cur_files_set = set(cur_files)

    # compare the sets
    diff_set1 = old_files_set.difference(cur_files_set)
    diff_list1 = list(diff_set1)
    diff_set2 = cur_files_set.difference(old_files_set)
    diff_list2 = list(diff_set2)

    # find files that were deleted or moved
    if diff_list1 != []:
        print('\n' + '########  DELETED/MOVED files  ######### -- runtime -- ' + str(datetime.datetime.now()))
        with open(folder + '_log.txt', 'a+') as log:
             log.writelines('\n' + '########  DELETED/MOVED files  ######### -- runtime --' + str(datetime.datetime.now()) + '\n') 
        for path in list(diff_list1):
            print(path)
            with open(folder + '_log.txt', 'a+') as log:
                log.writelines(path + '\n')

    # find new files
    if diff_list2 != []:
        print('\n' + '##########  NEW files  ########### -- runtime -- ' + str(datetime.datetime.now()))
        with open(folder + '_log.txt', 'a+') as log:
             log.writelines('\n' + '##########  NEW files  ########### -- runtime --' + str(datetime.datetime.now()) + '\n') 
        for path in list(diff_list2):
            print(path)
            with open(folder + '_log.txt', 'a+') as log:
                log.writelines(path + '\n')

    # if no new or deleted/moved files
    else:
        with open(folder + '_log.txt', 'a+') as log:
            log.writelines('\n' + '######## NEW/DELETED/MOVED files  ######### -- runtime --' + str(datetime.datetime.now()) + '\n') 
            log.writelines('No files were added or removed' + '\n')
        print('\n' + '########  NEW/DELETED/MOVED files  ######### -- runtime --' +  str(datetime.datetime.now()) + '\n')
        print('No files were added or removed \n')


def compare_mod_date(file_list_old, folder_path, folder, initial):
    # open the saved history for the folder
    with open(folder + '_log.txt', 'a+') as log:
          log.writelines('\n' + '########  UPDATED Files  ######### -- runtime --' + str(datetime.datetime.now())  + '\n') 
    print('########  UPDATED Files  ######### -- runtime --' + str(datetime.datetime.now()))
    file_list_current = find_files(folder_path, initial)

    # extract dictionary keys into a set for old files
    flag_mod_date_happend = 0 # flag if a modification happened or not (default to no)

    for old_file in file_list_old:
        for cur_file in file_list_current:
            for old_key, old_value in old_file.items():
                for cur_key, cur_value in cur_file.items():
                    if old_key == cur_key and old_value != cur_value:
                        flag_mod_date_happend = 1 # flags modification happened
                        print(cur_key + ' -- Last Modified Date: ' + cur_value)
                        with open(folder + '_log.txt', 'a+') as log:
                            log.writelines(cur_key + ' -- Last Modified Date: ' + cur_value + '\n')

    if flag_mod_date_happend == 0: # flag if a modification did not happened
        with open(folder + '_log.txt', 'a+') as log:
             log.writelines('No files were modified' + '\n')
        print('No files were modified')


def main():
    print("######################################################")
    print("     Welcome to the Detect File Updates Program ")
    print()
    print(" This program will monitor changes in a folder each time ")
    print(" you drag and drop a folder into it.")
    print()
    print("          Created by: Joel Anderton")
    print("          Updated: 5/11/2019")
    print("          version: 1.0")
    print()
    print("######################################################")
    print('For instructions, type "help"')
    print()

    folder_path  = input('Drag/drop in the folder you want to monitor changes: ')
    print()

    if folder_path == 'help':
        print('''
                Step 1. Drag and drop the folder you want to monitor directly 
                        into the black space of the program. This puts in the 
                        path to the folder and initializes the folder by recording 
                        the current files and folders and their last modified times.
                
                Step 2. Whenever you want to check to see if any changes happened inside
                        the folder, restart the program and drag/drop the folder back into it.
                        
                Step 3. Review the files that were added/deleted/moved or modified the program
                        shows. Or refer to the _log.txt file for a history of what has happend to the
                        folder since the last time the program was run. The _log.txt file is created
                        in the same location of this program.
                ''')
        print()
        folder_path  = input('Drag/drop in the folder you want to monitor changes: ')
        print()

    folder_path =  folder_path.replace('"','')
    folder = re.split(r'\\', folder_path)
    folder = folder[-1:][0]

    # check if saved history file that holds the folder history exists (pickle file)
    try:
        with open(folder + '.pkl', 'rb') as fh:
            initial = 0 # flags that folder has not been initialized
            file_list = pickle.load(fh)
            compare_filenames(file_list, folder_path, folder, initial)
            compare_mod_date(file_list, folder_path, folder, initial)
            file_list = find_files(folder_path, initial)
            save_history(file_list, folder)

    except FileNotFoundError:
        initial = 1  # flags that folder is being initialized
        print('Initialized monitoring')
        file_list = find_files(folder_path, initial)
        save_history(file_list, folder)

    finally:
        print('Done!')
        end = input('Press Enter....')

if __name__ == '__main__':
    main()

