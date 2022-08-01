import sys
import json
import os
import time
from itertools import permutations
from typing import List
from pymongo import MongoClient
import pymongo

# ===============
# FUNCTIONS
# ===============

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
    count = 1
    source = '{0}/{1}.{2}'.format(source_path, file_name,  file_extension, 'r')
    source_file = open(source, 'r')
    target = '{0}/{1}-csv.{2}'.format(target_path, file_name, 'json')
    target_file = open(target, 'w')
    temp_data = []


    source_text = source_file.readlines()
    source_file.close()
    leftover = False
    force_new_file = False

    file_contents = []

    print('---- Splitting Files -----')

    for i in range(1, len(source_text)):
        if force_new_file or i%split_max == 1 :

            # File done
            # write and close current file
            #target_file.writelines(temp_data)
            #target_file.close()
            if len(temp_data) > 0:
                file_contents.append(temp_data)
            leftover = False
            force_new_file = False

            if not i == len(source_text) -1:
                # refresh for new file
                count = count + 1
                temp_data = []
                #target ='{0}/{1}_{2}.{3}'.format(target_path, file_name, count, file_extension)
                #target_file = open(target, 'w')
        else:
            # collect data
            temp_data.append(source_text[i])
            leftover = True
            if len(source_text[i]) > word_length_max:
                force_new_file = True
    if leftover:
        file_contents.append(temp_data)

    target_file.writelines(json.dumps(file_contents))
    target_file.close()

    if i%100 == 0 or i == len(source_text) - 1:
        print('---------------- {0} Files Created'.format(count))

    print('---- Done: Splitting Files ----')


def files_to_json(directory_name:str, src_data, target_directory_path:str, process_id:int, process_count:int):
    print('---- Creating JSON File ----')

    count = 0
    print('got files')

    total_files = len(src_data)
    chunk_size = total_files / process_count

    min_idx = process_id * chunk_size
    max_idx = min_idx + chunk_size

    print('---------------- min index {0}'.format(min_idx))
    print('---------------- max index {0}'.format(max_idx))

    for cur_data in src_data:
        is_file_good_a = count >= min_idx and count < max_idx
        is_file_good_b = process_id == process_count - 1 and count > max_idx
        is_file_good = is_file_good_a or is_file_good_b

        if is_file_good:
            src_file = os.path.join(src_directory_path, file_name)
            target_file = os.path.join(target_directory_path, directory_name + '_'+ str(count) + '.json')

            print('{0} | Reading from file: {1}'.format(count, cur_data))
            words_json = file_to_json(cur_data)

            print('{0} | Writing to file: {1}'.format(count, target_file))
            #write_to_file(target_file, json.dumps(words_json))
        count = count + 1
    print('---- DONE: Creating JSON Files ----')

#converts a file with a word on every line into a json object
def file_to_json(word_list):
    data_out = []

    for i in range(len(word_list)):
        word = word_list[i].rstrip()

        print('------{0}-------'.format( word ))
        perms = permutations(word)

        for perm in perms:
            entry = {}
            entry['permutation'] = list_to_string(perm)
            entry['word'] = word

            data_out.append( entry )
            scrambles_db.update_one(entry, { '$set' : entry }, upsert=True)

    #scrambles_db.update_many(data_out, upsert=True)

    time.sleep(20)

    return data_out

def get_database(connection_string:str, db_name:str ):
    client = MongoClient(connection_string)

    return client[db_name]



# ===============
# Environment Variables
# ===============
TEST = 0
PRODUCTION = 1
FILES = ['words_short', 'words']
DBs = ['unscramble-test', 'unscramble']

enviro = TEST

# ===============
# Commands
# ===============

# init mongodb
mongodb_connection = "mongodb://localhost:27017"

scrambles_mongo = get_database(mongodb_connection, DBs[enviro])
scrambles_db = scrambles_mongo['scrambles']

print('------------ MongoDB Connection Made {0}'.format(scrambles_db))

#time.sleep(10000)

# split files
file_name = FILES[enviro]
src_file_path = '{0}/../data/'.format(sys.path[0])
target_file_path = '{0}/../data/{1}'.format(sys.path[0], file_name)
file_extension = 'csv'
split_max = 3
max_word_length = 6
process_count = 2
process_index = 0


#split_file(file_name, src_file_path, target_file_path, file_extension, split_max, max_word_length)

try:
    process_count = int(sys.argv[1])
    process_index = int(sys.argv[2])
except:
    print('-------------------- arg error')

print('-------------------- process {0} of {1}'.format(process_index, process_count ))

print('========================')

# create directiory of file_name_j
# count files in directory
# loop through files and convert to json, wite to file
directory_name = '{0}_json'.format(file_name)
src_directory_path = '{0}/../data/{1}/{2}-csv.json'.format(sys.path[0], file_name, file_name)
target_file_path = '{0}/../data/{1}'.format(sys.path[0], directory_name)

src_file = open(src_directory_path, 'r')
data = json.loads(src_file.read())
src_file.close()

files_to_json(directory_name, data, target_file_path, process_index, process_count )

print('------- nothing else ------')
#time.sleep(1000000)