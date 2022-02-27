import cv2
import numpy as np
import os
import sys

curr_dir = os.getcwd()
path_to_append = os.path.join(curr_dir,"preproc")

sys.path.insert(0,path_to_append)

from preproc_main import *

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", type=str,required=True)
    parser.add_argument("--pagenum", type=int,required=True)
    args = parser.parse_args()

    filename = args.filename
    page_number = args.pagenum

    curr_dir = os.getcwd()
    new_dir=curr_dir

    while True:
        if filename[:3] == "../" or filename[:3]== "..\\":
            filename = filename[3:]
            new_dir = os.path.dirname(new_dir)
        else:
            break

    os.chdir(new_dir)

    #print(os.getcwd())

    if filename[:11] == "data_actual":
        new_dir = os.path.join(new_dir, "data_actual")
        filename = filename[12:]
        pagefolder = filename[:5]
        new_dir = os.path.join(new_dir, pagefolder)
        filename = filename[6:]
        os.chdir(new_dir)
    #print(filename)
    #print(os.getcwd())
    #at this point, filename is "directory/filename.png" or just "filename.png"

    if(filename.find("/") > 0):
        temp = filename.find("/")
        new_dir = os.path.join(new_dir,filename[:temp])
        os.chdir(new_dir)
        filename = filename[(temp+1):]

    #print(filename)
    #print(os.getcwd())

    #at this point. filename is just "filename.png" and that file is in the same working directory

    preproc_main(filename, page_number)
