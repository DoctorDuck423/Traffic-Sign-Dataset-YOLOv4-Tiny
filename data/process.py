import glob
import os
import numpy as np
import sys

current_dir = "obj" 
split_pct = 10;
file_train = open("train.txt", "w")  
file_val = open("test.txt", "w")  
counter = 1  
index_test = round(100 / split_pct)  
for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.txt")): 
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if counter == index_test:
                counter = 1
                file_val.write("data/"+current_dir + "/" + title + '.jpg' + "\n")
        else:
                file_train.write("data/"+current_dir + "/" + title + '.jpg' + "\n")
                counter = counter + 1
file_train.close()
file_val.close()