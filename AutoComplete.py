import json
from extractData import meta_data, data
import re


def get_add_and_delete_score(txt, offset):

    reduce = 2
    if offset < 4:
        reduce = 10 - 2 * offset
    
    return 2 * len(txt) - reduce


def get_replace_score(txt, offset):

    reduce = 1
    if offset < 4:
        reduce = 5 - offset
    
    return 2 * (len(txt) - 1) - reduce


def get_completed_by_add(clean_input):
    completed_sentences_ids = set()

    for i in range(0, len(clean_input) + 1):
        for c in range(26):
            first_part = clean_input[:i]
            end_part = clean_input[i:]
            new_string = first_part + chr(c + ord('a')) + end_part
            # print(new_string)

            list_completed_sentences_ids = data.get(new_string)
            if list_completed_sentences_ids:
                score = get_add_and_delete_score(clean_input, i)
                for comp_sent_id in list_completed_sentences_ids:
                    completed_sentences_ids.add((comp_sent_id, score))

    completed_sentences = [(meta_data[id[0]], id[1]) for id in completed_sentences_ids]
    return completed_sentences


def get_completed_by_delete(clean_input):
    completed_sentences_ids = set()

    for i in range(0, len(clean_input)):

        start_txt = clean_input[:i]
        end_txt = clean_input[i + 1:]
        new_string = start_txt + end_txt

        list_completed_sentences_ids = data.get(new_string)
        if list_completed_sentences_ids:
            score = get_add_and_delete_score(new_string, i)
            for comp_sent_id in list_completed_sentences_ids:
                completed_sentences_ids.add((comp_sent_id, score))

    completed_sentences = [(meta_data[id[0]], id[1]) for id in completed_sentences_ids]
    return completed_sentences


def get_completed_by_replace(clean_input):
    completed_sentences_ids = set()
    for i in range(0, len(clean_input)):
        string_list = list(clean_input)
        for c in range(26):
            string_list[len(clean_input) - i - 1] = chr(c + ord('a'))
            new_string = "".join(string_list)

            list_completed_sentences_ids = data.get(new_string, 0)
            if list_completed_sentences_ids != 0:
                score = get_replace_score(clean_input, len(clean_input) - i - 1)
                for comp_sent_id in list_completed_sentences_ids:
                    completed_sentences_ids.add((comp_sent_id, score))

    completed_sentences = [(meta_data[id[0]], id[1]) for id in completed_sentences_ids]
    return completed_sentences


def pure_key(subsen):
    lower_key = subsen.lower()
    key = "".join([char for char in lower_key if (char.isalpha() or char == ' ')])
    clean_key = " ".join([word.strip() for word in key.split()])
    return clean_key


def get_completion(clean_input):
    completed_list = []
    sentences_ids = data.get(clean_input, [])
    for sentence_id in sentences_ids:
        completed_sentence = meta_data[sentence_id]
        completed_list.append((completed_sentence, (len(clean_input) * 2)))
    completed_list += get_completed_by_replace(clean_input)
    completed_list += get_completed_by_add(clean_input)
    completed_list += get_completed_by_delete(clean_input)
    return completed_list


def get_five_completion(input):
    completed_list = get_completion(pure_key(input))
    # [((str,path),score),....]
    sort_completed_list = sorted(completed_list, key=lambda x: x[1], reverse=True)
    return sort_completed_list[:5]


def main():
    while True:
        user_input = input("\nEnter your text:\n")
        while True:
            try:
                if len(user_input) > 15:
                    user_input = user_input.split()[-1]
                five_completion = get_five_completion(user_input)
                for i, comp in enumerate(five_completion):
                    print(i + 1, comp)

                if user_input[-1] == "#":
                    break
                user_input += input(user_input)
            except:
                print("exception Occurred")

main()
