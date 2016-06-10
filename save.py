import os
import sys

# Contains methods for creating .html files from server responses,
# and their respective parent directories.


# Saves an html page on a path
def save_html(html, page):
    print(page)
    page = page.split('//', 1)[1]
    make_dirs(page)
    f = open(page + 'index.html', 'wb')
    f.write(html)
    f.close()
    os.chdir(sys.path[0])


# Makes directories for a particular file-path if they do not already exist
def make_dirs(filename):
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)