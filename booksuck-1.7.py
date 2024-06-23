#!/usr/bin/env python3
#coding: utf-8

#Copyright notice is at the end.

#Cloudscraper is failing when the target site checks with cloudflare when the scraping has run for about 10-20 seconds.
#The program will just scrape the "Just a moment..." cloudflare page and halt, since no link for the next page is found.
#The program tells the last link it tried to scrape and you can resume from there, but it is cumbersome.
#-> try to make cloudscraper work or consider an alternative

from urllib.request import HTTPError
from html import unescape
from tqdm import tqdm
from os import mkdir, system
from bs4 import BeautifulSoup
import cloudscraper, re, Levenshtein

#These tags are removed from the text, but the text inside of them is saved.
removed_tags = ["<em>", "</em>", "<strong>", "</strong>", "<hr>", "</hr>", "<span>", "</span>", "<table>", "</table>", "<caption>", "</caption>", "<tbody>", "</tbody>", "<td>", "</td>", "<tr>", "</tr>", "<i>", "</i>", "<b>", "</b>"]

forbidden_tags = ["<sub>", "</sub>", "<a href=\""]

#If filename is based on title, these characters are removed from the filename.
forbidden_chars = ["#", "%", "&", "{", "}", "/", "\\", "<", ">", "€", "$", "!", "?", "+", "@", "\"", "'", "´", "`", "*", ":", ";"]

#This is a list of website where this program is known to work.
working_websites = ["www.lightnovelpub.com", "www.readlightnovel.me"]

href = "href=\""

previous_chapter_txt = ""
previous_urls = []

i = 1
i_iterator = ""

previous_chapter = ""
previous_chapter_txt = ""
is_title = None

version = "1.7"

def main():
    class Book:
        """
        Book class has almost every variable needed for the operation

        Parameters:
        book_name
        url
        website
        ending_chapter_number
        chapter_file_name_based_on_book_name
        folder_path
        generate_folder
        page
        title_name

        Functions:
        set_page_info(): Set current page, url and title name to the list of pages
        save_to_file(): Save all pages in the pages list to specified folder
        """
        def __init__(self, input):
            self.book_name = input[0]
            self.url = input[1]
            self.website = input[2]
            self.ending_chapter_number = input[3]
            self.chapter_file_name_based_on_book_name = input[4]
            self.folder_path = input[5]
            self.generate_folder = input[6]
            self.page = ""
            self.title_name = ""
            self.book_pages = []

        def __str__(self):
            return f"Book name: {self.book_name}\nUrl: {self.url}\nWebsite: {self.website}\nEnding chapter: {self.ending_chapter_number}\nFile based on book name: {self.chapter_file_name_based_on_book_name}\nFolder path: {self.folder_path}\nGenerate folder: {self.generate_folder}"

        def set_page_info(self, filename: str):
            """Set classes own variables to a list with, page text, title_name and url of the chapter."""

            self.book_pages.append((self.page, self.title_name, filename))
            progressbar.update(1)

        def save_to_file(self):
            """Save chapters in the pages list to aready specified output folder."""
            progressbar = tqdm(total=len(self.book_pages), desc="Writing: ")

            for i in list(range(len(self.book_pages))):
                if self.chapter_file_name_based_on_book_name in ["y", "yes"]:
                    self.title_name = self.book_name
                else:
                    self.title_name = self.book_pages[i][2] # is a filename

                #If book_txt is the same as previous chapter, do not copy to file
                if self.book_pages[i][0][self.book_pages[i][0].find("\n\n"):] is not self.book_pages[i-1][0][self.book_pages[i-1][0].find("\n\n"):]:
                    try:
                        with open(self.folder_path + self.book_pages[i][2], "w", encoding="utf-8") as txt_file:
                            txt_file.write(unescape(self.book_pages[i][0]))
                            progressbar.update(1)
                    except OSError as e:
                        progressbar.close()
                        print("Writing file to the folder in path: ", self.folder_path, " failed.")
                        print("Check if BookSuck program has write, read and execute permissions on the desired folder.")
                        print("Error: ", e)
                        system("pause")
                        exit(1)
            progressbar.close()

    def ask_input() -> tuple:
        """
        Ask user for input and return it in a tuple format, ready for book class.

        Returns:
        In a tuple:
            book_name (str): The name of the book
            url (str): Url of the chapter
            website (str): Website where book is
            ending_chapter_number (str): The chapter number of the ending chapter
            chapter_file_name_based_on_book_name (str): Whether file name should be book_name
            folder_path (str): The path to designated output folder
            generate_folder (str): Whether the book should saved on its own folder
        """
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
            return book_name, url, website, ending_chapter_number, chapter_file_name_based_on_book_name, folder_path, generate_folder
        else:
            system("pause")
            exit(0)

    def get_chapter_number(url: str) -> str:
        """Finds and outputs starting chapter number from url.

        Parameters:
        url (str): url of the specified chapter

        Returns:
        chapter_number (str): the chapter number from  inputted url
        """
        global previous_chapter, i, i_iterator

        #This returns function gets empty string for first run of the loop, so it returns somethin below 0 so it cannot loop into 0 1 chapters.
        if url == "":
            return "-1"
        else:
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
                    if chapter_number.isdigit():
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


            return chapter_number

    def make_folder():
        """Generates a folder with the specified name book.book_name to the book.folder_path"""
        try:
            mkdir(book.folder_path + book.book_name + directory_separator)
        except OSError as e:
            print(f"Could not create a folder as a: {book.folder_path + book.book_name + directory_separator}")
            print("Error code: ", e)
            print("Check if the program has read, write & execute permissions and the folder does not already exist.")
            system("pause")
            exit(1)

    def get_page_text() -> str:
        """Fetches the html page text in book.url

        Returns:
        page_content (str): content of the website of book.url
        """
        try:
            page_content = scraper.get(book.url).text
            return page_content
        except (HTTPError, ConnectionError) as e:
            progressbar.close()
            print("\nTrying to reach the website returned an error!")
            print(f"Website: {book.url}")
            print("Error: ", e)
            system("pause")
            exit(1)

    def get_title() -> str:
        """Searches page_content for <title> tags and if found returns it, if not found uses book_name

        Returns:
        title_name (str): if <title> is found; name of the <title> tag, if not found; book_name

        Side effects:
        is_title (bool): True if title found, false otherwise
        """
        global is_title
        title_name = page_content.title

        if title_name != None:
            title_name = str(title_name).replace("<title>", "").replace("</title>", "")
            for char in forbidden_chars:
                title_name = title_name.replace(char, "")
            title_name = title_name + "\n\n"
            is_title = True
        else:
            title_name = book.book_name + "-chapter-" + chapter_number + i_iterator + "\n\n"
            is_title = False

        return title_name

    def get_book_text() -> str:
        """Iterates page_contents <p> tags and appends the text to book_text

        Returns:
        book_text (str): from page_content found paragraphs
        """
        book_txt = book.title_name + "\n"
        paragraph_list = page_content.find_all("p")
    
        for line in paragraph_list:
            book_line = str(line).replace("<p>", "").replace("</p>", "").replace("\n", "").replace("\t", "")
            for tag in removed_tags:
                book_line = book_line.replace(tag, "")
    
            tag_found = False
            for tag in forbidden_tags:
                if tag in book_line:
                    tag_found = True

            if not tag_found and book_line != "":
                book_txt = book_txt + book_line + "\n\n"

        return book_txt

    def find_next_chapter_link() -> str:
        """Finds the most similar link in all <a href=> tags to the current chapter link.
        Returns:
        next_chapter (str): link to the next chapter, or if not found: not found
        """

        a_list = page_content.select("a[href]")
        link_list = []
        url = book.url.replace(book.website, "").replace("https://", "").replace("http://", "")
        
        for a in a_list:
            if "next" in str(a).lower():
                link_list.append(a)

        for i in list(range(len(link_list))):
            #Iterate links, and rate them on how much they differ to the current url and then pick the min points gotten
            levenshtein_distance = Levenshtein.distance(str(link_list[i].get("href")), url)
            link_list[i] = (str(link_list[i].get("href")), levenshtein_distance)

        link_list.sort(key=lambda cell: cell[1])
        
        if (len(link_list) != 0):
            next_chapter = link_list[0][0]

            #Frankly, I don't get it why this needs to iterate over "link_list" and compare "next_chapter" and not "link"
            i = 1
            for link in link_list:
                if (book.website not in next_chapter) and (("https://" or "http://") not in next_chapter):
                    next_chapter = website_url + next_chapter
                elif (("https://" or "http://") not in next_chapter):
                    next_chapter = "https://" + next_chapter


                is_previous_url = False
                for previous_url in previous_urls:
                    if next_chapter == previous_url:
                        is_previous_url = True

                if is_previous_url:
                    next_chapter = link[0]
                elif "javascript" not in next_chapter:
                    previous_urls.append(next_chapter)
                    return next_chapter

        progressbar.close()
        print("Next chapter cannot be found!")
        while True:
            user_input = input("Write scraped pages to folder? (y/n): ")
            if user_input.lower() in ["n", "no"]:
                print("Last url: " + book.url)
                break
            elif user_input.lower() in ["y", "yes"]:
                book.save_to_file()
                print("Last url: " + book.url)
                break

        system("pause")
        exit(0)

    def make_filename() -> str:
        """Generate a filename based on book.title_name and i_iterator (for sub chapters).

        Returns:
        filename (str): filename based on title and i_iterator
        """
        if book.generate_folder in ["y", "yes"]:
            file_name = book.book_name + directory_separator

        if book.chapter_file_name_based_on_book_name in ["n", "no"]:
            file_name = file_name + book.title_name.replace("\n", "") + ".txt"
        else:
            if is_title:
                file_name = file_name+ book.book_name + "-chapter-" + chapter_number + i_iterator + ".txt"
            else:
                file_name = file_name + book.title_name.replace("\n", "") + ".txt"

        return file_name

    print("BookSuck Copyright (C) 2022-2024  Otto Kuusniemi\nThis program comes with ABSOLUTELY NO WARRANTY; for details refer to LICENSE.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; refer to LICENSE for details.\n")

    print(f"BookSuck {version} is starting.\nRefer to associated README for more details.\n")

    book = Book(ask_input())

    if "\\" in book.folder_path:
        directory_separator = "\\"
    elif "/" in book.folder_path:
        directory_separator = "/"

    website_url = book.url[0:book.url.find("/", 10)]

    starting_chapter_number = get_chapter_number(book.url)

    scraper = cloudscraper.create_scraper(
        delay=10,
        browser={
            'browser': 'chrome',
            'platform': 'android',
            'desktop': False
        }
    )

    if book.generate_folder in ["y", "yes"]:
        make_folder()

    progressbar = tqdm(total=int(book.ending_chapter_number)+1-int(starting_chapter_number), desc="Scraping: ")

    #Website scraping & content manipulation loop
    while True:
        global previous_chapter_txt

        page_content = BeautifulSoup(get_page_text(), "html.parser")

        book.title_name = get_title()

        book.page = get_book_text()

        if book.page == previous_chapter_txt:
            progressbar.close()
            print("\nChapter text is the same as the previous!")
            print("Check manually from the website if the next chapter link is working.")
            print("If it isn't then continue the operation from the next chapter.")
            system("pause")
            exit(1)

        chapter_number = get_chapter_number(book.url)

        filename = make_filename()
        book.set_page_info(filename)

        end_reached = re.search(("([^0-9]" + book.ending_chapter_number + "[^0-9])"), (book.url + "-"))

        if end_reached:
            break
        
        previous_chapter_txt = book.page
        book.url = find_next_chapter_link()

    progressbar.close()
    book.save_to_file()

    print(f"\nBookSuck {version}:")
    print(f"{book.book_name} has been succesfully downloaded.")
    system("pause")
    exit(0)

if __name__ == "__main__":
    main()

#    --Start of copyright notice--

#    BookSuck is a program which looks at a inputted website url and downloads it's
#    text inside html body tags, while removing <sub> tags text and just other tags. The downloaded text is saved
#    according to user input.
#    Copyright (C) 2022-2024  Otto Kuusniemi
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
