# Script for bookstackapp import
This script is based on the work of https://github.com/lotfihamid/Bookstack-importdocs/blob/master/importdocs.py
## Use-Case
* (Ab-)use Bookstackapp as a network drive replacement 
* Integrated viewers, e.g., pdf viewer, video player, image rendering
* Knowledge base 

## How to use the import.py script
1. Ensure no file names include the following characters: ( ) ,
2. Set the correct path, url, token, base_path_len variables
3. "Dry-run" the script by commenting out all the insert_... calls
   -> You will see how the shelves/books/chapters/pages/attachments will be created and can adapt the variables accordingly.
   -> Make sure there are no errors (ignore the root error). 
    * ERROR:SHELVEPAGE means the directory is not deep enough, so add another subfolder
    * TOO DEEP means the directory is too deep. Try to reorganize or move folders up a level in the respective directories.
4. Make sure there are no errors and then run the script with the insert_... calls. 
   * You might have to tune server parameters to allow different file size uploads.

## How to use the html_header.html script
Define the file extension types you want to automatically render on page load
   * The first line renders an iframe object
   * The second line creates an image tag
   * The previewImg function enables toggle previews of images (small width) and full display (page width)