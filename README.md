# Chronological_File_Sorter
Automatically sorts every file within a directory (and all subdirectories) into new folders based on chronological order. For instance, if a picture was taken on August 8th, 1992, it would be sorted into the path "1992/Aug." 

The date of the file can be determined by one of three ways:
  - File title (if a timecode is included in the file title, it will be probably be found)
  - File metadata (exif)
  - File creation or modification date (whichever is older)

