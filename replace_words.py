import Levenshtein
import json
import base64

with open ("data.json","r") as file:
    data = json.load(file)


ALPHABETS = ['a','i','u','e','o']

def remove_alphabets(input_string):
    for alphabet in ALPHABETS:
        input_string = input_string.replace(alphabet, '')
    return input_string


def calculate_similarity(query, message):
    ratio =  Levenshtein.ratio(str(query).lower(), str(message).lower())
    return ratio

input_text = input("Enter a query: ")
input_without_alphabets = remove_alphabets(input_text)

similar_words = []
for index, message in enumerate(data):
        similarity = calculate_similarity(input_text, message["message"])
        if similarity > 0.7 and index < len(data) - 1:
             similar_words.append(message['message'])
        else:
            for index, message in enumerate(data):
                similarity = calculate_similarity(input_without_alphabets, message["message"])
                if similarity > 0.7:
                    similar_words.append(message['message'])
                  
                

print("Similar words:")
for word in similar_words:
    print(word)