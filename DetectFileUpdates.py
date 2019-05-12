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
import pickle


# find all files and files in subfolders: their names and last modified date/time
def find_files():
    folder_path = r'/Users/joelanderton/Desktop/Here'
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(file)
            print(os.path.join(root, file))
            mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))

            file_dic = {file: mod_time}
            file_list.append(file_dic)
            print(file_list)
            save_history(file_list)


# save the state of the folder
def save_history(file_list):
    with open ('folder_history.pkl', 'wb') as f:
        pickle.dump(file_list, f)

# compare the text file to the folder's current state
def compare(file_list):
    pass


def main():

    try:
        fh = open('folder_history.pkl')

    except FileNotFoundError:
        find_files()

    else:
        fh = open('folder_history.pkl', 'rb')
        file_list = pickle.load(fh)
        print(file_list)


if __name__ == '__main__':
    main()
