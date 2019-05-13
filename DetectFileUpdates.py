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
import time
import datetime
import pickle


# find all files and files in subfolders: their names and last modified date/time
def find_files():
    folder_path = r'/Users/joelanderton/Desktop/Here'
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))
            file_dic = {file_path: mod_time}
            file_list.append(file_dic)
    return file_list


# save the state of the folder
def save_history(file_list):
    with open('folder_history.pkl', 'wb') as f:
        pickle.dump(file_list, f)


# compare the text file to the folder's current state
def compare_filenames(file_list_old):

    # find file differences:
    file_list_current = find_files()

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
        print('Check the following DELETED/MOVED files: ')
        with open('log.txt', 'a+') as log:
            log.writelines('################################################' + '\n') 
            log.writelines(str(datetime.datetime.now()) + ' -- DELETED/MOVED files:' + '\n')
        for path in list(diff_list1):
            print(path)
            with open('log.txt', 'a+') as log:
                log.writelines(path + '\n')

    elif diff_list2 != []:
        print('Check the following NEW files: ')
        with open('log.txt', 'a+') as log:
            log.writelines('################################################' + '\n')
            log.writelines(str(datetime.datetime.now()) + ' -- NEW files:' + '\n')
        for path in list(diff_list2):
            print(path)
            with open('log.txt', 'a+') as log:
                log.writelines(path + '\n')
    else:
        print('No files were added or removed changes')


def compare_mod_date(file_list_old):

    file_list_current = find_files()

    # extract dictionary keys into a set for old files
    flag_mod_date_happend = 0

    for old_file in file_list_old:
        for cur_file in file_list_current:
            for old_key, old_value in old_file.items():
                for cur_key, cur_value in cur_file.items():
                    if old_key == cur_key and old_value != cur_value:
                        flag_mod_date_happend = 1
                        print('Updated Modified Date: ' + cur_key + ' -- ' + cur_value)
                        with open('log.txt', 'a+') as log:
                            log.writelines('################################################' + '\n')
                            log.writelines(str(datetime.datetime.now()) + 'Updated Modified Date: ' + cur_key + ' -- ' + cur_value + '\n')

    if flag_mod_date_happend == 0:
        print('No files were modified')

def main():
    # check if folder history file exists
    try:
        with open('folder_history.pkl', 'rb') as fh:
            file_list = pickle.load(fh)
            compare_filenames(file_list)
            compare_mod_date(file_list)
            file_list = find_files()
            save_history(file_list)

    except FileNotFoundError:
        file_list = find_files()
        save_history(file_list)


if __name__ == '__main__':
    main()

