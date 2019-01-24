#     This script is used to rename photos based on two columns in a .csv
#     Column 1 is the old name, column 2 is the new name.
#     The script also changes the image file extension from .JPG to .PNG
#     
#     Be sure to name the .csv flie old-names-new-names.csv and place in the same directory
#     as the python script and the image files.
#
#     To execute the script via cli use the following:
#     python rename-pics.py old-names-new-names.csv

import os
import csv

with open('old-names-new-names.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        name = row[0] + '.JPG'
        new = row[1] + '.PNG'
        if os.path.exists(name):
            os.rename(name, new)
        else:
            print name + " does not exist"
