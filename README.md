# BookSuck
Contact email: okdev99@gmail.com

This is a repository for my project BookSuck.

Information about my program can be found from booksuck-README.txt.

If you want to run the source code, then you need the following depencies:
- python 3
- cloudscraper
- tqdm

If you do not have these use pip to install them.

Github repository only has the programs source code. If you want to have a executable version, then you can download them from this Google drive folder: https://drive.google.com/drive/folders/1-_YRMVwOQR8fLahNohXtPSfA4vzWnJ4B?usp=sharing

The executable versions are made with a program called pyinstaller, in a macOS Catalina version, Windows 10 and Parrot Home (Debian based).

-> Sidenote, I have noticed that somehow some executable files have stopped working, even if it was previously working. This could be because of some updates to my emulator or on the libraries of my code.

If a executable folder has a "onefile" on it's name, then you only need to download the one file inside. If there is no "onefile" on the folder, the you need to download the specific folder with the wanted program version, in it's entirety. Inside this folder is the executable which can be used to run the program. Other files on the folder are depencies and libraries.

---Changelog---
BookSuck 1.6.2 (24.08.2022)
- Added unescaping HTML special characters

BookSuck 1.6.1 (15.07.2022)
- If scraped page text is the same as previous text, it is not saved to file
- If next chapter url is the same as previous, halt the operation with some instructions on how to proceed

BookSuck 1.6 (30.06.2022)
- Incorrect input is identified and help text added
- Program no longer iterates chapters, but looks for "next" button on page and copies it's link
- Handling of multiple (fractioned) chapters has been added
- Handling of "<table>, <caption>, <tbody>, <td> and <tr>" tags has beend added

BookSuck 1.5 (19.06.2022)
- Compatible with macOS filesystem
- Executable versions available (win, macOS, linux)

BookSuck 1.4 (17.06.2022)
- Compatible with Windows filesystem

BookSuck 1.3 (11.06.2022)
- User can now choose to use chapter title as filename or inputted book name
- Handling of "<span>" tags has been added

BookSuck 1.2 (10.06.2022)
- Handling of "<em>" tags has been added
- Program reads the chapter title and uses it to name its output file
- Rudimentary error correction has been added

BookSuck 1.1 (08.06.2022)
- Progress bar has been added

BookSuck 1.0 (07.06.2022)
- Program is operational
