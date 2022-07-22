import os
from urllib.parse import urlencode
import subprocess
import re

url = 'http://10.10....'
token = 'h8...:q4...'

def insert_shelf(shelfname):
    # Create shelf 
    cmd = f"curl {url}api/shelves -H 'Authorization: Token {token}' -d 'name={shelfname}'"
    response = subprocess.run(cmd, shell=True, capture_output=True)
    shelfid = re.search(r'"id":(.*?)}', response.stdout.decode('utf-8')).group(1)
    return shelfid

def insert_book(bookname):
    # Create Book 
    cmd = f"curl {url}api/books -H 'Authorization: Token {token}' -d 'name={bookname}'"
    response = subprocess.run(cmd, shell=True, capture_output=True)
    bookid = re.search(r'"id":(.*?)}', response.stdout.decode('utf-8')).group(1)
    return bookid

def insert_chapter(bookid, chaptername):
    # Create Chapter 
    cmd = f"curl {url}api/chapters -H 'Authorization: Token {token}' -d book_id={int(bookid)} -d 'name={chaptername}'"
    response = subprocess.run(cmd, shell=True, capture_output=True)
    chapterid = re.search(r'"id":(.*?),"', response.stdout.decode('utf-8')).group(1)
    return chapterid

def insert_page(bookorchapterid,pagename,files,filepath,mode="book"):
    # mode: "book" or "chapter"
    # Create Page 
    cmd = f"curl {url}api/pages -H 'Authorization: Token {token}' -d {mode}_id={int(bookorchapterid)} -d 'name={pagename}' -d html='<p></p>' "
    response = subprocess.run(cmd, shell=True, capture_output=True)
    pageid = re.search(r'"id":(.*?),"', response.stdout.decode('utf-8')).group(1)

    html_content = ''
    for file in files: 
        # Upload file
        cmd = f"curl {url}api/attachments -H 'Authorization: Token {token}' -F 'file=@{filepath}{file}' -F 'name={file}' -F uploaded_to={pageid}"
        response = subprocess.run(cmd, shell=True, capture_output=True)
        a_id = re.search(r'"id":(.*?),"', response.stdout.decode('utf-8')).group(1)
        
        html_content += f'<p><a href="{url}attachments/{a_id}" target="_blank" rel="noopener" data-mce-href="{url}attachments/{a_id}" data-mce-selected="inline-boundary">{file}</a></p>'
   
    # Update Link on Page
    html = {"html":html_content}
    cmd = f"curl -X PUT {url}api/pages/{pageid} -H 'Authorization: Token {token}' -d {urlencode(html)}"
    subprocess.run(cmd, shell=True)

# Potential test calls
# shelfid = insert_shelf("TEST")
# bookid = insert_book("TESTBOOK")
# chapterid = insert_chapter(bookid, "TESTCHAPTER")
# insert_page(bookid,"TESTPAGE in Book","test.pdf","/Users/.../test.pdf","book")
# fs = ['....docx', '....pdf']
# fs_root = '/Users/...'+'/'
# insert_page(chapterid,"TESTPAGE in Chapter",fs,fs_root,"chapter")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

path='/Users/...'
base_path_len = 10 # How deep is the directory, check the len(root.split(os.sep))
ignore_files = [".DS_Store"]

for root, dirs, files in os.walk(path):
    path = root.split(os.sep)
    files = [f for f in files if f not in ignore_files]
    if (len(path) - base_path_len) == 0: 
        print("shelf", os.path.basename(root))
        insert_shelf(os.path.basename(root))
        for file in files:
            print(f"{bcolors.FAIL}ERROR:shelfPAGE {bcolors.ENDC}", f'{root}/{file}')
    elif (len(path) - (base_path_len + 1)) == 0: 
        print("BOOK", os.path.basename(root))
        bookid = insert_book(os.path.basename(root))
        if len(files)>0:
            print("BOOK ATTACHMENTS ", files)
            insert_page(bookid,"Attachments",files,f"{root}/","book")
    elif (len(path) - (base_path_len + 2)) == 0: 
        print("CHAPTER", os.path.basename(root))
        chapterid = insert_chapter(bookid, os.path.basename(root))
        if len(files)>0:
            print("CHAPTER ATTACHMENTS ", files)
            insert_page(chapterid,"Attachments",files,f"{root}/","chapter")
    elif (len(path) - (base_path_len + 3)) == 0: 
        print("PAGE", os.path.basename(root))
        insert_page(chapterid,os.path.basename(root),files,f"{root}/","chapter")
        if len(files)>0:
            print("ATTACHMENTS ", files)
    else:
        print(f"{bcolors.FAIL}TOO DEEP {bcolors.ENDC}", root)
