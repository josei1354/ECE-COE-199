import cv2
import numpy as np
import h5py
import os
import string

from data import preproc as pp, evaluation
from data.generator import DataGenerator, Tokenizer
from data.reader import Dataset

from PSG import *

from network.model import HTRModel

def HTR(image_path):

    img = pp.preprocess(image_path, input_size=input_size)

    x_test = pp.normalization([img])

    predicts, probabilities = model.predict(x_test, ctc_decode=True)
    predicts = [[tokenizer.decode(x) for x in y] for y in predicts]

    print(predicts[0][0])
    return predicts[0][0]

if __name__ == "__main__":

    curr_dir = os.getcwd()
    
    orig_dir = "lines" #Change this line only
    
    os.chdir(curr_dir + "\\" + orig_dir)
    dirs = os.listdir()
    os.chdir(curr_dir)

    
    archi = "flor"
    target_path = "train_weights/flor_checkpoint_weights.hdf5"

    input_size = (1024, 128, 1)
    max_text_length = 128
    charset_base = string.printable[:95]

    tokenizer = Tokenizer(chars=charset_base, max_text_length=max_text_length)

    model = HTRModel(architecture=archi,
                     input_size=input_size,
                     vocab_size=tokenizer.vocab_size,
                     beam_width=10,
                     top_paths=10)

    model.compile(learning_rate=0.001)
    model.load_checkpoint(target=target_path)

    print("Model Loaded")

    for direc in dirs:
    
        dir_to_scan = orig_dir + "\\" + direc
  
        os.chdir(curr_dir + "\\" + dir_to_scan)
        subdirectories = os.listdir()
        os.chdir(curr_dir)

        for subdir in subdirectories:

            os.chdir(curr_dir + "\\" + dir_to_scan + "\\" + subdir)
            image_files_list = os.listdir()
            os.chdir(curr_dir)
        
            f = open(dir_to_scan + "\\" + subdir + "\\00_predicts.txt", "w")

            for image_filename in image_files_list:
                print(image_filename, end='\t')
                pred = HTR(dir_to_scan + "\\" + subdir + "\\" + image_filename)

                f.write(image_filename + "\t" + pred + "\n")

            f.close()

    print("End")
