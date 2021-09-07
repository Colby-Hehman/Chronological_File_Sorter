import os.path, time
from os.path import isfile, join, isdir
from os import listdir
from datetime import date
import os
import exifread
import getpass


# Write the path of the directory you want sorted in "directory." Write the path you want the files sent to into "sort_to." Example: "C:\\Users\\David\\Pictures\\Camera Roll"
# EVerything will be sorted into a folder for their respective year, and then into their month (within the year folder)
# This is all done automatically, just enter the two values below and hit run
directory = "C:\\Users\\Colby Hehman\\Pictures\\testing folder\\5"
sort_to = "C:\\Users\\Colby Hehman\\Pictures\\life so far"


subfolders = [f.path for f in os.scandir(sort_to) if f.is_dir()]
monthnums = {"Jan": '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9',
             'Oct': '10', 'Nov': '11', 'Dec': '12'}
monthnames = {'1': '1-Jan', '2': '2-Feb', '3': '3-Mar', '4': '4-Apr', '5': '5-May', '6': '6-Jun', '7': '7-Jul',
              '8': '8-Aug', '9': '9-Sep', '10': '10-Oct', '11': '11-Nov', '12': '12-Dec'}


# Add function that sorts into year/month, and creates folder for each as needed
def add_to_folder(location, year, month):
    try:
        year_dirname = sort_to + "\\" + year
        month_dirname = year_dirname + "\\" + month
        file_type = location[location.rindex("."):]
        filename = location[location.rindex("\\") + 1:-(len(file_type))]
        if year_dirname in subfolders:
            year_subfolders = [f.path for f in os.scandir(year_dirname) if f.is_dir()]
            if month_dirname in year_subfolders:
                os.rename(location, month_dirname + "\\" + filename + file_type)
            else:
                os.mkdir(month_dirname)
                os.rename(location, month_dirname + "\\" + filename + file_type)
        else:
            os.mkdir(year_dirname)
            os.mkdir(month_dirname)
            os.rename(location, month_dirname + "\\" + filename + file_type)
    except FileExistsError:
        year_dirname = sort_to + "\\" + year
        copies_dirname = year_dirname + "\\" + "Copies"
        file_type = location[location.rindex("."):]
        filename = location[location.rindex("\\") + 1:-(len(file_type))]
        year_subfolders = [f.path for f in os.scandir(year_dirname) if f.is_dir()]
        if copies_dirname not in year_subfolders:
            os.mkdir(copies_dirname)
        os.rename(location, copies_dirname + "\\" + filename + file_type)
    except:
        print(location + "\tcaused an error")


this_year = int(str(date.today())[:4])
years_range = set(str(yr) for yr in range(1980, this_year + 1))
months_range = set(str(i) for i in range(0, 13))
days_range = set(str(i) for i in range(0, 32))
integers = set(str(i) for i in range(0, 10))


# Determines the year and month for each file and then calls add_to_folder()
def find_date(location):
    file_type = location[location.rindex("."):]
    filename = location[location.rindex("\\") + 1:-(len(file_type))]
    global sorted
    sorted = False
    # Sees if date is in name using pointers
    if len(filename) >= 6:
        l_pointer, r_pointer = 0, 4
        yearidx = None
        while r_pointer < len(filename) + 1:
            if filename[l_pointer: r_pointer] in years_range:
                yearidx = l_pointer
                break
            r_pointer += 1
            l_pointer += 1
        # If a year is found, the function will try to find the month and day. If successful, add_to_folder() is called
        # and sorted is made equal to True
        if yearidx is not None and int(yearidx) + 5 < len(filename):
            if filename[yearidx + 4] in integers:
                if len(filename[yearidx:]) >= 8:
                    if filename[yearidx + 4] == '0':
                        month = filename[yearidx + 5]
                    else:
                        month = filename[yearidx + 4: yearidx + 6]
                    if len(month) == 2:
                        if month[1] not in integers:
                            month = month[0]
                    if filename[yearidx + 6] == '0':
                        day = filename[yearidx + 7]
                    else:
                        day = filename[yearidx + 6: yearidx + 8]
                    if len(day) == 2:
                        if day[1] not in integers:
                            day = day[0]
                    if month in months_range and day in days_range:
                        sorted = True
                        add_to_folder(location, filename[yearidx: yearidx + 4], monthnames[month])
            else:
                filename_len = len(filename[yearidx:])
                if filename_len >= 8:
                    day = 'None'
                    if filename[yearidx + 5] == '0':
                        month = filename[yearidx + 6]
                    else:
                        month = filename[yearidx + 5: yearidx + 7]
                    if len(month) == 2:
                        if month[1] not in integers:
                            month = month[0]
                    if len(month) == 1:
                        if filename[yearidx + 5] == '0':
                            if filename[yearidx + 8] == '0':
                                if filename_len >= 10:
                                    day = filename[yearidx + 9]
                            else:
                                if filename_len >= 11:
                                    day = filename[yearidx + 8: yearidx + 10]
                                elif filename_len == 10:
                                    day = filename[yearidx + 8:]
                                elif filename_len == 9:
                                    day = filename[yearidx + 8]
                        else:
                            if filename[yearidx + 7] == '0':
                                if filename_len >= 9:
                                    day = filename[yearidx + 8]
                            else:
                                if filename_len >= 10:
                                    day = filename[yearidx + 7: yearidx + 9]
                                elif filename_len == 9:
                                    day = filename[yearidx + 7:]
                                elif filename_len == 8:
                                    day = filename[yearidx + 7]
                    else:
                        if filename[yearidx + 8] == '0':
                            if filename_len >= 10:
                                day = filename[yearidx + 9]
                        else:
                            if filename_len >= 11:
                                day = filename[yearidx + 8: yearidx + 10]
                            elif filename_len == 10:
                                day = filename[yearidx + 8:]
                            elif filename_len == 9:
                                day = filename[yearidx + 8]
                    if len(day) == 2:
                        if day[1] not in integers or day not in days_range:
                            day = day[0]
                    if month in months_range and day in days_range:
                        add_to_folder(location, filename[yearidx: yearidx + 4], monthnames[month])
                        sorted = True
    # If the year and month were not found, this will attempt to find them from the date taken metadata inside of photos
    if sorted is False:
        try:
            with open(location, 'rb') as fh:
                tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                dateTaken = str(tags["EXIF DateTimeOriginal"])
                year = dateTaken[:4]
                month = dateTaken[5:7]
                if month[0] == str(0):
                    month = month[1]
            add_to_folder(location, year, monthnames[month])
            sorted = True
        except:
            pass
    # If this doesn't work, this compares modification and creation dates and then goes with the oldest
    if sorted is False:
        modified = "%s" % time.ctime(os.path.getmtime(location))
        created = "%s" % time.ctime(os.path.getctime(location))
        mod_year = modified[20:24]
        cre_year = created[20:24]
        # Determines which is older, creation or modification date, and uses add_to_folder() on the oldest
        if cre_year != mod_year:
            if cre_year < mod_year:
                cre_month = created[4:7]
                add_to_folder(location, cre_year, monthnums[cre_month] + "-" + cre_month)
            else:
                mod_month = modified[4:7]
                add_to_folder(location, mod_year, monthnums[mod_month] + "-" + mod_month)
        else:
            cre_month = created[4:7]
            mod_month = modified[4:7]
            if cre_month <= mod_month:
                add_to_folder(location, cre_year, monthnums[cre_month] + "-" + cre_month)
            else:
                add_to_folder(location, mod_year, monthnums[mod_month] + "-" + mod_month)


# Uses find_date() function on each file within a directory, then does the same to every subdirectory (in each level
# below) using recursion
def sort_directory(location):
    only_files = [f for f in listdir(str(location)) if isfile(join(str(location), f))]
    try:
        only_files.remove("desktop.ini")
    except:
        pass
    for file in only_files:
        find_date(location + "\\" + file)
    subdirectories = [f for f in listdir(str(location)) if isdir(join(str(location), f))]
    if len(subdirectories) == 0:
        return
    for subdir in subdirectories:
        sort_directory(location + "\\" + subdir)



sort_directory(directory)
