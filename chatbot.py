import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load your dataset (replace with your data)
with open('action_movie_reviews.json', 'r') as f:
    data = json.load(f)
    


# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(list(data.values()))
sequences = tokenizer.texts_to_sequences(list(data.values()))[0]

# Define the vocabulary size and maximum sequence length
vocab_size = len(tokenizer.word_index) + 1
max_sequence_length = 28077  # Adjust as needed

# Pad sequences to a fixed length
sequences = pad_sequences([sequences], maxlen=max_sequence_length)

# Create training and target sequences
X = sequences[:, :-1]
y = sequences[:, 1:]

# Create the LSTM RNN model
model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=max_sequence_length-1))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))
model.add(Dense(vocab_size, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, batch_size=64)

# Save the model
model.save('text_generation_model.h5')