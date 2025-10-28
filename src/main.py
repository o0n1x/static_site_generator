from textnode import *
import os
import shutil
from config import *
from md_2_html import generate_pages_recursive
def main():
    copy_to_public()


def copy_to_public():
    #delete everything in public
    if os.path.exists(SOURCE_FOLDER):
        shutil.rmtree(DIST_FOLDER)
        os.mkdir(DIST_FOLDER)
        # recursively copy whats in static
        copy_to_public_r("/")
        #generate html files
        generate_pages_recursive("content/","template.html","public/")
    else:
        print("Error: invalid path:" , SOURCE_FOLDER)

    


def copy_to_public_r(source_folder):  
    listdir = os.listdir(SOURCE_FOLDER + source_folder)

    for path in listdir:
        if os.path.isfile(SOURCE_FOLDER + source_folder + path):
            print(f"file {SOURCE_FOLDER + source_folder + path} is copied to {DIST_FOLDER + source_folder + path}")
            shutil.copy(SOURCE_FOLDER + source_folder + path,DIST_FOLDER + source_folder + path)
        else:
            print(f"folder {source_folder + path + "/"} detected making new folder {DIST_FOLDER + source_folder + path}")
            os.mkdir(DIST_FOLDER + source_folder + path)
            copy_to_public_r(source_folder + path + "/")

if __name__ == "__main__":
    main()
