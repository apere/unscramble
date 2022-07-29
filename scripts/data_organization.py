import sys
import json


#converts a file with a word on every line to a json object
def list_to_json(file_path):
    words = open(file_path)
    word_list = words.readlines()
    word_json = {}

    for count in range(len(word_list)):
        word_json[word_list[count].rstrip()] = {}

    return word_json


def write_to_file(file_path, text):
    file = open(file_path, 'w')
    file.write(text)



# commands
words = list_to_json(sys.path[0]+'/../data/words.csv')
print(json.dumps(words))

write_to_file(sys.path[0]+'/../data/words.json', json.dumps(words))