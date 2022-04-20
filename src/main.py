import cv2
import numpy as np
import os
import sys
import json

curr_dir = os.getcwd()
path_to_append = os.path.join(curr_dir,"preproc")

sys.path.insert(0,path_to_append)

path_to_append_1 = os.path.join(curr_dir,"data_proc")
sys.path.insert(0,path_to_append_1)

from preproc_main import *
from dataproc_main import *

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
        page_folder = filename[:5]
        new_dir = os.path.join(new_dir, page_folder)
        filename = filename[6:]
        os.chdir(new_dir)
    #print(filename)
    #print(os.getcwd())
    #at this point, filename is "directory/filename.png" or just "filename.png"

    if(filename.find("/") > 0):
        temp = filename.find("/")
        data_number = filename[:temp]
        new_dir = os.path.join(new_dir,data_number)
        os.chdir(new_dir)
        filename = filename[(temp+1):]

    #print(filename)
    #print(os.getcwd())

    #at this point. filename is just "filename.png" and that file is in the same working directory

    #print("Current Dir: ", page_folder, data_number)
    
    preproc_main(filename, page_number)

    final_output_dict = dataproc_main(page_number)

    json_filename = "output_" + page_folder + "_" + data_number + ".json"
    print("Writing to", json_filename)
    
    with open(json_filename, "w") as outfile:
        json.dump(final_output_dict, outfile, indent=4)
    print("Complete")
    
