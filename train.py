import json
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

 c
# Load your Instagram message data from JSON
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract and clean message text
messages = [entry["message"] for entry in data]

# Tokenize the text using a tokenizer with a limited vocabulary
tokenizer = Tokenizer(num_words=5000)  # Adjust the vocabulary size as needed
tokenizer.fit_on_texts(messages)
total_words = len(tokenizer.word_index) + 1

# Convert text to sequences of numerical tokens
sequences = tokenizer.texts_to_sequences(messages)


# Pad sequences to have the same length
max_sequence_length = max([len(seq) for seq in sequences])
print(max_sequence_length)
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding="pre")

# Create input sequences and labels for training
input_sequences = []
for sequence in padded_sequences:
    for i in range(1, len(sequence)):
        n_gram_sequence = sequence[: i + 1]
        input_sequences.append(n_gram_sequence)

# Pad input sequences to have the same length
max_input_sequence_length = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(
    input_sequences, maxlen=max_input_sequence_length, padding="pre"
)

# Separate the last column (labels)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

# Convert labels to one-hot encoding
y = to_categorical(y, num_classes=total_words)

# Build a simplified RNN model
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_input_sequence_length - 1))
model.add(LSTM(150))
model.add(Dense(total_words, activation="softmax"))

# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam")

# Train the model
model.fit(X, y, epochs=5, verbose=1)
# Save the model architecture to a JSON file
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# Save the model weights to an HDF5 file
model.save_weights("model_weights.h5")

with open("tokenizer.json", "w") as tokenizer_file:
    tokenizer_json = tokenizer.to_json()
    tokenizer_file.write(tokenizer_json)
# Load the Tokenizer if save
