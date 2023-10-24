import json
import numpy as np
from keras.models import model_from_json
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences

# Load the Tokenizer if saved
with open("tokenizer.json", "r") as tokenizer_file:
    tokenizer_json = tokenizer_file.read()
    tokenizer = tokenizer_from_json(tokenizer_json)

# Load the model architecture from a JSON file
with open('model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

# Create a new model from the loaded JSON
loaded_model = model_from_json(loaded_model_json)

# Load the model weights into the new model
loaded_model.load_weights('model_weights.h5')


# Function to generate a reply
def generate_reply(input_text, model, max_sequence_length):
    seed_text = input_text  # Initialize seed_text with the user input
    generated_text = seed_text  # Initialize generated_text with seed_text

    for _ in range(10):  # Generate 10 words in the reply
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')
        predicted = model.predict(token_list, verbose=0)
        predicted_class = np.argmax(predicted)
        output_word = ""

        for word, index in tokenizer.word_index.items():
            if index == predicted_class:
                output_word = word
                break
        generated_text += " " + output_word
        seed_text = generated_text  # Update seed_text with the generated output

    return generated_text


# User interaction loop
while True:
    user_input = input("Ask a question (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break

    # Generate a reply
    reply = generate_reply(user_input, loaded_model, 2)
    print("Bot: " + reply)

# Exit the program
print("Goodbye!")
