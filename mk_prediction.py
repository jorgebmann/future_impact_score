"""
Prediction of new test data:
    1. load test data
    2. clean data
    3. load tokenizer
    4. apply tokenizer and padding to test data
    5. load model and weihts
    6. predict
"""

from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
import pickle


def mk_prediction(test_data):

    # turn a doc into clean tokens
    def clean_doc(doc):
        # split into tokens by white space
        tokens = doc.split()
        # remove punctuation from each token
        table = str.maketrans('', '', punctuation)
        tokens = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]
        tokens = ' '.join(tokens)
        return tokens

    
    test_x = list()
    test_data = pd.DataFrame([test_data], index = ['abstract'])
    test_data.columns = ['abstract']
    test_data['abstract'] = test_data['abstract'].fillna(' ')
    test_data['abstract'] = test_data['abstract'].str.lower()

    for j in range(len(test_data)):
        if len(test_data.abstract[j].split()) < 500:
            tokens = clean_doc(test_data.abstract[j])
            # add to list
            test_x.append(tokens)
            
    # encode a list of lines
    def encode_text(tokenizer, lines, length):
        # integer encode
        encoded = tokenizer.texts_to_sequences(lines)
        # pad encoded sequences
        padded = pad_sequences(encoded, maxlen=length, padding='post')
        return padded

    # loading tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    length = 382
    testX = encode_text(tokenizer, test_x, length)
    
    
    # when repeating query, it gives an error message
    # solution K.clear_session() after prediction
    # load json and create model
    json_file = open('pred_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    #delete_module('keras.models')
    #tf.keras.backend.clear_session()
    # load weights into new model
    loaded_model.load_weights("pred_model.h5")
    
    batch_size = 512 #256

    # evaluate loaded model on test data
    loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])
    loaded_predictions = loaded_model.predict([testX,testX,testX], batch_size=batch_size, verbose=1)
    if loaded_predictions[0] <= 2:
        fis = 'very low'
    elif (loaded_predictions[0] > 2) and (loaded_predictions[0] <= 5):
        fis = 'low'
    elif (loaded_predictions[0] > 5) and (loaded_predictions[0] <= 10):      
        fis = 'intermediate'
    elif (loaded_predictions[0] > 10) and (loaded_predictions[0] <= 20):      
        fis = 'high'
    elif loaded_predictions[0] > 20:
        fis = 'very high'
    #print(fis)
    #loaded_df = pd.DataFrame(loaded_predictions)
    
    K.clear_session()

    return fis
