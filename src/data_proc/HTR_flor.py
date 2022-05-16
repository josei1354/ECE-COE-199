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

    archi = "flor"
    target_path = "../../../src/data_proc/train_weights/flor_checkpoint_weights.hdf5"

    input_size = (1024, 128, 1)
    max_text_length = 128
    charset_base = string.printable[:95]

    tokenizer = Tokenizer(chars=charset_base, max_text_length=max_text_length)

    img = pp.preprocess(image_path, input_size=input_size)

    x_test = pp.normalization([img])

    model = HTRModel(architecture=archi,
                     input_size=input_size,
                     vocab_size=tokenizer.vocab_size,
                     beam_width=10,
                     top_paths=10)

    model.compile(learning_rate=0.001)
    model.load_checkpoint(target=target_path)

    predicts, probabilities = model.predict(x_test, ctc_decode=True)
    predicts = [[tokenizer.decode(x) for x in y] for y in predicts]

    print(predicts[0][0])
    return predicts[0][0]

if __name__ == "__main__":
    print("Hello1")

    archi = "flor"
    target_path = "train_weights/flor_checkpoint_weights.hdf5"
    image_path = "blank_samples_p1/Abdomen2b.png"

    input_size = (1024, 128, 1)
    max_text_length = 128
    charset_base = string.printable[:95]

    print("Hello2")
    
    tokenizer = Tokenizer(chars=charset_base, max_text_length=max_text_length)

    img = pp.preprocess(image_path, input_size=input_size)

    cv2.imwrite("samples2/HTROut.png", img)

    print("Hello3")
    
    x_test = pp.normalization([img])

    print("Hello4")

    model = HTRModel(architecture=archi,
            input_size=input_size,
            vocab_size=tokenizer.vocab_size,
            beam_width=10,
            top_paths=10)

    model.compile(learning_rate=0.001)
    model.load_checkpoint(target=target_path)

    print("Hello5")

    predicts, probabilities = model.predict(x_test, ctc_decode=True)
    predicts = [[tokenizer.decode(x) for x in y] for y in predicts]

    print("Hello6")

    print("\n####################################")
    print(predicts[0][0])
    #for i, (pred, prob) in enumerate(zip(predicts, probabilities)):
    #    print("\nProb.  - Predict")
    #
    #    for (pd, pb) in zip(pred, prob):
    #        print(f"{pb:.4f} - {pd}")

    cv2.imshow("Image", cv2.imread(image_path))
    print("\n####################################")
    cv2.waitKey(0)
    cv2.destroyAllWindows()