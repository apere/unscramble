import sys
import json
from typing import List

# ===============
# FUNCTIONS
# ===============

#converts a file with a word on every line to a json object
def list_to_json(file_path):
    words = open(file_path)
    word_list = words.readlines()
    scrambles = {}

    for count in range(len(word_list)):
        word = word_list[count].rstrip()

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

# ===============
# Environment Variables
# ===============
TEST = 0
PRODUCTION = 1
FILES = ['words_short.csv', 'words.csv']

# ===============
# Commands
# ===============
file = FILES[PRODUCTION]
words = list_to_json(sys.path[0]+'/../data/' + file)

print('========================')
write_to_file(sys.path[0]+'/../data/' + file, json.dumps(words))
print(json.dumps(words))