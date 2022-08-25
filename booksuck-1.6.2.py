#!/usr/bin/env python3
#coding: utf-8

#Copyright notice is at the end.

from urllib.request import HTTPError
from html import unescape, escape
from tqdm import tqdm
from os import mkdir, system
from re import search
from cloudscraper import create_scraper

version = "1.6.2"

#These tags are removed from the text, but the text inside of them is saved.
removed_tags = ["<em>", "</em>", "<strong>", "</strong>", "<hr>", "</hr>", "<span>", "</span>", "<table>", "</table>", "<caption>", "</caption>", "<tbody>", "</tbody>", "<td>", "</td>", "<tr>", "</tr>", "<i>", "</i>"]

forbidden_tags = ["<sub>", "</sub>", "<a href=\""]

#If filename is based on title, these characters are removed from the filename.
forbidden_chars = ["#", "%", "&", "{", "}", "/", "\\", "<", ">", "€", "$", "!", "?", "+", "@", "\"", "'", "´", "`", "*", ":", ";"]

#This is a list of website where this program is known to work.
working_websites = ["www.lightnovelpub.com", "www.readlightnovel.me"]

#Program looks for these buttons on website
next_buttons = ["next", "Next", "NEXT", "next chapter", "Next Chapter", "Next chapter", "next Chapter", "NEXT CHAPTER"]

href = "href=\""

previous_chapter_txt = ""
previous_url = ""

print(f"BookSuck {version} is starting.\nRefer to associated README for more details.\n")

#Input & overview loop
while True:
    #Url input loop
    while True:
        run_anyway = ""
        print("Inputted url must be the url of the books starting chapter, not the default page of the website!")
        print("For example: https://lightnovelpub.com/gourmet-of-another-world-chapter-1")
        url = input("\nInput the books starting chapter url: ")
        website = url[url.find("//")+len("//"):url.find("/",8)]

        if url.find("https://",0,8) == -1 and url.find("http://",0,7) == -1:
            print("Attention! Inputted url must have \"https://\" or \"http://\" prefix.")
            run_anyway = "n"
        elif website not in working_websites:
            print("Warning. Inputted website has not been tested to work with program.")

            while True:
                run_anyway = input("Proceed anyway? (yes/no): ")
                if run_anyway in ["y", "yes", "n", "no"]:
                    break

        if run_anyway in ["y", "yes", ""]:
            break
    
    print("--------------------------------------------------")
    while True:
        ending_chapter_number = input("Input the desired ending chapter (as a number): ")
        if ending_chapter_number.isdigit():
            break
        print("Attention! Input must be number.")

    print("--------------------------------------------------")
    print("Inputted book's name is used in absence of a title to determine the filename or if so chosen, always determine the filename.")
    book_name = input("Input the books name: ")

    print("--------------------------------------------------")
    while True:
        chapter_file_name_based_on_book_name = input("Use book name as a filename? (yes/no): ")
        if chapter_file_name_based_on_book_name in ["y", "yes", "n", "no"]:
            break
    
    #Folder path input loop
    print("--------------------------------------------------")
    print("Inputted folder path must be a absolute path not a relative path, in essence it needs to start with a letter in Windows systems and with \"/\" in macOS or linux systems.")
    print("For example:")
    print("Windows: C:\\Users\\user\\Books\\")
    print("macOS and linux: /home/user/Books/\n")
    while True:
        folder_path = input("Input the output folder path: ")
        if folder_path[-1] != "/" and folder_path[-1] != "\\":
            print("Attention! Folder path must end with \"\\\" or \"/\".\nOtherwise it is not a folder, but a file.")
        elif folder_path[0] != "/" and folder_path[1] != ":":
            print("Attention! Folder path must start with a letter or with \"/\".")
        else:
            break
    
    print("--------------------------------------------------")
    print("Generate a folder based on book name, where chapters are saved.")
    while True:
        generate_folder = input("Generate folder? (yes/no): ")
        if generate_folder in ["y", "yes", "n", "no"]:
            break
    
    print("--------------------------------------------------")
    print("\nOverview:")
    print(f"Starting chapter url: {url}")
    print(f"Ending chapter: {ending_chapter_number}")
    print(f"Book name: {book_name}")
    print(f"Chapter filename will be based on inputted name (yes/no): {chapter_file_name_based_on_book_name}")
    print(f"Output path: {folder_path}")
    print(f"Generate folder (yes/no): {generate_folder}\n\n")

    choices_right = ""
    while True:
        choices_right = input("Begin the operation? (yes/no): ")

        if choices_right in ["y", "yes", "n", "no"]:
            break
    
    if choices_right in ["y", "yes"]:
        break

if "\\" in folder_path:
    directory_separator = "\\"
elif "/" in folder_path:
    directory_separator = "/"

website_url = url[0:url.find("/", 10)]

#Find url's starting chapter number
t = -1
while True:
    last_line = url.find("-", t)
    if last_line == -1:
        t -= 1
    else:
        t = -1
        break

if url[last_line-1].isdigit() and url[last_line+1].isdigit():
        
    while True:
        second_last_line = url.find("-", last_line+t)
        if second_last_line == last_line:
            t -= 1
        else:
            t = -1
            break
    start_chapter_number = url[second_last_line+1:last_line]
else:
    start_chapter_number = url[last_line+1:]
    while True:
        if start_chapter_number[-1].isdigit():
            break
        else:
            start_chapter_number = start_chapter_number[:-1]

scraper = create_scraper()

if generate_folder in ["y", "yes"]:
    try:
        mkdir(folder_path + book_name + directory_separator)
    except OSError as e:
        print(f"Could not create a folder as a: {folder_path + book_name + directory_separator}")
        print("Error code: ", e)
        print("Check if the program has read, write & execute permissions and the folder does not already exist.")
        system("pause")
        exit()

progressbar = tqdm(total=int(ending_chapter_number)+1-int(start_chapter_number), desc="Progress: ")

#Website scraping & content manipulation loop
i = 1
previous_chapter = ""
while True:

    #Find current chapter number
    t = -1
    while True:
        last_line = url.find("-", t)
        if last_line == -1:
            t -= 1
        else:
            t = -1
            break

    if url[last_line-1].isdigit() and url[last_line+1].isdigit():
        
        while True:
            second_last_line = url.find("-", last_line+t)
            if second_last_line == last_line:
                t -= 1
            else:
                t = -1
                break
        chapter_number = url[second_last_line+1:last_line]
    else:
        chapter_number = url[last_line+1:]
        while True:
            if chapter_number[-1].isdigit():
                break
            else:
                chapter_number = chapter_number[:-1]

    if chapter_number == previous_chapter:
        i_iterator = "-" + str(i)
        i += 1
    else:
        i = 1
        i_iterator = ""
        previous_chapter = chapter_number
        progressbar.update(1)

    #Scrape the text from site
    try:
        page_content = scraper.get(url).text
    except HTTPError as e:
        progressbar.close()
        print("\nTrying to reach the website returned an error!")
        print(f"Website: {url}")
        print("Error: ", e)
        system("pause")
        exit()

    #Convert html entities to text
    page_content = unescape(page_content)

    #content start search was here
    book_txt = ""
    title_name = ""

    #Determine the title of the chapter
    content_title_start_location = page_content.find("<title>")
    content_title_end_location = page_content.find("</title>")

    if content_title_start_location != -1:
        title_name = page_content[(content_title_start_location + len("<title>")):content_title_end_location]

        for j in list(range(0, len(forbidden_chars))):
            title_name = title_name.replace(forbidden_chars[j], "")

        book_txt = book_txt + title_name + "\n\n"
        is_title = True
    else:
        title_name = book_name
        book_txt = book_txt + title_name + "-chapter-" + chapter_number + i_iterator + "\n\n"
        is_title = False

    #Scraped page, paragraph finding, generating book_txt (after loop, book_txt is finished)
    content_start_search = 0
    while True:
        content_p_start_location = page_content.find("<p>", content_start_search)
        content_p_end_location = page_content.find("</p>", content_p_start_location + 1)

        if content_p_start_location == -1:
            break
        
        book_line = page_content[(content_p_start_location + len("<p>")):content_p_end_location].strip("\n\t")

        for l in list(range(len(removed_tags))):
            book_line = book_line.replace(removed_tags[l], "")

        
        tag_found = False
        for tag in forbidden_tags:
            if tag in book_line:
                tag_found = True
        
        if not tag_found and book_line != "":
            book_txt = book_txt + book_line + "\n\n"
        
        content_start_search = content_p_start_location + 1

    if chapter_file_name_based_on_book_name in ["y", "yes"]:
        title_name = book_name

    if generate_folder in ["y", "yes"]:
        file_name = book_name + directory_separator + title_name
    else:
        file_name = title_name

    if is_title and (chapter_file_name_based_on_book_name in ["n", "no"]):
        file_name = file_name + ".txt"
    else:
        file_name = file_name + "-chapter-" + chapter_number + i_iterator + ".txt"

    #If book_txt is the same as previous chapter, do not copy to file
    if book_txt[book_txt.find("\n\n"):] is previous_chapter_txt[previous_chapter_txt.find("\n\n"):]:
        print()
    else:
        try:
            with open(folder_path + file_name, "w", encoding="utf-8") as txt_file:
                txt_file.write(book_txt)
        except OSError as e:
            progressbar.close()
            print("Writing file to the folder in path: ", folder_path, " failed.")
            print("Check if BookSuck program has write, read and execute permissions on the desired folder.")
            print("Error: ", e)
            system("pause")
            exit()
    
    end_reached = search(("([^0-9]" + ending_chapter_number + "[^0-9])"), (url + "-"))

    if end_reached:
        break

    #Looks for "next" button on website and copies it's link
    if website == "www.lightnovelpub.com":
        page_find_next = page_content.find("a rel=\"next\"")
    elif website == "www.readlightnovel.me":
        x = page_content.find("class=\"next next-link\">")

        if x == -1:
            progressbar.close()
            print("The end of the novel has been reached.")
            break

        while True:
            if page_content.find(href, x, x+7) != -1:
                page_find_next = page_content.find(href, x, x+7)
                break
            else:
                x -= 1

    if page_find_next == -1:
        for n in next_buttons:
            page_find_next = page_content.find(f"a rel=\"{n}\"")
            if page_find_next != -1:
                break
    
    if page_find_next == -1:
        progressbar.close()
        print("Next button from website cannot be found!")
        print(f"This program looks for: {next_buttons}")
        exit()

    page_find_next_href_start = page_content.find(href, page_find_next) + len(href)
    page_find_next_href_end = page_content.find("\"", page_find_next_href_start+2)
    next_chapter = page_content[page_find_next_href_start:page_find_next_href_end]

    if "javascript" in next_chapter:
        progressbar.close()
        print("The end of the novel has been reached.")
        break
    
    if (website in url) and (("https://" or "http://") in url):
        url = next_chapter
    elif website in url:
        url = "https://" + next_chapter
    else:
        url = website_url + next_chapter
    
    if url == previous_url:
        progressbar.close()
        print("Next chapter link is the same as the current chapter url.")
        print("Check manually from the website, if the next chapter link actually points to the next chapter.")
        print("If not, then continue downloading the book where the program left.")
        print(f"Current chapter number: {chapter_number}")
        print(f"Ending chapter number: {ending_chapter_number}")
        print(f"Current url: {url}")
        system("pause")
        exit()
    
    previous_chapter_txt = book_txt
    previous_url = url

progressbar.close()
print(f"\nBookSuck {version}:")
print(f"{book_name} has been succesfully downloaded.")
system("pause")

#    --Start of copyright notice--

#    BookSuck is a program which looks at a inputted website url and downloads it's
#    text inside html body tags, while removing <sub> tags text and just other tags. The downloaded text is saved
#    according to user input.
#    Copyright (C) 2022  Otto Kuusniemi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#    Developer contact
#    Email: okdev99@gmail.com

#    --End of copyright notice--