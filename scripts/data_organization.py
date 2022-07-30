import sys
import json
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
        perms = generate_permutations(letters, start_index, end_index)
        perms = perms.split()
        if len(perms) < 100:
            print(perms)
        # create a key for each scramble and add current word as value
        #print(perms)

        for perm in perms:
            perm = list_to_string(perm)
            if perm in scrambles.keys():
                scrambles[perm].append(word)
            else:
                scrambles[perm] = [word]

    print(scrambles)
    return scrambles

def generate_permutations(word, start_i, end_i) -> List:
    permutations = ''
    temp = []
    if start_i==end_i:
        permutations = list_to_string(word)
    else:
        for i in range(start_i,end_i):
            word[start_i], word[i] = word[i], word[start_i]
            temp = generate_permutations(word, start_i+1, end_i)
            permutations = permutations + ' ' + temp

            word[start_i], word[i] = word[i], word[start_i] # backtrack

    return permutations


def list_to_string(list):
    return ''.join(list)


def write_to_file(file_path, text):
    file = open(file_path, 'w')
    file.write(text)
    file.close()

def write__lines_to_file(file_path, text):
    file = open(file_path, 'w')
    file.writelines(text)
    file.close()

# Takes a
def split_file(file_name:str, source_path:str, target_path:str, file_extension:str, split_max:int ):
    count = 0
    source = '{0}/{1}.{2}'.format(source_path, file_name,  file_extension, 'r')
    source_file = open(source, 'r')
    target = '{0}/{1}_{2}.{3}'.format(target_path, file_name, count, file_extension)
    target_file = open(target, 'w')
    temp_data = []


    source_text = source_file.readlines()
    source_file.close()
    leftover = False

    for i in range(1, len(source_text)):
        if not i == 1 and i%split_max == 1 :

            # File done
            # write and close current file
            target_file.writelines(temp_data)
            target_file.close()
            leftover = False

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
    if leftover:
        target_file.writelines(temp_data)
        target_file.close()






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
file_name = FILES[TEST]
src_file_path = '{0}/../data/'.format(sys.path[0])
target_file_path = '{0}/../data/{1}'.format(sys.path[0], file_name)
file_extension = 'csv'
split_max = 3

split_file(file_name, src_file_path, target_file_path, file_extension, split_max)

print('========================')

#words = file_to_json(sys.path[0]+'/../data/' + file)
#write_to_file(sys.path[0]+'/../data/' + file, json.dumps(words))
#print(json.dumps(words))


# create directiory of file_name_json
# count files in directory
# loop through files and convert to json, wite to file