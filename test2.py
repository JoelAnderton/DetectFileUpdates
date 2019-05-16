import os
import re
import time
import datetime
import pickle


# long_path = "S:\\IRB\\IRB Documents\\IRB Docs of collaborating centers\\OFC Collaborating Sites' Current & Prior Site IRB Appr ltrs & consents\\Hungary\\Hungary 09-10\\FWA for Foundation\\FWA Application\\GAT Foundations Application\\FWA Info Given to HU\\Good Clinical Practice Guidelines.pdf"
long_path = "S:\\IRB\\IRB Documents\\IRB Docs of collaborating centers\\OFC Collaborating Sites' Current & Prior Site IRB Appr ltrs & consents\\Hungary\\Hungary 09-10\\FWA for Foundation\\FWA Application\\GAT Foundations Application\\FWA Info Given to HU"

def find_files(folder_path, initial):
    #folder_path = r'/Users/joelanderton/Desktop/Here'
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            folder_path = os.path.join(root, file)
            print(folder_path)
            if initial == 1:
                display_file_name = re.split(r'\\', folder_path)
                display_file_name = display_file_name[-1:][0]
                print('Gathering files to monitor: ' + display_file_name)
            try:
                mod_time = time.ctime(os.path.getmtime(os.path.join(root, file)))
                print(mod_time)
            except:
                print('Greater than 255')
                mod_time = time.ctime(os.path.getmtime(os.path.join(u'\\\\?\\' + root, file)))
                print(mod_time)
            file_dic = {folder_path: mod_time}
            file_list.append(file_dic)
    print()
    return file_list

file_list = find_files(long_path, 1)

for i in file_list:
    print(i)