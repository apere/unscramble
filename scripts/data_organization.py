import sys
import json
from typing import List


#converts a file with a word on every line to a json object
def list_to_json(file_path):
    words = open(file_path)
    word_list = words.readlines()

    for count in range(len(word_list)):
        scrambles = {}
        word = word_list[count].rstrip()

        start_index = 0
        end_index = len(word)
        letters = list(word)

        perms = generate_permutations(letters, start_index, end_index)

        # create a key for each scramble and add current word as value
        for perm in perms:
            if perm in scrambles:
                # append
                scrambles[perm].append(word)
            else:
                scrambles[perm] = [word]
    return scrambles

def generate_permutations(word, stard_i, end_i) -> List:
    permutations = []
    if stard_i==end_i:
        permutations.append(list_to_string(word))
    else:
        for i in range(stard_i,end_i):
            word[stard_i], word[i] = word[i], word[stard_i]
            generate_permutations(word, stard_i+1, end_i)
            word[stard_i], word[i] = word[i], word[stard_i] # backtrack

    return permutations

def list_to_string(list):
    return ''.join(list)


def write_to_file(file_path, text):
    file = open(file_path, 'w')
    file.write(text)


# commands
words = list_to_json(sys.path[0]+'/../data/words.csv')


write_to_file(sys.path[0]+'/../data/words.json', json.dumps(words))
print(json.dumps(words))