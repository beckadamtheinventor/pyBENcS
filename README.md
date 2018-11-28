# pyBENcS
A file encryption system written in python 3 #Devember

This program will be able to encrypt files from both the command line and a 'make'file.
I intend to have this program work on any python capable system which can also work with files.

Current platforms:
+ Linux
+ (untested) Windows

Goal platforms:
+ Windows
+ Macintosh
+ Website (possibly)

Current features:
+ Gap/skip encryption method
+ Randomize Encryption key, or have the user choose.
+ Encrypt from any file's raw bytes, and output them in unsquished hexidecimal.
+ Decrypt from a file containing unsquished hexidecimal, and output raw bytes.
+ Encrypt/Decrypt files or uses a makefile; a list of files and settings.

Goal features:
+ More than on encryption method. {*IMPORTANT*}
+ Encrypt from any file's raw bytes, and output them in base64.
+ Decrypt from a file containing base64, and output raw bytes.
+ Encrypt/Decrypt from a file containing unsquished hex, and output in unsquished hex.
+ Encrypt/Decrypt user input data.
