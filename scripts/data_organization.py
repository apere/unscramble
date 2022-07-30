import sys
import json
import os
from itertools import permutations
from typing import List

# ===============
# FUNCTIONS
# ===============

#converts a file with a word on every line into a json object
def file_to_json(file_path):
    words = open(file_path)
    word_list = words.readlines()
    scrambles = {}

    for i in range(len(word_list)):
        word = word_list[i].rstrip()

        start_index = 0
        end_index = len(word)
        letters = list(word)
        print('------' + word + '-------')
        perms = permutations(word)

        for perm in perms:
            perm = list_to_string(perm)
            if perm in scrambles:
                scrambles[perm].append(word)
            else:
                scrambles[perm] = [word]
    return scrambles




def list_to_string(list)-> str:
    """
    A very unnecessary function that converts a [] to a string
    Args:
        list (_type_):

    Returns:
        _type_: str
    """
    return ''.join(list)


def write_to_file(file_path, text):
    file = open(file_path, 'w')
    file.write(text)
    file.close()

def write__lines_to_file(file_path, text):
    file = open(file_path, 'w')
    file.writelines(text)
    file.close()


def split_file(file_name:str, source_path:str, target_path:str, file_extension:str, split_max:int, word_length_max:int ):
    """
    Takes a text file (in this context, a file with a single word on each line) and splits it
    it into multiple smaller files.

    Args:
        file_name (str): file name without extension
        source_path (str): file path to the directory that contains the source file.
        target_path (str): file path to the directory where the new split files will be saved
        file_extension (str): file extension for the new split files. This should probably always be 'json'
        split_max (int): the max number of words per file
        word_length_max (int): the character count of a word to force a new fie - long words have too much data
    """
    count = 0
    source = '{0}/{1}.{2}'.format(source_path, file_name,  file_extension, 'r')
    source_file = open(source, 'r')
    target = '{0}/{1}_{2}.{3}'.format(target_path, file_name, count, file_extension)
    target_file = open(target, 'w')
    temp_data = []


    source_text = source_file.readlines()
    source_file.close()
    leftover = False
    force_new_file = False

    for i in range(1, len(source_text)):
        if force_new_file or i%split_max == 1 :

            # File done
            # write and close current file
            target_file.writelines(temp_data)
            target_file.close()
            leftover = False
            force_new_file = False

            if not i == len(source_text) -1:
                # refresh for new file
                count = count + 1
                temp_data = []
                target ='{0}/{1}_{2}.{3}'.format(target_path, file_name, count, file_extension)
                target_file = open(target, 'w')
        else:
            # collect data
            temp_data.append(source_text[i])
            leftover = True
            if len(source_text[i]) > word_length_max:
                force_new_file = True
    if leftover:
        target_file.writelines(temp_data)
        target_file.close()


def files_to_json(directory_name:str, src_directory_path:str, target_directory_path:str):
    for file_name in os.listdir(src_directory_path):
        src_file = os.path.join(src_directory_path, file_name)
        target_file = os.path.join(target_directory_path, file_name + '.json')
        if os.path.isfile(src_file) and not str(file_name)[0] == '.':
            print('Reading from file: {0}'.format(src_file))
            words_json = file_to_json(src_file)
            print('Writing to file: {0}'.format(target_file))
            write_to_file(target_file, json.dumps(words_json))
            #print(json.dumps(words_json))
    print('---- DONE: created JSON files ----')




# ===============
# Environment Variables
# ===============
TEST = 0
PRODUCTION = 1
FILES = ['words_short', 'words']

# ===============
# Commands
# ===============


# split files
file_name = FILES[PRODUCTION]
src_file_path = '{0}/../data/'.format(sys.path[0])
target_file_path = '{0}/../data/{1}'.format(sys.path[0], file_name)
file_extension = 'csv'
split_max = 3
max_word_length = 5

split_file(file_name, src_file_path, target_file_path, file_extension, split_max, max_word_length)

print('========================')

#words = file_to_json(sys.path[0]+'/../data/' + file)
#write_to_file(sys.path[0]+'/../data/' + file, json.dumps(words))
#print(json.dumps(words))


# create directiory of file_name_json
# count files in directory
# loop through files and convert to json, wite to file
directory_name = '{0}_json'.format(file_name)
src_directory_path = '{0}/../data/{1}'.format(sys.path[0], file_name)
target_file_path = '{0}/../data/{1}'.format(sys.path[0], directory_name)

files_to_json(directory_name, src_directory_path, target_file_path)