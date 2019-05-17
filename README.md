# Detect File Updates
Python application to detect all file updates or additions in a given folder and its subfolders compared to the last time the program was run

# What I Learned
* Compared the contents of both keys and values between 2 dictionaries.
* File paths greater than 255 characters makes Python return "file does not exist". The work around is to add u'\\\\\\\\?\\\\' to the beginning of the file path. This converts it to a Universal Naming Convention (UNC) path name and unicode file name.
    https://stackoverflow.com/questions/12022364/python-windows-maximum-directory-path-length-workaround
* Practice using "pickle" to save the list of dictionaries so they can be compared at a later date.
* Practice features of Github.
