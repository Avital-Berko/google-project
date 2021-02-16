from collections import defaultdict
import os
import json
import pickle


DATA_PATH = "/content/drive/MyDrive/Aechive"

def read_data_from_dir():
    i = 0
    sentence_meta_data = {}
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".txt"):
            with open(DATA_PATH + "/" + filename, encoding="utf8") as f:
                lines = set(f.readlines())
                for line in lines:
                    sentence_meta_data[i] = (line, filename)
                    i += 1

    return sentence_meta_data
    
def pure_key(subsen):
    lower_key = subsen.lower()
    key = "".join([char for char in lower_key if (char.isalpha() or char == ' ')])
    clean_key = " ".join([word.strip() for word in key.split()])
    return clean_key
    
def create_db(meta_data):
    dictionary_of_sentences = defaultdict(set)
    for key, line in meta_data.items():
        for offset in range(len(line[0]) - 1):
            if offset == 0 or line[0][offset - 1] == ' ':
                for j in range(offset + 1, len(line[0])):
                    clean_key = pure_key(line[0][offset:j])
                    if len(dictionary_of_sentences.get(clean_key, [])) < 5 and len(clean_key) < 20:
                        dictionary_of_sentences[clean_key].add(key)
    d = dict()
    for key, val in dictionary_of_sentences.items():
        d[key] = list(val)

    return d


def main():     
    meta_data = read_data_from_dir()
    # print(len(meta_data))
    data = create_db(meta_data)

    with open('/content/drive/MyDrive/sentence_data5.json', 'w') as f:
        json.dump(data, f)

    with open('/content/drive/MyDrive/meta_data6.json', 'w') as f:
        json.dump(meta_data, f)

if __name__ == "__main__":
    main()
