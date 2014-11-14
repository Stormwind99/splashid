#!/usr/bin/env python
"""
Clean SplashID DB (v3) file

Syncing with mobile SplashID app sometimes dupes all entries 4x and adds junk non-ASCII entries
This script helps remove these bad entries

Based on linuxsquad's Convert-SplashID-to-KeePassX scripts from https://github.com/linuxsquad/Convert-SplashID-to-KeePassX

From SplashID website:
 You may also import and export SplashID records in CSV format.
 CSV stands for Comma Separated Values, and is a common file format
 readable by most spreadsheets, databases and word processors.
 If you wish to import a CSV file, the data must be in the following format:

    Type, Field 1, Field 2, Field 3, Field 4, Field 5, Field 6, Field 7, Field 8, Field 9, Date Modified, Notes, Category

 It is easy to create the above format in Excel by creating a spreadsheet
 with 13 columns (as designated above) with one record per row.
 Then save the splashid_export_f in CSV format.

 Note: When importing data, if the type field is blank the record
 will be placed in Unfiled. If there is a type name and it
 does not match an existing type a new type will be created.
"""

import sys
import csv

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

splashid_type = {}
splashid_value_unique = {}
splashid_value = []
splashid_type_prev = '0'

if (len(sys.argv) > 1):
    splashid_vid_input = sys.argv[1]
    splashid_vid_export = sys.argv[2]
else:
    print "Usage: " + sys.argv[0] + " splashid_vid_input splashid_vid_output"
    quit(1)

# read splashid vid file

with open(splashid_vid_input, 'rb') as csv_file:
    csv_imported_splashid = csv.reader(csv_file)
    with open(splashid_vid_input+".log", 'w') as log_file:
        for i, row in enumerate(csv_imported_splashid):
            csv_entry = [ item for item in row ]
            try:
                # handle type entries
                if csv_entry[0] == 'T':
                    try:
                        if is_ascii(csv_entry[2]):
                            if csv_entry[1] in splashid_type:
                                pass
                            else:
                                splashid_type[csv_entry[1]] = csv_entry[2:]
                                #log_file.write("  INFO: Group Name ="+csv_entry[2]+", Group ID ="+csv_entry[1]+"\n")
                                #print("  INFO T: Group Name ="+csv_entry[2]+", Group ID ="+csv_entry[1])
                                pass
                            splashid_type_prev = csv_entry[1]
                        else:
                             #print "  WARN T: skipping non-ascii T=", csv_entry[1], " = ", csv_entry[2:]
                             pass
                    except IndexError, name:
                        pass
                # handle value entries
                if csv_entry[0] == 'F':
                    #if csv_entry[1] != splashid_type_prev:
                    if csv_entry[1] not in splashid_type:
                        #log_file.write("  WARN: Unrecognized Group ID F="+csv_entry[1]+", Guessing a correct one T="+splashid_type_prev+"\n")
                        #print("  WARN F: Unrecognized Group ID F="+csv_entry[1]+", Guessing a correct one T="+splashid_type_prev)
                        csv_entry[1] = splashid_type_prev
                    # remove rough match dupes
                    unique_value = "-"
                    unique_value = unique_value.join(csv_entry[1:5])
                    print "unique_value=", unique_value
                    if not is_ascii(csv_entry[2]):
                        #print "  WARN F: skipping non-ascii ", csv_entry[2]
                        pass
                    elif unique_value in splashid_value_unique:
                        #print "  WARN F: skipping dupe ", unique_value
                        pass
                    else:
                        splashid_value_unique[unique_value] = csv_entry[1:]
                        splashid_value.append(csv_entry[1:])
            except IndexError, name:
                pass


# output cleaned splashid vid file

prev_type=-1

with open(splashid_vid_export, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["SplashID vID File -v2.0"])
    writer.writerow(["F"])

    for single_record in splashid_value:
        if single_record[0] != prev_type:
             prev_type = single_record[0]
             writer.writerow( ["T", prev_type] + splashid_type[prev_type] )
        writer.writerow( ["F"] + single_record )
