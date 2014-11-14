Clean SplashID DB (v3) file
===========================

Syncing with mobile SplashID app sometimes dupes all entries and adds junk non-ASCII entries.
This script helps remove these bad entries - my DB went from ~2500 entries to ~900 entries.

Usage
-----
./fixsplashidvid.py splashid_vid_input splashid_vid_output

Credit
------
Based on linuxsquad's Convert-SplashID-to-KeePassX scripts from https://github.com/linuxsquad/Convert-SplashID-to-KeePassX

File format
-----------
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

